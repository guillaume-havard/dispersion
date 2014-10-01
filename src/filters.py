 #! /usr/bin/python3

"""
"""

from dispersion import *
import pygame

# vont prendre des levels (liste(liste(int[0, 255])) pour le moment

def blur_average(levels, matrix):
    """
    matrix = matrix size pour le moment
    """
    
    
    
def blur_median(levels, matrix):
    """
    matrix = matrix size pour le moment
    """
    win = matrix//2
    
    res = []
    
    for x in range(len(levels)):
        res.append([])
        for y in range(len(levels[x])):            
            res[x].append(0)
            if not win <= x < len(levels) - win:
                continue       
            if not win <= y < len(levels[0]) - win:
                continue
                
            buff = []    
            for i in range(-win, win +1):
                for j in range(-win, win +1):
                    buff.append(levels[x+i][y+j])
            
            buff.sort()

            res[x][y] = buff[(matrix*matrix) // 2]
            
            if res[x][y] == 0:
                print(buff)
            
    return res
            
            
if __name__ == "__main__":
    
    pygame.init() 
               
    image = pygame.image.load('census_hue_w15-15_0-0.bmp')     
    levels = image_to_levels(image, hue_level)
    
    median = blur_median(levels, 9)
    
    im_result = levels_to_image(median, level_to_color)
    pygame.image.save(im_result, "median.bmp")
    
    
    
    
            
