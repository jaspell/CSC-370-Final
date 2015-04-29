import color_image
import math
import os

def PI():
    return 3.1415
def E():
    return float(2.71)

def blur(imageOriginal, radius):
    image = imageOriginal.image
    #first, make the filter.
    filt = []
    for i in range(0,radius*2+1): 
        filt.extend(str(0)) 

    sigma = (float(radius) - 1.0)/3.0

    total = get_total_for_filter(filt, sigma, radius)    
    
    normFactor = 1.0/total
    print filt
    filt = make_filter(filt, sigma, radius, normFactor)
    #print image
    print filt
    blurred = color_image.ColorImage(width=imageOriginal.width, height=imageOriginal.height)
    for j, row in enumerate(image):
        #make sure we are not at the boundary
        if j > radius and j < (len(image)-radius):
            for i,col in enumerate(row):
                if i > radius and i < (len(row)-radius):
                    newRed, newGreen, newBlue = 0,0,0
                    #TODO: for r, g, b:
                    for k in range(-radius+1, radius): #Now go through filter and apply blur horizontally
                        newRed = newRed + image[j][i+k][0]*filt[k+radius]
                        newGreen = newGreen + image[j][i+k][1]*filt[k+radius]
                        newBlue = newBlue + image[j][i+k][2]*filt[k+radius]
                    #make new pixel to be inserted.    
                    pixel = (int(newRed), int(newGreen), int(newBlue))
                    blurred.image[j][i] = pixel
    blurred.write_to_file("test.png")            

        
    #print filter
    
    
    
    

def get_total_for_filter(filt, sigma, radius):
    total = 0
    for i,init_val in enumerate(filt):
        x = int(i)-radius
        val = 1.0/(sigma*math.sqrt(2.0*3.1415))*pow(2.71,(-pow(x,2)/(2.0*pow(sigma,2))))
        total+= val
    return total

def make_filter(filt, sigma, radius, normFactor):
    for i,init_val in enumerate(filt):
            x = int(i)-radius
            val = 1.0/(sigma*math.sqrt(2.0*3.1415))*pow(2.71,(-pow(x,2)/(2.0*pow(sigma,2))))
            filt[int(i)]=val*normFactor   
    return filt
    
    
depth_file = os.path.expanduser("~/Desktop/letters.png")
blur(color_image.ColorImage(depth_file),20)

    
