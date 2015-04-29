#!/usr/bin/env python

"""Client code for Final Project (Depth Image Segmentation)."""

import os
from random import randint

import color_image
import depth_image

__author__ = "Micah Brown and Jackson Spell"
__email__ = "msbrown@davidson.edu, jaspell@davidson.edu"

def main():

	depth_file = os.path.expanduser("~/Desktop/Images/DepthData/img_0000.yml")
	color_file = os.path.expanduser("~/Desktop/Images/KinectColor/img_0000.png")

	test_file = "test.png"

	#image = color_image.ColorImage(color_file)
	#image = color_image.ColorImage(w=20, h=100)

	image = depth_image.DepthImage(depth_file)

	#print len(image.image[0])

	image.write_to_file(test_file)

def create_segmented_image(regions, width, height):
	"""
	Create a ColorImage made from the segmented regions given.

	Parameters:
		regions - list of lists of tuples - segmented regions
		width - int - width of image in pixels
		height - int - height of image in pixels

	Returns:
		ColorImage of segmented regions
	"""

	segmented_image = color_image.ColorImage(width=width, height=height) 
	#print segmented_image
	
	for region in regions:

		#pick a random color for that entire region
		rgb = [randint(0,255),randint(0,255),randint(0,255)]

		for coord_tuple in region:

			#Now go through and change the R, G, and B vals.
			for i in range(0,3): 

				segmented_image.image[coord_tuple[1]][3*coord_tuple[0]+i] = rgb[i]
														  
	return segmented_image


if __name__ == "__main__":
	main()