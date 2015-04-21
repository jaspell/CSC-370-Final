#!/usr/bin/env python

"""Image base object for Final Project (Depth Image segmentation)."""

__author__ = "Micah Brown and Jackson Spell"
__email__ = "msbrown@davidson.edu, jaspell@davidson.edu"

class Image:
	"""
	Image object.
	"""

	def __init__(image_file=None, w=None, h=None):
		"""
		Image Constructor.

		Parameters:
			None

		Returns:
			instantiated Image
		"""

		if image_file is not None:
			self.width, self.height, self.image = read_image(image_file)

		else:
			self.width = w
			self.height = h

			self.image = [[0 for j in range(self.height)] for i in range(self.width)]

	def read_image(image_file):
		"""
		Read in image.

		Parameters:
			image_file - string - path to image

		Returns:
			width, height, image as 2D array 
		"""

		with open(image_file, 'r') as inf:

			# Skip first 2 lines.
			for i in range(2):
				inf.readline()

			# Read in width and height.
			width = int(inf.readline[10:])
			height = int(inf.readline[11:])

			# Skip next 3 lines.
			for i in range(3):
				inf.readline()

			# Read in the data.