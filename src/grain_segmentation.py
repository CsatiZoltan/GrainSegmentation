"""
This module contains the GrainSegmentation class, responsible for the image
segmentation of grain-based materials (rocks, metals, etc.)
"""

import os.path as path
import numpy as np
import matplotlib.pyplot as plt
from skimage import io, segmentation, color, measure
from skimage.future import graph
from skimage.morphology import skeletonize
from skimage.util import img_as_uint


class GrainSegmentation():
    """Segmentation of grain-based microstructures
    """

    def __init__(self, image_location, save_location=None, interactive_mode=True):
        """Initialize the class with file paths and with some options

        Parameters
        ----------
        image_location : str
            Path to the image to be segmented, file extension included.
        save_location : str, optional
            Path to directory where images will be outputted. If not given, the
            same directory is used where the input image is loaded from.
        show_plots : bool, optional
            When True, images of each image manipulation step are plotted and
            details are shown in the console.
            Default is False.

        Returns
        -------
        None.
        """

        # Check inputs
        assert path.isfile(image_location), 'Image file {0} does not exist'.format(image_location)
        extension = path.splitext(image_location)[1][1:]
        allowed_extensions = ['png', 'bmp', 'tiff']
        assert extension in allowed_extensions, \
            'Unsupported image file type {0}. Choose from one of the following \
             image types: {1}.'.format(extension, allowed_extensions)
        self.image_location = image_location
        if save_location is None:
            self.save_location = path.dirname(image_location)
        else:
            self.save_location = save_location
        self.__interactive_mode = interactive_mode
        
        # Load the image and optionally show it
        self.original_image = io.imread(image_location)
        if self.__interactive_mode:
            io.imshow(self.original_image)
            io.show()
            print('Image successfully loaded.')

    def initial_segmentation(self, *args):
        """Perform the quick shift superpixel segmentation on an image.
        The quick shift algorithm is invoked with its default parameters.

        Parameters
        ----------
        *args : 3D numpy array with size 3 in the third dimension
            Input image to be segmented. If not given, the original image is used.

        Returns
        -------
        segment_mask : numpy array
            Label image, output of the quick shift algorithm.
        """

        if args:
            image = args[0]
        else:
            image = self.original_image
        segment_mask = segmentation.quickshift(image)
        if self.__interactive_mode:
            io.imshow(color.label2rgb(segment_mask, self.original_image, kind='avg'))
            io.show()
            print('Quick shift segmentation finished. '
                  'Number of segments: {0}'.format(np.amax(segment_mask)))
        return segment_mask
    
    
    
    def build_graph(self):
        
        pass
    
    def filter_image(self):
        
        pass
    
    
    
    def merge_clusters(self):
        
        pass
    
    def find_grain_boundaries(self):
        
        pass
    
    def create_skeleton(self):
        
        pass

