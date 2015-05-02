#!/usr/bin/env python

"""Depth Image object for Final Project (Depth Image Segmentation)."""

import sys

import png


__author__ = "Micah Brown and Jackson Spell"
__email__ = "msbrown@davidson.edu, jaspell@davidson.edu"

class DepthImage(object):
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

			# Skip first 2 lines.
			for i in range(2):
				inf.readline()

			# Read in width and height.
			width = int(inf.readline()[10:])
			height = int(inf.readline()[11:])
			image = []

			# Skip next 3 lines.
			for i in range(3):
				inf.readline()

			# Read in data.
			tokens = inf.readline().split()
			curr = 0

			for row in range(height):

				line = []

				for col in range(width):

					#print row, col, curr, tokens

					# If end of tokens is reached, read new line.
					if curr == len(tokens):
						tokens = inf.readline().split()
						curr = 0

					#print tokens, tokens[curr], row, col

					# Keep reading until a number is found.
					while tokens[curr][-1] not in  [',', '.']:

						curr += 1

						# If end of tokens is reached, read new line.
						if curr == len(tokens):
							tokens = inf.readline().split()
							curr = 0

						#print tokens, tokens[curr], row, col

					# Cut the comma off the number and append to row.
					line.append(int(float(tokens[curr][:-1])))
					#print tokens[curr][:-1]
					curr += 1

				# Append line to image.
				image.append(line)

		return width, height, image

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

		print maximum, minimum

		greyscale = [[0 for j in range(self.width)] for i in range(self.height)]

		# Replace pixels in the color image with scaled pixels of the depth image.
		for row in range(self.height):
			for col in range(self.width):

				greyscale[row][col] = 255 * (self.image[row][col] - minimum) / (maximum - minimum) 

		with open(filename, 'wb') as outf:
			writer = png.Writer(self.width, self.height, greyscale=True)
			writer.write(outf, greyscale)
