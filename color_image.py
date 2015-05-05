#!/usr/bin/env python

"""Color image object for Final Project (Depth Image segmentation)."""

import png

__author__ = "Micah Brown and Jackson Spell"
__email__ = "msbrown@davidson.edu, jaspell@davidson.edu"

class ColorImage(object):
	"""
	Color image object.
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

			self.image = [[(0, 0, 0) for j in range(self.width)] for i in range(self.height)]
			
	def __getitem__(self, key):
		"""
		[] getter operator overload.
		
		Parameters:
		key - int - the index of the image list
		
		Returns:
		the list at index = key of the image.
		"""

		return self.image[key]	

	def read_image(self, image_file):
		"""
		Read in image from PNG file.

		Parameters:
			image_file - string - path to file containing PNG image

		Returns:
			width, height, image as 2D array of tuples
		"""

		with open(image_file, 'r') as inf:

			reader = png.Reader(file=inf)

			width, height, pixels, metadata = reader.read()

			# Read pixels into internal image storage
			image = []
			
			for line in pixels:
				
				row = []
				for i in range(width):
					row.append((line[3*i], line[3*i + 1], line[3*i + 2]))
				image.append(row)

		return width, height, image

	def write_to_file(self, filename):
		"""
		Write image to file.

		Parameters:
			filename - string - path to file

		Returns:
			None
		"""

		# Write output to file.
		with open(filename, 'wb') as outf:
			writer = png.Writer(self.width, self.height)

			# Convert image from tuples to list format.
			pic = []
			for line in self.image:
				row = []
				for tup in line:
					for i in range(3):
						row.append(tup[i])
				pic.append(row)

			writer.write(outf, pic)

