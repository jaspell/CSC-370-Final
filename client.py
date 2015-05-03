#!/usr/bin/env python

"""Client code for Final Project (Depth Image Segmentation)."""

import os
import math
from random import randint
import Queue

import color_image
import depth_image

__author__ = "Micah Brown and Jackson Spell"
__email__ = "msbrown@davidson.edu, jaspell@davidson.edu"

def main():

	depth_file = os.path.expanduser("~/Desktop/Images/DepthData/img_0005.yml")
	color_file = os.path.expanduser("~/Desktop/Images/KinectColor/img_0004.png")
	blackwhite_file = os.path.expanduser("~/Desktop/Images/RegisteredDepthData/img_0005_abs.png")

	test_file = "test1.png"

	#original = color_image.ColorImage(color_file)
	#original = color_image.ColorImage(width=20, height=100)

	original = depth_image.DepthImage(depth_file)
	original.write_to_file("original.png")
	blurred = blur(original, 10)
	blurred.write_to_file("blur.png")

	#print len(original.image[0])
	
	laplacian_segment(original, 200, 10, 20).write_to_file(test_file)

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

def laplacian_segment(original, threshold, radius, scale):
	"""
	Segment the depth image using the Laplacian technique.

	Parameters:
		original - ColorImage or DepthImage - image to be segmented
		threshold - int - 0 <= threshold < 256 - minimum value of edge between regions
		radius - int - radius of blurring filter
		scale - int - scaling factor for subtraction

	Returns:
		list of lists of tuples - segmented regions
	"""

	edged = edge_detect(original, radius, scale)
					
	# Create 2D boolean array, setting borders and detected edges to True.
	added = [[True if edged[i][j] > threshold 
				   or i == 0 
				   or i == original.height - 1 
				   or j == 0 
				   or j == original.width - 1 
				   else False for j in range(original.width)] for i in range(original.height)]

	regions = []

	for i in range(original.height):
		for j in range(original.width):
			if not added[i][j]:
				regions.append(group_region(added, i, j))

	return create_segmented_image(regions, original.width, original.height)

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

				segmented_image[coord_tuple[1]][3*coord_tuple[0]+i] = rgb[i]
														  
	return segmented_image

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
	
	blurred = blur(original, radius)

	# Subtract original image from blurred to locate edges.
	for j in range(radius, original.height - radius):
		for i in range(radius, original.width - radius):

			# Construct a pixel from the original and blurred pictures.
			if color:
				red = max((blurred[j][i][0] - original[j][i][0]) * scale, 0)
				green = max((blurred[j][i][1] - original[j][i][1]) * scale, 0)
				blue = max((blurred[j][i][2] - original[j][i][2]) * scale, 0)
				
				pixel = (min(red, 255), min(green, 255), min(blue, 255))			

			else:
				pixel = min(max((blurred[j][i] - original[j][i]) * scale, 0), 255)
			
			# Add the pixel to the final image.
			final[j][i] = pixel
			
	return final

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

def group_region(added, i, j):
	"""
	Group pixels into a region via floodfill for Laplacian segmentation.

	Parameters:
		added - 2D boolean list - whether the pixel at i,j has been added to a region
		i - int - height coordinate of starting pixel
		j - int - width coordinate of starting pixel

	Returns:
		list of tuples - list of coordinate pairs for pixels in the region
	"""

	region = []
	q = Queue.Queue()

	# Start with the starting pixel in the queue
	q.put((i, j))

	while not q.empty():
		x, y = q.get()

		# Add edge-adjacent neighbors to the region if they have not been added.
		for i in range(-1, 2):

			if not added[x][y+i]:
				q.put((x, y+i))
				added[x][y+i] = True
				region.append((x, y+i))

			if not added[x+i][y]:
				q.put((x+i, y))
				added[x+i][y] = True
				region.append((x+i, y))

	return region

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
						red += original[j][i+k][0] * filt[k+radius]
						green += original[j][i+k][1] * filt[k+radius]
						blue += original[j][i+k][2] * filt[k+radius]

					else:
						pixel += original[j][i+k] * filt[k+radius]
						
				elif blur_mode == "vertical":
					if color:
						red += original[j+k][i][0] * filt[k+radius]
						green += original[j+k][i][1] * filt[k+radius]
						blue += original[j+k][i][2] * filt[k+radius]  

					else:
						pixel += original[j+k][i] * filt[k+radius]

				else:
					print ("ERROR HAS OCCURED. Expected 'horizontal' or 'vertical' for blur mode "
						   "but received "), blur_mode
					exit()

			# Make new pixel an appropriate type for the image given.    
			if color:
				pixel = (int(red), int(green), int(blue))

			else:
				pixel = int(pixel)

			blurred[j][i] = pixel

	return blurred

if __name__ == "__main__":
	main()