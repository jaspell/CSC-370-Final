#!/usr/bin/env python

"""Client code for Final Project (Depth Image Segmentation)."""

import os

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


if __name__ == "__main__":
	main()