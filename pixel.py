#!/usr/bin/env python

"""Color pixel object for Final Project (Depth Image segmentation)."""

__author__ = "Micah Brown and Jackson Spell"
__email__ = "msbrown@davidson.edu, jaspell@davidson.edu"

class Pixel:
	"""
	Color pixel object.
	"""

	def __init__(red, green, blue):
		"""
		Pixel Constructor.

		Parameters:
			red - int - red value
			green - int - green value
			blue - int - blue value

		Returns:
			instantiated Pixel
		"""

		self.red = red
		self.green = green
		self.blue = blue

	def to_list():
		"""
		Return pixel in list format.

		Parameters:
			None

		Returns:
			list representing pixel [red, green, blue]
		"""

		return [self.red, self.green, self.blue]