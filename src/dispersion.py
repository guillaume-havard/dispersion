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
    
def level_to_color(grey_level, lum=0.5, sat=0.75):
    """
    Convert a grey level to an rgb color. the conversion is cyclique so the 
    color for 255 is near the color for 0.
    grey_level [in] : [0, 255]
    lum [in] : [0.0, 1.0] luminance for the color
    sat [in] : [0.0, 1.0] saturation for the color
    
    return : pygame.Color
    """  
    c = colorsys.hls_to_rgb(grey_level/255, .5, .7)    
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
    
def compute_dispertion(im_l, im_r, offset, threshold, pix_level):
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
    
    
if __name__ == "__main__":       
    marge_x = 180 # max offset between the two pictures on the x axis
    marge_y = 30 # max offset between the two pictures on the y axis
    off_x = 92
    off_y = -6
    thresh = 30  # max difference value to consider value alike.
    help = False # does the help is activate
    
    pygame.init()
    FPS = 30 
    fpsClock = pygame.time.Clock()    
    DISPLAYSURF = pygame.display.set_mode((2*(640 + marge_x), 960))
    pygame.display.set_caption('Dispersion')
    pygame.key.set_repeat(100, 20)
    
    font = pygame.font.Font("freesansbold.ttf", 32)
    
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    
    type_dispersion = "grey"       
   
    if type_dispersion == "grey":
        im_l = pygame.image.load('l.bmp')
        im_r = pygame.image.load('r.bmp')
        im_l_hue = hue_image(im_l)
        im_r_hue = hue_image(im_r)
        pix_level = grey_level
    elif type_dispersion == "hue":
        im_l = pygame.image.load('l_hue.bmp')
        im_r = pygame.image.load('r_hue.bmp')
        im_l_hue = im_l
        im_r_hue = im_r
        pix_level = hue_level
    
    
    im_result = im_l.copy()
    im_result.fill(BLACK)
   
    while True: 
        DISPLAYSURF.fill(WHITE)
        
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                step = 1
                mods = pygame.key.get_mods()
                if mods & KMOD_SHIFT:
                    step = 5
                if mods & KMOD_CTRL:
                    step = 10
                
                if event.key == K_RIGHT:
                    off_x -= step
                    if off_x < -marge_x:
                        off_x = -marge_x
                elif event.key == K_LEFT:
                    off_x += step
                    if off_x > marge_x:
                        off_x = marge_x
                elif event.key == K_DOWN:
                    off_y -= step
                    if off_y < -marge_y:
                        off_y = -marge_y
                elif event.key == K_UP:
                    off_y += step
                    if off_y > marge_y:
                        off_y = marge_y
                elif event.key == K_ESCAPE:
                    pygame.event.post(pygame.event.Event(QUIT))
                elif event.key == K_RETURN:
                    im_result = compute_dispertion(im_l, im_r, 
                                                   (off_x, off_y), thresh, 
                                                pix_level)
                elif event.key == K_s:
                    pygame.image.save(im_result, "res_" + type_dispersion +
                                                "_" + str(thresh) + "_" +
                                                str(off_x) + "-" + str(off_y)
                                                 + ".bmp")  
                elif event.key == K_a:
                    thresh -= step
                    if thresh < 0:
                        thresh = 0
                elif event.key == K_z:
                    thresh += step
                    if thresh > 255:
                        thresh = 255
                elif event.key == K_h:
                    help = not help  
                    if help:
                        im_r_hue.set_alpha(100)
                    else:
                        im_r_hue.set_alpha()                                          
        
        
                
        DISPLAYSURF.blit(im_l_hue, (0, 0))
        if help:
            DISPLAYSURF.blit(im_l_hue, (640 + marge_x, marge_y))
        DISPLAYSURF.blit(im_r_hue, (640 + marge_x - off_x, marge_y - off_y))        
        DISPLAYSURF.blit(im_result, (0, 480 + 10))
        
        pygame.draw.rect(DISPLAYSURF, (255, 0, 0),
                         (640, 0, 640 + 2*marge_x, 480 + 2*marge_y), 1)
        pygame.draw.rect(DISPLAYSURF, (0, 0, 255),
                         (640 + marge_x, marge_y, 640, 480), 1)
                         
        # affichage textuel
        marge_print = 20
        lim_print_y = 480 + 2*marge_y + marge_print
        lim_print_x = 640 + marge_print
        message = "Dispersion"
        print_GUI(DISPLAYSURF, message, (lim_print_x, lim_print_y), font)
        message = "offset : (" + str(off_x) + ", " + str(off_y) + ")" 
        print_GUI(DISPLAYSURF, message, (lim_print_x, lim_print_y + 50), font)
        message = "type dispersion : " + type_dispersion + \
                  "   seuil(a/z) : " + str(thresh)
        print_GUI(DISPLAYSURF, message, (lim_print_x, lim_print_y + 80), font)
        message = "visualisation supersposition(h) : " + \
                  ("active" if help else "non active")
        print_GUI(DISPLAYSURF, message, (lim_print_x, lim_print_y + 110), font)
        
        pygame.display.update()
        fpsClock.tick(FPS)
        
        
        
        
        
        
        
        
        
          
