import color_image
import math

def PI():
    return 3.1415
def E():
    return float(2.71)

def blur(imageO, radius):
    image = imageO.image
    #first, make the filter.
    filter = []
    for i in range(0,radius*2+1): 
        filter.extend(str(i)) 

    sigma = (radius - 1.0)/3.0

    total = get_total_for_filter(filter, sigma, radius)    
    
    normFactor = 1.0/total

    filter = make_filter(filter, sigma, radius, normFactor)
    print image
    
    blurred = color_image.ColorImage(w=imageO.width, h=imageO.height)
    for j, row in enumerate(image):
        #make sure we are not at the boundary
        if j > radius and j < (len(image)-radius):
            for i,col in enumerate(row):
                if i > radius and i < (len(row)-radius):
                    newRed = 0
                    #TODO: for r, g, b:
                    for k in range(-radius+1, radius): #Now go through filter and apply blur horizontally
                        newRed = newRed + image[j][i+k]*filter[k+radius]
                        print k
                

        
    #print filter
    
    
    
    
    
    
    
    
    
    

def get_total_for_filter(filter, sigma, radius):
    total = 0
    for i in filter:
        x = int(i)-radius
        val = 1.0/(sigma*math.sqrt(2.0*3.1415))*pow(2.71,(-pow(x,2)/(2.0*pow(sigma,2))))
        total+= val
    return total

def make_filter(filter, sigma, radius, normFactor):
    for i in filter:
            x = int(i)-radius
            val = 1.0/(sigma*math.sqrt(2.0*3.1415))*pow(2.71,(-pow(x,2)/(2.0*pow(sigma,2))))
            filter[int(i)]=val*normFactor   
    return filter
    
blur(color_image.ColorImage(w=30, h=40),3)

    
