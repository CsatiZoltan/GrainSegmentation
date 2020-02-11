"""
This module contains the GrainSegmentation class, responsible for the image
segmentation of grain-based materials (rocks, metals, etc.)
"""

import os.path as path
import numpy as np
import scipy.ndimage as ndi
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
        self.__stored_graph = None
        # Load the image and optionally show it
        self.original_image = io.imread(image_location)
        if self.__interactive_mode:
            io.imshow(self.original_image)
            io.show()
            print('Image successfully loaded.')

    def filter_image(self, window_size, image_matrix=None):
        """Median filtering on an image.
        The median filter is useful in our case as it preserves the important
        borders (i.e. the grain boundaries).

        Parameters
        ----------
        window_size : int
            Size of the sampling window.
        image_matrix : 3D ndarray with size 3 in the third dimension, optional
            Input image to be filtered. If not given, the original image is used.

        Returns
        -------
        filtered_image : 3D ndarray with size 3 in the third dimension
            Filtered image, output of the median filter algorithm.
        """

        if image_matrix is None:
            image = self.original_image
        else:
            assert np.shape(image_matrix)[2],\
                   'ndarray with size 3 in the third dimension expected.'
        filtered_image = ndi.median_filter(image, window_size)
        if self.__interactive_mode:
            io.imshow(filtered_image)
            io.show()
            print('Median filtering finished.')
        return filtered_image

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

    def merge_clusters(self, segmented_image, threshold=5):
        """Merge tiny superpixel clusters.
        Superpixel segmentations result in oversegmented images. Based on graph
        theoretic tools, similar clusters are merged.

        Parameters
        ----------
        segmented_image : ndarray
            Label image, output of a segmentation.
        threshold : float, optional
            Regions connected by edges with smaller weights are combined.

        Returns
        -------
        merged_superpixels : ndarray
            The new labelled array.
        """

        if self.__stored_graph is None:
            # Region Adjacency Graph (RAG) not yet determined -> compute it
            g = graph.rag_mean_color(self.original_image, segmented_image)
            self.__stored_graph = g
        else:
            g = self.__stored_graph
        merged_superpixels = graph.cut_threshold(segmented_image, g, threshold, in_place=False)
        if self.__interactive_mode:
            io.imshow(color.label2rgb(merged_superpixels, self.original_image, kind='avg'))
            io.show()
            print('Tiny clusters merged. '
                  'Number of segments: {0}'.format(np.amax(merged_superpixels)))
        return merged_superpixels

    def build_graph(self):
        
        pass
    
    def find_grain_boundaries(self):
        
        pass
    
    def create_skeleton(self):
        
        pass

