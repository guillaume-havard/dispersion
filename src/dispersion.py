 #! /usr/bin/python3

import sys
import pygame
from pygame.locals import *


def grey_level(color):
    """
    Convert a color into grey level
    color [in] : pygame.Color

    return : grey level [0, 255]
    """
    pass
    
def grey_to_color(grey_level):
    """
    Convert a grey level to an rgb color. the conversion is cyclique the color
    for 255 is near the color for 0.
    grey_level [in] : [0, 255]

    return : pygame.Color
    """  
    pass

def hue_image(surface):
    """
    Convert a grey image into a colored one
    """
    pass
    
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
    pass
    
    
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
    
    #im_l = pygame.image.load('l.bmp')
    #im_r = pygame.image.load('r.bmp')   
   
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    
    #im_result = im_l.copy()
    #im_result.fill(BLACK)
   
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
                    
                
        #DISPLAYSURF.blit(im_l, (0, 0))
        #DISPLAYSURF.blit(im_r, (640 + marge, marge ))        
        #DISPLAYSURF.blit(im_result, (0, 480))
        
        pygame.draw.rect(DISPLAYSURF, (255, 0, 0),
                         (640, 0, 640 + 2*marge, 480 + 2*marge), 1)
        pygame.draw.rect(DISPLAYSURF, (0, 0, 255),
                         (640 + marge - off_x, marge - off_y, 640, 480), 1)
        
        
        pygame.display.update()
        fpsClock.tick(FPS)
        
        
        
        
        
        
        
        
        
          
