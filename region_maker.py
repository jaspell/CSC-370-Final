#Input: List of List of Tuples (x_coord, y_coord).
#Output: for each List of Tuples, set them all to the same color
import color_image
from random import randint

def create_segmented_image(regions, width, height):
    segmented_image = color_image.ColorImage(w=width, h=height) 
    print segmented_image
    
    for region in regions:
        #pick a random color for that entire region
        rgb = [randint(0,255),randint(0,255),randint(0,255)]
        for coord_tuple in region:
            for i in range(0,3): #Now go through and change the R, G, and B vals.
                segmented_image.image[coord_tuple[1]][3*coord_tuple[0]+i] = rgb[i]
                                                          
    return segemented_image                                                    
                                                          
                                                          
            
image1 = color_image.ColorImage(w=4, height=6)

image1 = create_segmented_image([[(1,1),(1,2),(1,3)],[(2,1),(2,2),(2,3)],[(3,1),(3,2),(3,3)]], 4, 6)
