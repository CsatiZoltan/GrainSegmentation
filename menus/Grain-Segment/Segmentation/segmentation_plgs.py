import numpy as np
from scipy.ndimage import median_filter
from scipy.ndimage.morphology import distance_transform_edt
from skimage import data, io, segmentation, color, measure
from skimage.morphology import skeletonize, watershed
from skimage.future import graph
from imagepy.core import ImagePlus
from imagepy.core.engine import Filter, Simple
from imagepy.core.manager import ImageManager
from imagepy.core.util import fileio
from imagepy import IPy
from imagepy.menus.Process.Segment.shift_plgs import Quickshift
from imagepy.menus.Process.Filters.classic_plgs import Median
from imagepy.menus.Image.Type.convert_plg import ToInt32
from imagepy.menus.Image.duplicate_plg import Duplicate
from imagepy.menus.Process.Segment.graph_plgs import RagThreshold
from imagepy.menus.Process.Binary.distance_plgs import Skeleton
from imagepy.menus.Analysis.label_plg import Boundaries

from .gala_light import imextendedmin


class DuplicateNoGUI(Duplicate):

    @classmethod
    def copy(cls, ips, name):
        img = ips.img.copy()
        ipsd = ImagePlus([img], name)
        ipsd.back = ips.back
        ipsd.chan_mode = ips.chan_mode
        cls.para['name'] = name
        IPy.show_ips(ipsd)
        return ipsd

    def run(self, ips, imgs, para=None):
        pass

    pass


class OpenImage(fileio.Reader):
    """Open an image as store it for further processing."""
    title = 'Open image'
    filt = ['bmp', 'jpeg', 'jpg', 'png', 'tif']  # supported image formats

    def run(self, para=None):
        from . import storage
        storage.original_image = io.imread(para['path'])
        super().run(para)


class FilterImage(Median):
    """Median filtering of the current image."""
    title = 'Filter image'
    para = {'size': 5}

    def load(self, ips):
        super().load(ips)
        ips.data = DuplicateNoGUI.copy(ips, ips.title)  # create a copy from the original image
        ips.title = ips.title + '-filtered'  # rename original image
        return True

    def run(self, ips, snap, img, para = None):
        median_filter(snap, para['size'], output = img)


class InitialSegmentation(Quickshift):
    title = 'Quick shift segmentation'

    def run(self, ips, snap, img, para=None):
        from . import storage
        segment_mask = segmentation.quickshift(snap, para['ratio'], para['kernel_size'], para['max_dist'],
                                               para['sigma'])
        # Save the label image before plotting it (we will use it in the later steps)
        storage.segment_mask = segment_mask
        print(np.amax(segment_mask))
        # The final image is opened on a new tab
        IPy.show_img([color.label2rgb(segment_mask, storage.original_image, kind='avg')], ips.title + '-segmented')


class MergeClusters(RagThreshold):
    """Almost a complete reimplementation of the `RagThreshold` class to circumvent selecting from the open images,
    rather work with the label image obtained by segmentation.
    """
    title = 'Merge tiny clusters'
    para = {'thresh': 5, 'connect': '8-connected', 'mode': 'distance', 'sigma': 255.0}
    view = [(int, 'thresh', (1, 1024), 0, 'threshold', ''),
            (list, 'connect', ['4-connected', '8-connected'], str, 'connectivity', ''),
            (list, 'mode', ['distance', 'similarity'], str, 'mode', ''),
            (float, 'sigma', (0, 1024), 1, 'sigma', 'similarity')]

    def preview(self, ips, para):
        from . import storage
        connect = ['4-connected', '8-connected'].index(para['connect']) + 1
        g = graph.rag_mean_color(storage.original_image, storage.segment_mask, connect, para['mode'], para['sigma'])
        merged_superpixels = graph.cut_threshold(storage.segment_mask, g, para['thresh'], in_place = False)
        storage.merged_superpixels = merged_superpixels
        print(np.amax(storage.merged_superpixels))
        # The image preview is displayed on the current image. By changing the `img` attribute of `ips`, the image
        # update callback is invoked
        ips.img[:] = color.label2rgb(merged_superpixels, storage.original_image, kind = 'avg')

    def run(self, ips, imgs, para=None):
        from . import storage
        connect = ['4-connected', '8-connected'].index(para['connect']) + 1
        g = graph.rag_mean_color(storage.original_image, storage.segment_mask, connect, para['mode'], para['sigma'])
        merged_superpixels = graph.cut_threshold(storage.segment_mask, g, para['thresh'], in_place = False)
        storage.merged_superpixels = merged_superpixels
        print(np.amax(storage.merged_superpixels))
        # The final image is opened on a new tab
        IPy.show_img([color.label2rgb(merged_superpixels, storage.original_image, kind = 'avg')], '-merged')


class FindGrainBoundaries(Boundaries):
    title = 'Find grain boundaries'
    note = ['all']

    def run(self, ips, imgs, para=None):
        from . import storage
        # RGB images are not supported by the `find_boundaries` function of scikit-image
        rgb2int = ToInt32()
        rgb2int.run(ips, imgs, para)
        # We can now invoke ImagePy's boundary marker function
        super().run(ips, imgs, para)


class CreateSkeleton(Skeleton):
    title = 'Create skeleton'

    def run(self, ips, snap, img, para=None):
        from . import storage
        im = skeletonize(snap > 0)
        storage.skeleton_image = im.astype(np.bool)
        im.dtype = np.uint8
        im *= 255
        IPy.show_img([im], '-skeleton')


class WatershedSegmentation(Simple):
    title = 'Watershed segmentation'
    note = ['8-bit']

    def run(self, ips, imgs, para = None):
        from . import storage
        # Create a distance function whose maxima will serve as watershed basins
        distance_function = distance_transform_edt(1 - storage.skeleton_image)
        # Turn the distance function to a negative distance function for watershed
        distance_function = np.negative(distance_function)
        # Do not yet use watershed as that would result an oversegmented image
        # (each local minima of the distance function would become a catchment basin).
        # Hence, first execute the extended-minima transform to find the regional minima
        mask = imextendedmin(distance_function, 2)
        # The watershed segmentation can now be performed
        labelled = measure.label(mask)
        segmented = watershed(distance_function, labelled)

        IPy.show_img([color.label2rgb(segmented)], '-watershed')


plgs = [OpenImage, FilterImage, InitialSegmentation, MergeClusters, FindGrainBoundaries, CreateSkeleton, WatershedSegmentation]
