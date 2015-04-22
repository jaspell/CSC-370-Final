#!/usr/bin/env python

"""Color image object for Final Project (Depth Image segmentation)."""

import pixel

import png

__author__ = "Micah Brown and Jackson Spell"
__email__ = "msbrown@davidson.edu, jaspell@davidson.edu"

class ColorImage:
	"""
	Color image object.
	"""

	def __init__(image_file=None, w=None, h=None):
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
			self.width, self.height, self.image = read_image(image_file)

		else:
			self.width = w
			self.height = h

			self.image = [[pixel.Pixel(0, 0, 0) for j in range(self.width)]
							for i in range(self.height)]

	def read_image(image_file):
		"""
		Read in image from PNG file.

		Parameters:
			image_file - string - path to file containing PNG image

		Returns:
			width, height, image as 2D array of Pixels 
		"""

		with open(image_file, 'r') as inf:

			reader = png.Reader(file=inf)

			width, height, pixels, metadata = reader.read()

			# Read pixels into internal image storage
			image = []

			for line in pixels:
				row = []
				for i in range(width):
					row.append(pixel.Pixel(line[i], line[i+1], line[i+2]))
				image.append(row)

		return width, height, image

	def write_to_file(filename):
		"""
		Write image to file.

		Parameters:
			filename - string - path to file

		Returns:
			None
		"""

		output = []

		# Convert image to a list of lists of ints
		for line in self.image:
			row = []
			for pix in row:
				row.append(pix.to_list())
			output.append(row)

		# Write output to file.
		with open(filename, 'wb') as outf:
			writer = png.Writer(self.width, self.height)
			writer.write(outf, output)

