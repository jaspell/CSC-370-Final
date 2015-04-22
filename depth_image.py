#!/usr/bin/env python

"""Depth Image object for Final Project (Depth Image Segmentation)."""

import sys

import yaml

import color_image

__author__ = "Micah Brown and Jackson Spell"
__email__ = "msbrown@davidson.edu, jaspell@davidson.edu"

class DepthImage:
	"""
	A depth image.
	"""

	def __init__(self, image_file=None, width=None, height=None):
		"""
		Image Constructor.

		Parameters:
			image_file - string - path to original image
			w - int - pixel width of image
			h - int - pixel height of image

		Returns:
			instantiated ColorImage:
				matching original if file is given
				empty (pixels are 0) if w, h given
		"""

		if image_file is not None:
			self.width, self.height, self.image = self.read_image(image_file)

		else:
			self.width = width
			self.height = height

			self.image = [[0 for j in range(self.width)] for i in range(self.height)]

	def read_image(self, image_file):
		"""
		Read in image from YML file.

		Parameters:
			image_file - string - path to file containing YML image

		Returns:
			width, height, image as 2D array of ints
		"""

		with open(image_file, 'r') as inf:

			data = yaml.load(inf)

			

	def write_to_file(self, filename):
		"""
		Write a greyscale version of the image to file.

		Parameters:
			filename - string - path to file

		Returns:
			None
		"""

		maximum = 0
		minimum = sys.maxint

		# Determine the max and min values of the image.
		for line in self.image:
			for value in line:

				if value > maximum:
					maximum = value

				elif value < minimum:
					minimum = value

		# Create a new empty color image to write greyscale onto.
		greyscale = color_image.ColorImage(width=self.width, height=self.height)

		# Replace pixels in the color image with scaled pixels of the depth image.
		for row in range(self.height):
			for col in range(self.width):

				scaled_value = 256 * (self.image[row][col] - minimum) / (maximum - minimum)
				
				greyscale.image[row][3*col - 1] = scaled_value
				greyscale.image[row][3*col] = scaled_value
				greyscale.image[row][3*col + 1] = scaled_value

		greyscale.write_to_file(filename)
