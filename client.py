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

verbose = True

def main():

	depth_file = os.path.expanduser("~/Desktop/Images/DepthData/img_0331.yml")
	color_file = os.path.expanduser("~/Desktop/Images/KinectColor/img_0331.png")
	blackwhite_file = os.path.expanduser("~/Desktop/Images/RegisteredDepthData/img_0000_abs.png")

	depth_test_file = "depth_test.png"
	color_test_file = "color_test.png"

	#original = color_image.ColorImage(color_file)
	#original = color_image.ColorImage(width=20, height=100)

	original = depth_image.DepthImage(depth_file)
	color = color_image.ColorImage(color_file)
	# original.write_to_file("original.png")
	# blurred = blur(original, 10)
	# blurred.write_to_file("blur.png")

	#print len(original.image[0])


	depth_threshold = 5
	color_threshold = 10
	radius = 8

	scale = 20
	border = 25
	
	laplacian_segment(color, color_threshold, radius, scale, border).write_to_file(color_test_file)
	laplacian_segment(original, depth_threshold, radius, scale, border).write_to_file(depth_test_file)


	if verbose:
		print "Done."

def gradient_segment(original, threshold):
	"""
	Segment the depth image using the gradient technique.

	Parameters:
		original - DepthImage - depth image to be segmented
		threshold - float - maximum angle between two pixels in the same region

	Returns:
		list of lists of tuples - segmented regions
	"""

	added = [[False for j in range(width)] for i in range(height)]

	# Calculate normal vector for each pixel.
	normals = [[(0.0,0.0) for j in range(width)] for i in range(height)]
	# CALCULATE NORMALS.  HOW DO WE DO IT?!?!?!
	for i in range(1, original.height-1):
		for j in range(1, original.width-1):
			theta = math.atan((original[i][j+1]-original[i][j-1])/2)
			phi = math.atan((original[i+1][j]-original[i-1][j])/2)
			
			normals[i][j] = (theta, phi)
	
	


	for i in range(original.height):
		for j in range(original.width):
			if not added[i][j]:
				regions.append(group_region(added, i, j, normals, threshold))

	return regions

def laplacian_segment(original, threshold, radius, scale, border):
	"""
	Segment the depth image using the Laplacian technique.

	Parameters:
		original - ColorImage or DepthImage - image to be segmented
		threshold - int - 0 <= threshold < 256 - minimum value of edge between regions
		radius - int - radius of blurring filter
		scale - int - scaling factor for subtraction
		border - int - > 0 - width of non-region border

	Returns:
		list of lists of tuples - segmented regions
	"""

	if verbose: 
		print "Performing Laplacian segment..."

	color = type(original) is color_image.ColorImage 

	edged = edge_detect(original, radius, scale)
	edged.write_to_file("edged_no_blur.png")
	
	edged = blur(edged, 3) 

	edged.write_to_file("edged_blurred.png")
	edged
					
	# Create 2D boolean array, setting borders and detected edges to True.
	if color:
		added = [[True if (edged[i][j][0]+edged[i][j][1]+edged[i][j][2])/3.0 > threshold 
					   or i <= border - 1
					   or i >= original.height - border
					   or j <= border - 1
					   or j >= original.width - border
					   else False for j in range(original.width)] for i in range(original.height)]

	else:
		added = [[True if edged[i][j] > threshold 
					   or i <= border - 1
					   or i >= original.height - border
					   or j <= border - 1
					   or j >= original.width - border
					   else False for j in range(original.width)] for i in range(original.height)]

	if verbose:
		print "Grouping regions..."

	regions = []

	for i in range(original.height):
		for j in range(original.width):
			if not added[i][j]:
				regions.append(group_region(added, i, j))

	return create_segmented_image(regions, original.width, original.height)

def angle_between(normal1, normal2):
	"""
	Find the angle between the given normals.

	Parameters:
		normal1 - (float, float)
	"""
	

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

	if verbose:
		print "Coloring segmented image..."

	segmented = color_image.ColorImage(width=width, height=height) 
	
	for region in regions:

		# Pick a random color for that entire region.
		rgb = (randint(0,255), randint(0,255), randint(0,255))

		# Set every pixel in the region to that color.
		for coord_tuple in region:

			segmented[coord_tuple[0]][coord_tuple[1]] = rgb
														  
	return segmented

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

	if verbose:
		print "Determining edges..."

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

def group_region(added, i, j, normals=None, threshold=None):
	"""
	Group pixels into a region via floodfill for Laplacian segmentation.

	Parameters:
		added - 2D boolean array - whether the pixel at i,j has been added to a region
		i - int - height coordinate of starting pixel
		j - int - width coordinate of starting pixel
		normals - 2D float array - normal vector at pixel

	Returns:
		list of tuples - list of coordinate pairs for pixels in the region
	"""

	region = []
	q = Queue.Queue()

	# Start with the starting pixel in the queue
	q.put((i, j))

	while not q.empty():
		x, y = q.get()

		if normals:
			# Add edge-adjacent neighbors to the region if don't differ in normal too much.
			for i in range(-1, 2):

				if not added[x][y+i] and angle_between(normals[x][y], normals[x][y+i]) < threshold:
					continue

				if not added[x+i][y] and angle_between(normals[x][y], normals[x+i][y]) < threshold:
					continue
		else:
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