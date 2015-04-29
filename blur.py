import color_image
import math
import os


def blur(image_original, radius):
    image = image_original.image
    #first, make the filter.
    filt = []
    for i in range(0,radius*2+1): 
        filt.extend(str(0)) 

    sigma = (float(radius) - 1.0)/3.0

    total = get_total_for_filter(filt, sigma, radius)    
    
    normFactor = 1.0/total
    filt = make_filter(filt, sigma, radius, normFactor)
    
    blurred = one_dimensional_blur(image_original, radius, filt, "horizontal")  
    blurred.write_to_file("horizontal.png")
    final_blurred= one_dimensional_blur(blurred, radius, filt, "vertical")

    
    final_blurred.write_to_file("test.png")         
   

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
                            print "ERROR HAS OCCURED. Expected 'horizontal' or 'vertical' for blur mode but received ", blur_mode
                    #make new pixel as a tuple to be inserted.    
                    pixel = (int(newRed), int(newGreen), int(newBlue))
                    blurred.image[j][i] = pixel
    return blurred

def get_total_for_filter(filt, sigma, radius):
    PI, E = 3.14159265, 2.718281828
    total = 0
    for i,init_val in enumerate(filt):
        x = int(i)-radius
        val = 1.0/(sigma*math.sqrt(2.0*PI))*pow(E,(-pow(x,2)/(2.0*pow(sigma,2))))
        total+= val
    return total

def make_filter(filt, sigma, radius, normFactor):
    PI, E = 3.14159265, 2.718281828
    for i,init_val in enumerate(filt):
            x = int(i)-radius
            val = 1.0/(sigma*math.sqrt(2.0*PI))*pow(E,(-pow(x,2)/(2.0*pow(sigma,2))))
            filt[int(i)]=val*normFactor   
    return filt
    
    
depth_file = os.path.expanduser("~/Desktop/letters.png")
blur(color_image.ColorImage(depth_file),10)

    
