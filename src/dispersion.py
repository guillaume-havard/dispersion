 #! /usr/bin/python3

"""

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
    h = (pix & 0xFF0000) >> 16
    m = (pix & 0x00FF00) >> 8
    l = pix & 0x0000FF
    
    return (h+m+l) / 3
    
def grey_level_to_color(grey_level, lum=0.5, sat=0.75):
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
                pix_res[x][y] = grey_level_to_color(
                                        grey_level((pix_res[x][y])))
    
    return res
    
def compute_dispertion(im_l, im_r, offset, threshold):
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
            g = pix_l[x][y]
            xd = x + offset[0]
            if not 0 <= xd < im_r.get_width():
                continue
            yd = y + offset[1]
            if not 0 <= yd < im_r.get_height():
                continue           
            d = pix_r[xd][yd]
            if g != 0:                
                if abs(grey_level(g) - grey_level(d)) < threshold:                    
                    pix_disp[x][y] = grey_level_to_color(grey_level((g)))  
                    
    del pix_l
    del pix_r
    del pix_disp

    return im_disp
    
    
if __name__ == "__main__":
    print("coucou")
    
    marge = 100
    off_x = 0
    off_y = 0
    
    pygame.init()
    FPS = 30 
    fpsClock = pygame.time.Clock()    
    DISPLAYSURF = pygame.display.set_mode((2*(640 + marge), 960))
    pygame.display.set_caption('Dispersion')
    
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    
    im_l = pygame.image.load('l.bmp')
    im_r = pygame.image.load('r.bmp')   
   
    im_l_hue = hue_image(im_l)
    im_r_hue = hue_image(im_r)
    
    im_result = im_l.copy()
    im_result.fill(BLACK)
   
    while True: 
        DISPLAYSURF.fill(WHITE)
        
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_RIGHT:
                    off_x -= 1
                    if off_x < -marge:
                        off_x = -marge
                elif event.key == K_LEFT:
                    off_x += 1
                    if off_x > marge:
                        off_x = marge
                elif event.key == K_DOWN:
                    off_y -= 1
                    if off_y < -marge:
                        off_y = -marge
                elif event.key == K_UP:
                    off_y += 1
                    if off_y > marge:
                        off_y = marge
                elif event.key == K_ESCAPE:
                    pygame.event.post(pygame.event.Event(QUIT))
                elif event.key == K_RETURN:
                    im_result = compute_dispertion(im_l, im_r, 
                                                (off_x, off_y), 30)
                elif event.key == K_s:
                    pygame.image.save(result, "res_" + str(off_x) +
                                             "-" + str(off_y) + ".bmp")   
                                            
                print("offset : ", off_x, off_y)
                
        DISPLAYSURF.blit(im_l_hue, (0, 0))
        DISPLAYSURF.blit(im_r_hue, (640 + marge - off_x, marge - off_y))        
        DISPLAYSURF.blit(im_result, (0, 480 + 10))
        
        pygame.draw.rect(DISPLAYSURF, (255, 0, 0),
                         (640, 0, 640 + 2*marge, 480 + 2*marge), 1)
        pygame.draw.rect(DISPLAYSURF, (0, 0, 255),
                         (640 + marge, marge, 640, 480), 1)
        
        
        pygame.display.update()
        fpsClock.tick(FPS)
        
        
        
        
        
        
        
        
        
          
