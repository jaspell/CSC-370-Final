#!/usr/bin/env python

"""Client code for Final Project (Depth Image Segmentation)."""

import os
import math
from random import randint

import color_image
import depth_image

__author__ = "Micah Brown and Jackson Spell"
__email__ = "msbrown@davidson.edu, jaspell@davidson.edu"

def main():

	depth_file = os.path.expanduser("~/Desktop/Images/DepthData/img_0005.yml")
	color_file = os.path.expanduser("~/Desktop/Images/KinectColor/img_0004.png")
	blackwhite_file = os.path.expanduser("~/Desktop/Images/RegisteredDepthData/img_0005_abs.png")

	test_file = "test.png"

	#original = color_image.ColorImage(color_file)
	#original = color_image.ColorImage(width=20, height=100)

	original = depth_image.DepthImage(depth_file)
	original.write_to_file("original.png")
	blurred = blur(original, 10)
	blurred.write_to_file("blur.png")

	#print len(original.image[0])

	#blur(color_image.ColorImage(color_file), 10)
	
	#final = edge_detect(original,10)

	final = edge_detect(original, 10)
	
	final.write_to_file(test_file)

def edge_detect(original, radius, scale):
	"""
	Create an edge-detected ColorImage or DepthImage.

	Parameters:
		original - ColorImage or DepthImage - original image
		radius - int - radius of blurring filter
		scale - int - scaling factor for subtraction

	Returns:
		ColorImage or DepthImage - edge-detected image
	"""

	color = type(original) is color_image.ColorImage

	if color:
		final = color_image.ColorImage(width=original.width, height=original.height)
	else:
		final = depth_image.DepthImage(width=original.width, height=original.height)
	
	blurred = blur(original, radius, color)
	
	# Subtract original image from blurred to locate edges.
	for j in range(radius, original.height - radius):
		for i in range(radius, original.width - radius):

			# Construct a pixel from the original and blurred pictures.
			if color:
				red = max((blurred.image[j][i][0] - original.image[j][i][0]) * scale, 0)
				green = max((blurred.image[j][i][1] - original.image[j][i][1]) * scale, 0)
				blue = max((blurred.image[j][i][2] - original.image[j][i][2]) * scale, 0)
				
				pixel = (min(red, 255), min(green, 255), min(blue, 255))			

			else:
				pixel = min(max((blurred.image[j][i] - original.image[j][i]) * scale, 0), 255)
			
			# Add the pixel to the final image.
			final.image[j][i] = pixel
			
	return final

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

def laplacian_segment(image, threshold):
	"""
	Segment the depth image using the Laplacian technique.

	Parameters:
		image - DepthImage - depth image to be segmented
		threshold - int - 0 <= threshold < 256 - minimum value of edge between regions

	Returns:
		list of lists of tuples - segmented regions
	"""
	
	pass

	#subtracted

	# Track the pixels that have been grouped.
	#grouped = [[False for i in range(width)] for j in range(height)]

	#while 

def blur(original, radius):
	"""
	Blur image according to given radius.

	Parameters:
		original - ColorImage or DepthImage - original image
		radius - int - radius around each pixel to blur
		blur - bool - switch so that we can blur color and B&W images.

	Returns:
		ColorImage - blurred image
	"""

	filt = make_filter(radius)
		
	blurred = one_dimensional_blur(original, radius, filt, "horizontal")  
	blurred = one_dimensional_blur(blurred, radius, filt, "vertical")

	return blurred

def one_dimensional_blur(original, radius, filt, blur_mode):
	"""
	Blur image in given direction.

	Parameters:
		original - ColorImage or DepthImage - original image
		radius - int - radius around each pixel to blur
		filt - list of floats - blur filter
		blur_mode - string - "horizontal" or "vertical" - direction in which to blur

	Returns:
		ColorImage or DepthImage- image blurred in given direction
	"""

	color = type(original) is color_image.ColorImage

	if color:
		blurred = color_image.ColorImage(width=original.width, height=original.height)
	else:
		blurred = depth_image.DepthImage(width=original.width, height=original.height)

	# Make sure we are not at the boundary.
	for j in range(radius, original.height - radius):
		for i in range(radius, original.width - radius):

			red, green, blue = 0, 0, 0
			pixel = 0
			
			# Go through filter and apply blur in the given direction.
			for k in range(1 - radius, radius): 

				if blur_mode == "horizontal":
					if color:
						red += original.image[j][i+k][0] * filt[k+radius]
						green += original.image[j][i+k][1] * filt[k+radius]
						blue += original.image[j][i+k][2] * filt[k+radius]

					else:
						pixel += original.image[j][i+k] * filt[k+radius]
						
				elif blur_mode == "vertical":
					if color:
						red += original.image[j+k][i][0] * filt[k+radius]
						green += original.image[j+k][i][1] * filt[k+radius]
						blue += original.image[j+k][i][2] * filt[k+radius]  

					else:
						#print original.image[j+k][i]
						pixel += original.image[j+k][i] * filt[k+radius]

				else:
					print ("ERROR HAS OCCURED. Expected 'horizontal' or 'vertical' for blur mode "
						   "but received "), blur_mode
					exit()

			# Make new pixel an appropriate type for the image given.    
			if color:
				pixel = (int(red), int(green), int(blue))

			else:
				pixel = int(pixel)

			blurred.image[j][i] = pixel

	return blurred

def get_total_for_filter(radius):
	"""
	Determine the filter's total.

	Parameters:
		radius - int - radius around each pixel to blur

	Returns:
		int - filter's total
	"""

	total = 0

	sigma = (radius - 1) / 3.0

	for i in range(2*radius + 1):

		x = i - radius
		val = 1.0 / (sigma * math.sqrt(2.0 * math.pi)) * pow(math.e, (-pow(x, 2)
															 / (2.0 * pow(sigma, 2))))
		total += val

	return total

def make_filter(radius):
	"""
	Make the filter for the blur.

	Parameters:
		radius - int - radius around each pixel to blur

	Returns:
		list of floats - blur filter
	"""

	filt = []

	sigma = (radius - 1) / 3.0
	normFactor = 1.0 / get_total_for_filter(radius)

	for i in range(2*radius + 1):

			x = i - radius
			val = 1.0 / (sigma * math.sqrt(2.0 * math.pi)) * pow(math.e, (-pow(x, 2)
																 / (2.0 * pow(sigma, 2))))
			filt.append(val * normFactor)

	return filt

def gradient_segment(original, threshold):
	"""
	Segment the depth image using the gradient technique.

	Parameters:
		original - DepthImage - depth image to be segmented
		threshold - float - maximum angle between two pixels in the same region

	Returns:
		list of lists of tuples - segmented regions
	"""

	pass

if __name__ == "__main__":
	main()