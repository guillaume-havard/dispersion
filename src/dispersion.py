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
    
    return (r+g+b) // 3

def hue_level(pix):
    """
    Convert a color into hue level
    pix [in] : int (RGB sur 24 bits) from PixelArray

    return : hue level [0, 255]
    """
    r = (pix & 0xFF0000) >> 16
    g = (pix & 0x00FF00) >> 8
    b = pix & 0x0000FF
    
    try:
        hls = colorsys.rgb_to_hls(r, g, b)
    except ZeroDivisionError as err:
        #a, a, exc_tb = sys.exc_info()
        #print("hue_level", err, exc_tb.tb_lineno)
        hls = (0, 0, 0)
    
    return int(hls[0] * 255)
    
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

def level_to_grey(level, norm = 255, shiftp = 0.0):
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
        
    return (int(value*255), int(value*255), int(value*255))


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
            levels[x].append(pix_level(pixels[x][y]))            
                           
    return levels


def levels_to_image(levels, level_to_pix):
    """
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
                pix_res[x][y] = level_to_pix(levels[x][y], maximum, 0.35)
    
    del pix_res
    
    return im_res
    
    
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


def dispertion_rank(levels, window):
    """
      
    """    
    rank = []    
    # filtre sur le rang.
    # faire les comparaison avec :  "a < x < b"
    for x in range(len(levels)):
        rank.append([])  
        for y in range(len(levels[x])):
            rank[x].append(0)
            
            if x < (window//2) or x >= (len(levels) - (window//2) - 1):
                continue
            if y < (window//2) or y >= (len(levels[x]) - (window//2) - 1):
                continue
            
            for i in range(window):
                for j in range(window):
                    if i == window//2 and j == window//2:
                        continue
                    if levels[x][y] < levels[x - window//2 + i]\
                                            [y - window//2 + j]:
                        rank[x][y] = rank[x][y] + 1
                 
    return rank
                    
def SAD(levels1, levels2, window, disp_range, offset):
    """
    
    return levels
    """
    #tests listes de memes tailles
    hist = {}
    tot = 0   
    lvl_res = []
    
    win = window//2
    
    for x in range(len(levels1)):
        lvl_res.append([])
        for y in range(len(levels1[0])):
            lvl_res[x].append(0)            
            if not win + disp_range[1] <= x < len(levels1) - win:
                continue
            if not win <= y < len(levels1[0]) - win:
                continue                                
            xd = x + offset[0]           
            yd = y + offset[1]            
            # Verification si dans les deux images                    
            if not win + disp_range[1] <= xd < len(levels2) - win:
                continue       
            if not win <= yd < len(levels2[0]) - win:
                continue 
            
            best_disp = disp_range[0]
            prev_somme = 65532
            for disp in range(disp_range[0], disp_range[1]+1):                             
                somme = 0
                for i in range(-win, win + 1):
                    for j in range(-win, win + 1):                        
                        #if x-win+disp <= 0 or xd-win+disp <= 0:
                            #continue
                        somme += abs(levels1[x + i]
                                            [y + j] - 
                                     levels2[xd + i - disp]
                                            [yd + j])
                
                if somme < prev_somme:
                    prev_somme = somme
                    best_disp = disp
            lvl_res[x][y] = best_disp
               
    return lvl_res
    
def SAD2(levels1, levels2, window, disp_range, offset):
    """
    Je n'ai pas les resultats escomptes avec SAD pour le moment.
    2nd tentative, pas d'offset pour le moment.

    arg :
    list de list d'int * 2
    int
    set de deux int
    nimporte quoi
    
    retourne : list de list d'int
    """
    # va parcourir les pixel d'une image(1) et essayer de trouver les pixels 
    # correspondant sur l'autre image(2) avec un decalage de disp_range
    # comparaison du voisinage des pixel avec une matrice de carree de taille
    # window
    
    # fenetre de meme taille ?
    
    win = window // 2
    res = []
    for x in range(len(levels1)):
        res.append([])        
        for y in range(len(levels1[0])):
            res[x].append(0)
            
            if not win <= x < len(levels1) - win:
                continue
            if not win <= y < len(levels1[0]) - win:
                continue
            
            best_disp = 0
            min_somme = 65532
            for d in range(disp_range[0], disp_range[1] + 1):
                if x-win-d < 0:
                    continue
                somme = 0
                for i in range(-win, win+1):
                    for j in range(-win, win+1):
                        somme += abs(levels1[x+i][y+j] - 
                                     levels2[x+i-d][y+j])
                    
                if somme <= min_somme:
                    min_somme = somme
                    best_disp = d
                    
            res[x][y] = best_disp
            
    return res

def histo_2D(levels):
    
    hist = {}

    for x in range(len(levels)):
        for y in range(len(levels[0])):
            if levels[x][y] not in hist:
                hist[levels[x][y]] = 1
            else:
                hist[levels[x][y]] += 1
                
    return hist
"""
histo = histo_2D(levels)
    for key in iter(histo):
        print("{} : {}".format(key, histo[key]))
"""


def histo_2D_int(levels):
    
    hist = {}

    for x in range(len(levels)):
        for y in range(len(levels[0])):
            if int(levels[x][y]) not in hist:
                hist[int(levels[x][y])] = 1
            else:
                hist[int(levels[x][y])] += 1
                
    return hist


def dispertion_census(levels, window):
    """
    Compute the dispertion image of two images. The image can be shift by
    an offset.
    
    im_l [in] : pygame.Surface left image
    im_r [in] : pygame.Surface right image
    offset [in] : set with x and y offset for dispersion computation
    window [in] : window for the computation

    return : image de rank #pygame.Surface dispersion image  
    """    
    rank = []    
    # filtre sur le rang.
    # faire les comparaison avec :  "a < x < b"
    for x in range(len(levels)):
        rank.append([])  
        for y in range(len(levels[x])):
            rank[x].append([])
            
            if x < (window//2) or x >= (len(levels) - (window//2) - 1):
                continue
            if y < (window//2) or y >= (len(levels[x]) - (window//2) - 1):
                continue
            
            for i in range(window):
                for j in range(window):
                    if i == window//2 and j == window//2:
                        continue
                    if levels[x][y] < levels[x - window//2 + i]\
                                            [y - window//2 + j]:
                        rank[x][y].append(1)
                    else:
                        rank[x][y].append(0)
                 
    return rank

def hamming_distance(levels1, levels2, disp_range, offset):
    """
    sans window
    
    return levels
    """
    #tests listes de memes tailles
        
        
    lvl_res = []
    
    for x in range(len(levels1)):
        lvl_res.append([])
        for y in range(len(levels1[0])):
            lvl_res[x].append(0)
                        
            
            
            xd = x + offset[0]
            if not disp_range[1] <= xd < len(levels2):
                continue
            yd = y + offset[1]
            if not 0 <= yd < len(levels2):
                continue   
            
            prev_somme = 65532
            best_disp = 0;
            for disp in range(disp_range[0], disp_range[1] + 1):                                                  
                somme = 0
                if len(levels1[x][y]) != 0 and len(levels2[xd-disp][yd]) != 0:                
                    for index in range(len(levels1[x][y])):
                        if levels1[x][y][index] != levels2[xd-disp][yd][index]:
                            somme += 1
                
                if somme < prev_somme:
                    prev_somme = somme
                    best_disp = disp
                    
              
            lvl_res[x][y] = best_disp
    
    return lvl_res
                        

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









