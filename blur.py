import color_image
import math

def PI():
    return 3.1415
def E():
    return float(2.71)

def blur(image, radius):
    #first, make the filter.
    filter = []
    for i in range(0,radius*2+1): 
        filter.extend(str(i)) 

    sigma = (radius - 1.0)/3.0

    total = get_total_for_filter(filter, sigma, radius)    
    
    normFactor = 1.0/total

    filter = make_filter(filter, sigma, radius, normFactor)
    
    blurred = color_image.ColorImage(w=image.width, h=image.height)
    for i in 

        
    print filter
    
    
    
    
    
    
    
    
    
    

def get_total_for_filter(filter, sigma, radius):
    total = 0
    for i in filter:
        print int(i)
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

"""
float total = 0;
            float sigma = (r - 1.0)/3.0;
            for (int i = 0; i < r * 2 + 1; i++) {
                float x = i - r;
                float val = 1.0/(sigma*sqrt(2.0*PI))*pow(E,(-pow(x,2)/(2.0*pow(sigma, 2))));
                total += val;
            }
            float normFactor = 1.0/total;
            //now, we multiple gaus fn value by the normalizing factor.
            for (int i = 0; i < r * 2 + 1; i++) {
                float x = i - r;
                float val = 1.0/(sigma*sqrt(2.0*PI))*pow(E,(-pow(x,2)/(2.0*pow(sigma, 2))));
                filterArray[i] = val*normFactor;
            }
"""
    
