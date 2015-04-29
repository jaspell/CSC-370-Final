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
	color_file = os.path.expanduser("~/Desktop/Images/KinectColor/img_0000.png")

	test_file = "test.png"

	#image = color_image.ColorImage(color_file)
	#image = color_image.ColorImage(w=20, h=100)

	#image = depth_image.DepthImage(depth_file)

	#print len(image.image[0])

	#blur(color_image.ColorImage(color_file),10)
	
	final = edge_detect(color_file,10)
	
	final.write_to_file(test_file)

def edge_detect(image_file, filter_radius):
	blurred_image = blur(color_image.ColorImage(image_file),10)
	final_image = color_image.ColorImage(width=blurred_image.width, height=blurred_image.height)
	original_image = color_image.ColorImage(image_file)
	
	blurred_image.write_to_file("blurred.png")
	original_image.write_to_file("original.png")
	
	#subtract original image from the blurred image
	for j, row in enumerate(blurred_image.image):
		#make sure we are not at the boundary
		if j > filter_radius and j < (len(blurred_image.image)-filter_radius):
			newRed, newGreen, newBlue = 0,0,0
			for i,col in enumerate(row):
				if i > filter_radius and i < (len(row)-filter_radius):
					newRed = max((blurred_image.image[j][i][0]-original_image.image[j][i][0])*10,0)
					newGreen = max((blurred_image.image[j][i][1]-original_image.image[j][i][1])*10,0)
					newBlue = max((blurred_image.image[j][i][2]-original_image.image[j][i][2])*10,0)
			final_image.image[j][i]=(min(newRed,255), min(newGreen,255), min(newBlue,255))		
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

def laplacian_segment(image):
	"""
	Segment the depth image using the Laplacian technique.

	Parameters:
		image - DepthImage - depth image to be segmented

	Returns:
		list of lists of tuples - segmented regions
	"""
	pass

def blur(image_original, radius):
	"""
	Blur image according to given radius.

	Parameters:
		image_original - ColorImage - original image
		radius - int - radius around each pixel to blur

	Returns:
		ColorImage - blurred image
	"""

	image = image_original.image

	total = get_total_for_filter(radius)    
	
	normFactor = 1.0/total
	filt = make_filter(radius, normFactor)
	
	blurred = one_dimensional_blur(image_original, radius, filt, "horizontal")  

	final_blurred= one_dimensional_blur(blurred, radius, filt, "vertical")

	
	#final_blurred.write_to_file("test.png")         
	return final_blurred

def one_dimensional_blur(image_original, radius, filt, blur_mode):
	blurred = color_image.ColorImage(width=image_original.width, height=image_original.height)
	image = image_original.image
	
	for j, row in enumerate(image):
		#make sure we are not at the boundary
		if j > radius and j < (len(image)-radius):
			for i,col in enumerate(row):
				if i > radius and i < (len(row)-radius):
					newRed, newGreen, newBlue = 0,0,0
					for k in range(-radius+1, radius): #Now go through filter and apply blur horizontally
						if blur_mode == "horizontal":
							newRed = newRed + image[j][i+k][0]*filt[k+radius]
							newGreen = newGreen + image[j][i+k][1]*filt[k+radius]
							newBlue = newBlue + image[j][i+k][2]*filt[k+radius]
						elif blur_mode == "vertical":
							newRed = newRed + image[j+k][i][0]*filt[k+radius]
							newGreen = newGreen + image[j+k][i][1]*filt[k+radius]
							newBlue = newBlue + image[j+k][i][2]*filt[k+radius]       
						else:
							print "ERROR HAS OCCURED. Expected 'horizontal' or 'verticle' for blur mode but received ", blur_mode
					#make new pixel as a tuple to be inserted.    
					pixel = (int(newRed), int(newGreen), int(newBlue))
					blurred.image[j][i] = pixel
	return blurred

def get_total_for_filter(radius):

	total = 0

	sigma = (radius - 1) / 3.0

	for i in range(2*radius + 1):

		x = i - radius
		val = 1.0 / (sigma * math.sqrt(2.0 * math.pi)) * pow(math.e, (-pow(x, 2)
															 / (2.0 * pow(sigma, 2))))
		total += val

	return total

def make_filter(radius, normFactor):

	filt = []

	sigma = (radius - 1) / 3.0

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