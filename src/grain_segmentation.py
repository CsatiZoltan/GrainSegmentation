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
    
    def __init__(self, image_location, save_location=None, show_plots=True):
        """Initialize the class with file paths and with some options
        
        Parameters
        ----------
        image_location : str
            Path to the image to be segmented, file extension included.
        save_location : str, optional
            Path to directory where images will be outputted. If not given, the
            same directory is used where the input image is loaded from.
        show_plots : bool, optional
            When True, images of each image manipulation step are plotted.
            Default is True.

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
        self.show_plots = show_plots
        
        # Load the image and optionally show it
        self.original_image = io.imread(image_location)
        if self.show_plots:
            io.imshow(self.original_image)

    
    def build_graph(self):
        
        pass
    
    def filter_image(self):
        
        pass
    
    def initial_segmentation(self):
        
        pass
    
    def merge_clusters(self):
        
        pass
    
    def find_grain_boundaries(self):
        
        pass
    
    def create_skeleton(self):
        
        pass

