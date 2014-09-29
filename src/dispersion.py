 #! /usr/bin/python3

"""
/!\ La taille des images est fixe (640, 480)
"""
import sys
import pygame
from pygame.locals import *
import colorsys

class ImagesSizeDoNotMatch(Exception):
    pass

def grey_level(pix):
    """
    Convert a color into grey level
    pix [in] : int (RGB sur 24 bits) from PixelArray

    return : grey level [0, 255]
    """
    r = (pix & 0xFF0000) >> 16
    g = (pix & 0x00FF00) >> 8
    b = pix & 0x0000FF
    
    return (r+g+b) / 3

def hue_level(pix):
    """
    Convert a color into hue level
    pix [in] : int (RGB sur 24 bits) from PixelArray

    return : hue level [0, 255]
    """
    r = (pix & 0xFF0000) >> 16
    g = (pix & 0x00FF00) >> 8
    b = pix & 0x0000FF
    
    hls = colorsys.rgb_to_hls(r, g, b)
    
    return hls[0] * 255
    
def level_to_color(level, norm = 255, shiftp = 0.0, lum=0.5, sat=0.75):
    """
    Convert a grey level to an rgb color. the conversion is cyclique so the 
    color for 255 is near the color for 0.
    grey_level [in] : [0, 255]
    lum [in] : [0.0, 1.0] luminance for the color
    sat [in] : [0.0, 1.0] saturation for the color
    
    return : pygame.Color
    """      
    level_compressed = level * (1-shiftp)    
    value = shiftp + level_compressed/norm
    
    c = colorsys.hls_to_rgb(value, lum, sat)    
    return (int(c[0]*255), int(c[1]*255), int(c[2]*255))
    
def hue_image(surface):
    """
    Create a colored image from a grey image.
    Blacks pixels will stay black
    surface [in] : pygame.Surface in grey level 
    
    return pygame.Surface
    """
    res = surface.copy()
    pix = pygame.PixelArray(surface)
    pix_res = pygame.PixelArray(res)
    
    for x in range(surface.get_width()):
        for y in range(surface.get_height()):
            if pix_res[x][y] != 0: 
                pix_res[x][y] = level_to_color(
                                        grey_level((pix_res[x][y])))
    
    return res
    
def compute_dispersion_level(im_l, im_r, offset, threshold, pix_level):
    """
    Compute the dispertion image of two images. The image can be shift by
    an offset.
    
    im_l [in] : pygame.Surface left image
    im_r [in] : pygame.Surface right image
    offset [in] : set with x and y offset for dispersion computation
    threshold [in] : threshold to determine the difference allowed for a match

    return : pygame.Surface dispersion image  
    """
    if (im_l.get_width() != im_r.get_width()) or\
       (im_l.get_height() != im_r.get_height()):        
        raise ImagesSizeDoNotMatch()

    im_disp = im_l.copy()
    im_disp.fill((0, 0, 0))
    
    pix_l = pygame.PixelArray(im_l)
    pix_r = pygame.PixelArray(im_r)
    pix_disp = pygame.PixelArray(im_disp)
        
    for x in range(im_l.get_width()):
        for y in range(im_l.get_height()):
            l = pix_l[x][y]
            
            xd = x + offset[0]
            if not 0 <= xd < im_r.get_width():
                continue
            yd = y + offset[1]
            if not 0 <= yd < im_r.get_height():
                continue           
            r = pix_r[xd][yd]
            if l != 0:
                p_l = pix_level(l)
                p_r = pix_level(r)
                if abs(p_l - p_r) < threshold:                    
                    pix_disp[x][y] = level_to_color((p_l + p_r) / 2)
                    
    del pix_l
    del pix_r
    del pix_disp

    return im_disp

def image_to_levels(image, pix_level):
    """
    Will convert an image to a 2D list of level computed by an input function.
    
    image [in]: pygame.Surface
    pix_level: function taking a pixelArray (3 bytes) and compute a [0, 255]
               level
               
    return: 2D list (same size than the image) with levelfor each "pixel".
    """
    
    #test pour l'image
    
    pixels = pygame.PixelArray(image)
    levels = []
    
    for x in range(image.get_width()):
        levels.append([])        
        for y in range(image.get_height()):
            levels[x].append(pix_level(pixels[x][y]) )
            
    return levels

