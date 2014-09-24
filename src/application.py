 #! /usr/bin/python3

"""
/!\ La taille des images est fixe (640, 480)
"""
import sys
import pygame
from pygame.locals import *
import colorsys

from dispersion import *
    
if __name__ == "__main__":       
    marge_x = 180 # max offset between the two pictures on the x axis
    marge_y = 30 # max offset between the two pictures on the y axis
    off_x = 92 # offset between the two pictures
    off_y = -6 # offset between the two pictures
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
        
       
