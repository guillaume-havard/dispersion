 #! /usr/bin/python3

"""
Quelques filtres de flou.

"""

from dispersion import *
import pygame

# vont prendre des levels (liste(liste(int[0, 255])) pour le moment

def blur_average(levels, matrix):
    """
    levels [in] : liste(liste(Int)) : image en niveau
    matrix [in] : matrix size (pour le moment)
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
                
            somme = 0    
            for i in range(-win, win +1):
                for j in range(-win, win +1):
                    somme += levels[x+i][y+j]
            
            res[x][y] = somme // (matrix*matrix)
            
            
    return res
    
    
def blur_median(levels, matrix):
    """
    levels [in] : liste(liste(Int)) : image en niveau
    matrix [in] : matrix size (pour le moment)
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
    """           
    image = pygame.image.load('census_hue_w15-15_0-0.bmp')     
    levels = image_to_levels(image, grey_level)
    
    median = blur_median(levels, 9)
    
    im_result = levels_to_image(median, level_to_color)
    pygame.image.save(im_result, "median.bmp")
    
    ""
    
    image = pygame.image.load('r.bmp')     
    levels = image_to_levels(image, grey_level)
           
    levels = blur_average(levels, 3)
    
    im_result = levels_to_image(levels, level_to_grey)
    pygame.image.save(im_result, "r-av3.bmp")
    """
        
        
    #images to grey
    """
    image = pygame.image.load('im2.ppm')     
    levels = image_to_levels(image, grey_level)   
    levels = blur_median(levels, 3)
    im_result = levels_to_image(levels, level_to_grey)
    pygame.image.save(im_result, "im2-med3.bmp")
    
    image = pygame.image.load('im6.ppm')     
    levels = image_to_levels(image, grey_level)  
    levels = blur_median(levels, 3) 
    im_result = levels_to_image(levels, level_to_grey)
    pygame.image.save(im_result, "im6-med3.bmp")
    """
    
    image = pygame.image.load('l_pingouin.bmp')     
    levels = image_to_levels(image, grey_level)  
    
    res = []
    
    for x in range(len(levels)):
        res.append([])
        for y in range(len(levels[x])):            
            res[x].append(0)
            
            if 211 <= levels[x][y] <= 255 or 0 <= levels[x][y] <= 44 or 84 <= levels[x][y] <= 171:
                res[x][y] = levels[x][y]
            
    
    im_result = levels_to_image(res, level_to_grey)
    pygame.image.save(im_result, "l_pingouin_-horiz_40.bmp")
    
    pygame.quit        
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
