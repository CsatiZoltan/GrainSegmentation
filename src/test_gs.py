#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os.path as path

from grain_segmentation import GrainSegmentation


# User-defined parameters

# Use a sample image shipped with the code (https://stackoverflow.com/a/36476869/4892892)
script_dir = path.dirname(__file__) # absolute directory the script is in
rel_image_path = '../data/homogeneous_1_cropped.png'
abs_image_path = path.join(script_dir, rel_image_path)

# Perform all image processing steps the class offers
GS = GrainSegmentation(abs_image_path, interactive_mode=True)
filtered = GS.filter_image(5)
segmented = GS.initial_segmentation(filtered)
reduced = GS.merge_clusters(segmented, threshold=5)
boundary = GS.find_grain_boundaries(reduced)
skeleton = GS.create_skeleton(boundary)