def dispertion_rank(levels, windows):
    """
      
    """    
    rank = []    
    # filtre sur le rang.
    # faire les comparaison avec :  "a < x < b"
    for x in range(len(levels)):
        rank.append([])  
        for y in range(len(levels[x])):
            rank[x].append(0)
            
            if x < (windows[0]//2) or x >= (len(levels) - (windows[0]//2) - 1):
                continue
            if y < (windows[1]//2) or y >= (len(levels[x]) - (windows[1]//2) - 1):
                continue
            
            for i in range(windows[0]):
                for j in range(windows[1]):
                    if i == windows[0]//2 and j == windows[1]//2:
                        continue
                    if levels[x][y] < levels[x - windows[0]//2 + i]\
                                            [y - windows[1]//2 + j]:
                        rank[x][y] = rank[x][y] + 1
                 
    return rank
                    
def SAD(levels1, levels2, windows, offset):
    """
    
    return levels
    """
    #tests listes de memes tailles
        
    lvl_res = []
    
    for x in range(len(levels1)):
        lvl_res.append([])
        for y in range(len(levels1[0])):
            lvl_res[x].append(0)
                        
            xd = x + offset[0]
            if not 0 <= xd < len(levels2):
                continue
            yd = y + offset[1]
            if not 0 <= yd < len(levels2):
                continue   
            
            # Verification si dans les deux images
            if  not (windows[0]//2) <= x <= len(levels1) - (windows[0]//2) - 1:
                continue        
            if  not (windows[0]//2) <= xd <= len(levels1) - (windows[0]//2) - 1:
                continue
            if  not (windows[1]//2) <= y <= len(levels2[x]) - (windows[1]//2) - 1:
                continue        
            if  not (windows[1]//2) <= yd <= len(levels2[xd]) - (windows[1]//2) - 1:
                continue 
            
            somme = 0
            for i in range(windows[0]):
                for j in range(windows[1]):
                    if i == windows[0]//2 and j == windows[1]//2:
                        continue
                    somme += abs(levels1[x - windows[0]//2 + i]
                                        [y - windows[1]//2 + j] - 
                                 levels2[xd - windows[0]//2 + i]
                                        [yd - windows[1]//2 + j])
                    
            lvl_res[x][y] = somme
    
    return lvl_res

def dispertion_census(levels, windows):
    """
    Compute the dispertion image of two images. The image can be shift by
    an offset.
    
    im_l [in] : pygame.Surface left image
    im_r [in] : pygame.Surface right image
    offset [in] : set with x and y offset for dispersion computation
    windows [in] : windows for the computation

    return : image de rank #pygame.Surface dispersion image  
    """    
    rank = []    
    # filtre sur le rang.
    # faire les comparaison avec :  "a < x < b"
    for x in range(len(levels)):
        rank.append([])  
        for y in range(len(levels[x])):
            rank[x].append([])
            
            if x < (windows[0]//2) or x >= (len(levels) - (windows[0]//2) - 1):
                continue
            if y < (windows[1]//2) or y >= (len(levels[x]) - (windows[1]//2) - 1):
                continue
            
            for i in range(windows[0]):
                for j in range(windows[1]):
                    if i == windows[0]//2 and j == windows[1]//2:
                        continue
                    if levels[x][y] < levels[x - windows[0]//2 + i]\
                                            [y - windows[1]//2 + j]:
                        rank[x][y].append(1)
                    else:
                        rank[x][y].append(0)
                 
    return rank

def hamming_distance(levels1, levels2, offset):
    """
    
    return levels
    """
    #tests listes de memes tailles
        
        
    lvl_res = []
    
    for x in range(len(levels1)):
        lvl_res.append([])
        for y in range(len(levels1[0])):
            lvl_res[x].append(0)
                        
            xd = x + offset[0]
            if not 0 <= xd < len(levels2):
                continue
            yd = y + offset[1]
            if not 0 <= yd < len(levels2):
                continue   
                      
            somme = 0
            if len(levels1[x][y]) != 0 and len(levels2[xd][yd]) != 0:                
                for index in range(len(levels1[x][y])):
                    if levels1[x][y][index] != levels2[xd][yd][index]:
                        somme += 1
                    
              
            lvl_res[x][y] = somme
    
    return lvl_res
                        
def levels_to_image(levels):
    """
    """
    
    """
    print(type(levels))
    #print(levels)
    print(len(levels))
    print(type(levels[0]))
    print(levels[0])
    print(len(levels[0]))
    """
    
    
    maximum = 0
    for level in levels:        
        if maximum < max(level):
            maximum = max(level)    
            
    print("maximum pour normalisation :", maximum)
    
    im_res = pygame.Surface((len(levels), len(levels[0])))
    im_res.fill((0, 0, 0))
    
    pix_res = pygame.PixelArray(im_res)
    
    for x in range(im_res.get_width()):
        for y in range(im_res.get_height()):
            if levels[x][y] != 0:
                pix_res[x][y] = level_to_color(levels[x][y], maximum, 0.35)
    
    del pix_res
    
    return im_res


def echelle(shift_p):
    """
    taille 200*20
    """    
    width = 200
    height = 20
    echelle = pygame.Surface((width, height))
    echelle.fill((255, 255, 255))
    pix_echelle = pygame.PixelArray(echelle)
    
    for x in range(width):
        for y in range(height):
            pix_echelle[x][y] = level_to_color(x, width, shift_p)
    
    del pix_echelle
    
    return echelle

def print_GUI(surface, msg, top_left, font):
    """
    Print a black message in a surface
    surface [in] : pygame.Surface surface where the message will be blit
    msg [in] : text to print
    top_left [in] : left top position to print the message
    font [in] : font of the message
    """    
    msg_surface = font.render(msg, False, (0, 0, 0))
    rect = msg_surface.get_rect()
    rect.topleft = top_left
    surface.blit(msg_surface, rect)       

def mask_image(image, mask):
    """
    Mask an image with an other image. The resulting image will be a copy
    of the inputed one for non black (0, 0, 0) pixels of the mask.
    The two images must have the same size.
    surface [in] : pygame.Surface image we want to mask
    mask [in] : pygame.Surface mask all black (0, 0, 0) pixel will mask the
    image
    
    return : pygame.Surface result of the mask
    """
    if (image.get_width() != mask.get_width()) or\
       (image.get_height() != mask.get_height()):        
        raise ImagesSizeDoNotMatch()
    
    im_res = image.copy()
    im_res.fill((0, 0, 0))
    
    pix_image = pygame.PixelArray(image)
    pix_mask = pygame.PixelArray(mask)
    pix_res = pygame.PixelArray(im_res)
        
    for x in range(image.get_width()):
        for y in range(image.get_height()):
            if pix_mask[x][y] != 0:
                pix_res[x][y] = pix_image[x][y]
        
    del pix_image
    del pix_mask
    del pix_res 
    
    return im_res









