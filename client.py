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

	depth_file = os.path.expanduser("~/Desktop/Images/DepthData/img_0000.yml")
	color_file = os.path.expanduser("~/Desktop/Images/KinectColor/img_0004.png")
	blackwhite_file = os.path.expanduser("~/Desktop/Images/RegisteredDepthData/img_0003_abs.png")

	test_file = "test.png"

	#image = color_image.ColorImage(color_file)
	#image = color_image.ColorImage(w=20, h=100)

	#image = depth_image.DepthImage(depth_file)

	#print len(image.image[0])

	#blur(color_image.ColorImage(color_file),10)
	
	color = True
	
	final = edge_detect(color_file,10, color)
	
	final.write_to_file(test_file)

def edge_detect(image_file, filter_radius, color):
	original_image = color_image.ColorImage(image_file)
	print "here"
	blurred_image = blur(original_image,filter_radius, color)
	final_image = color_image.ColorImage(width=blurred_image.width, height=blurred_image.height)
	
	blurred_image.write_to_file("blurred.png")
	original_image.write_to_file("original.png")
	
	
	for j in range(filter_radius, original_image.height - filter_radius):
		for i in range(filter_radius, original_image.width - filter_radius):
			if(color):
				newRed = max((blurred_image.image[j][i][0]-original_image.image[j][i][0])*2,0)
				newGreen = max((blurred_image.image[j][i][1]-original_image.image[j][i][1])*2,0)
				newBlue = max((blurred_image.image[j][i][2]-original_image.image[j][i][2])*2,0)
				
				pixel = (min(newRed,255), min(newGreen,255), min(newBlue,255))				
			else:
				pixel = min(max((blurred_image.image[j][i][0]-original_image.image[j][i][0])*2,0),255)
			
			final_image.image[j][i]=pixel
			
	return final_image
	

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

def blur(image, radius, color):
	"""
	Blur image according to given radius.

	Parameters:
		image - ColorImage - original image
		radius - int - radius around each pixel to blur

	Returns:
		ColorImage - blurred image
	"""

	filt = make_filter(radius)
		
	blurred = one_dimensional_blur(image, radius, filt, "horizontal", color)  
	blurred = one_dimensional_blur(blurred, radius, filt, "vertical", color)

	return blurred

def one_dimensional_blur(original, radius, filt, blur_mode, color):
	"""
	Blur image in given direction.

	Parameters:
		original - ColorImage - original image
		radius - int - radius around each pixel to blur
		filt - list of floats - blur filter
		blur_mode - string - "horizontal" or "vertical" - direction in which to blur

	Returns:
		ColorImage - image blurred in given direction
	"""
	
	blurred = color_image.ColorImage(width=original.width, height=original.height)
	
	# Make sure we are not at the boundary.
	for j in range(radius, original.height - radius):
		for i in range(radius, original.width - radius):

			newRed, newGreen, newBlue = 0, 0, 0

			# Go through filter and apply blur in the given direction.
			for k in range(-radius + 1, radius): 

				if blur_mode == "horizontal":
					if(color):
						newRed += original.image[j][i+k][0] * filt[k+radius]
						newGreen += original.image[j][i+k][1] * filt[k+radius]
						newBlue += original.image[j][i+k][2] * filt[k+radius]
					else:
						pixel += original.image[j][i+k] * filt[k+radius]
						
				elif blur_mode == "vertical":
					if(color):
						newRed += original.image[j+k][i][0] * filt[k+radius]
						newGreen += original.image[j+k][i][1] * filt[k+radius]
						newBlue += original.image[j+k][i][2] * filt[k+radius]    
					else:
						pixel += original.image[j+k][i] * filt[k+radius]
				else:
					print "ERROR HAS OCCURED. Expected 'horizontal' or 'vertical' for blur mode but received ", blur_mode
					exit()

			# Make new pixel as a tuple to be inserted.    
			if(color):
				pixel = (int(newRed), int(newGreen), int(newBlue))
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

def gradient_segment(image, threshold):
	"""
	Segment the depth image using the gradient technique.

	Parameters:
		image - DepthImage - depth image to be segmented
		threshold - float - maximum angle between two pixels in the same region

	Returns:
		list of lists of tuples - segmented regions
	"""

	pass

if __name__ == "__main__":
	main()