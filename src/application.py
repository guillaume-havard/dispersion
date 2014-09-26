 #! /usr/bin/python3

"""
/!\ La taille des images est fixe (640, 480)
"""
import sys
import pygame
from pygame.locals import *
import colorsys

from dispersion import *
 
def algo_SAD(im_l, im_r, pix_level, offset, windows):
    print("level l...", end="")
    levels_l = image_to_levels(im_l, pix_level)  
    print("ok") 
    print("level r...", end="")                 
    levels_r = image_to_levels(im_r, pix_level)
    print("ok")
    print("SAD...", end="")
    sad = SAD(levels_l, levels_r, (3, 3), offset)    
    print("ok") 
    print("generation image...", end="")
    im_result = levels_to_image(sad)
    print("ok")
    
    return im_result
     
def algo_rank_SAD(im_l, im_r, pix_level, offset, windows):
    print("level l...", end="")
    levels_l = image_to_levels(im_l, pix_level)  
    print("ok") 
    print("level r...", end="")                 
    levels_r = image_to_levels(im_r, pix_level)
    print("ok")
    print("rank l...", end="")
    rank_l = dispertion_rank(levels_l, windows)
    print("ok") 
    print("rank r...", end="")
    rank_r = dispertion_rank(levels_r, windows) 
    print("ok")
    print("SAD...", end="")                   
    sad = SAD(rank_l, rank_r, windows, offset)
    print("ok") 
    print("generation image...", end="")
    im_result = levels_to_image(sad)
    print("ok")
    
    return im_result

def algo_census_hamming(im_l, im_r, pix_level, offset, windows):
    print("level l...", end="")
    levels_l = image_to_levels(im_l, pix_level)  
    print("ok") 
    print("level r...", end="")                 
    levels_r = image_to_levels(im_r, pix_level)
    print("ok")
    print("census l...", end="")
    census_l = dispertion_census(levels_l, windows)
    print("ok")         
    print("census r...", end="")
    census_r = dispertion_census(levels_r, windows) 
    print("ok")
    print("hamming...", end="")                   
    hamming = hamming_distance(census_l, census_r, offset)
    print("ok") 
    print("generation image...", end="")
    im_result = levels_to_image(hamming)
    print("ok")
    
    return im_result    
    
if __name__ == "__main__":     
    marge_x = 180 # max offset between the two pictures on the x axis
    marge_y = 30 # max offset between the two pictures on the y axis
    off_x = 0 # offset between the two pictures
    off_y = 0 # offset between the two pictures
    thresh = 30  # max difference value to consider value alike.
    help = False # does the help is activate
    windows = [3, 3] # windows used with some algorithms
    
    pygame.init()
    FPS = 30 
    fpsClock = pygame.time.Clock()    
    DISPLAYSURF = pygame.display.set_mode((2*(640 + marge_x), 960))
    pygame.display.set_caption('Dispersion')
    pygame.key.set_repeat(100, 20)
    
    font = pygame.font.Font("freesansbold.ttf", 32)
    
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    
           
    
    im_l = pygame.image.load('l.bmp')
    im_r = pygame.image.load('r.bmp')
    im_l_OE = pygame.image.load('l_OE.bmp')
    im_r_OE = pygame.image.load('r_OE.bmp')
    
    type_algorithme = "none"
    type_affichage = "hue"
    im_l_aff = im_l
    im_r_aff = im_r    
    
    im_result = im_l.copy()
    im_result.fill(BLACK)
    
    im_echelle = None
   
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
                    
                elif event.key == K_a:
                    if type_affichage == "hue":
                        type_affichage = "grey"
                        im_l_aff = hue_image(im_l_OE)
                        im_r_aff = hue_image(im_r_OE)
                    elif type_affichage == "grey": 
                        type_affichage = "hue"  
                        im_l_aff = im_l
                        im_r_aff = im_r
    
        
                elif event.key == K_f:
                    type_algorithme = "simple"
                    if type_affichage == "hue":
                        im_result = compute_dispersion_level(im_l, im_r, 
                                                        (off_x, off_y), thresh, 
                                                        hue_level)   
                    elif type_affichage == "grey":
                        im_result = compute_dispersion_level(im_l_OE, im_r_OE, 
                                                        (off_x, off_y), thresh, 
                                                        grey_level)                
                elif event.key == K_d:  
                    type_algorithme = "sad" 
                    im_result = algo_SAD(im_l, im_r, grey_levell, (off_x, off_y), windows)
                    im_echelle = echelle(0.35)
                elif event.key == K_r:  
                    type_algorithme = "rank" 
                    im_result = algo_rank_SAD(im_l, im_r, grey_level, (off_x, off_y), windows)
                    im_echelle = echelle(0.35)
                elif event.key == K_c:   
                    type_algorithme = "census"
                    im_result = algo_census_hamming(im_l, im_r, grey_level, (off_x, off_y), windows)
                    im_echelle = echelle(0.35)
                    
                elif event.key == K_s:
                    message = type_algorithme + "_"
                    if type_algorithme == "simple":
                        message += type_affichage + "_" + str(thresh) + "_" 
                    message += str(off_x) + "-" + str(off_y) + ".bmp"
                    
                    pygame.image.save(im_result, message)  
                    #pygame.image.save(im_echelle, "echelle.bmp")
                    
                # threshold difference
                elif event.key == K_t:
                    thresh -= step
                    if thresh < 0:
                        thresh = 0
                elif event.key == K_y:
                    thresh += step
                    if thresh > 255:
                        thresh = 255
                # help
                elif event.key == K_h:
                    help = not help  
                    if help:
                        im_r_aff.set_alpha(100)
                    else:
                        im_r_aff.set_alpha()
                # Windows
                elif event.key == K_w:   
                    windows = [windows[0] - 2, windows[0] - 2]
                    if windows[0] < 1:
                        windows = [1, 1]
                elif event.key == K_x:   
                    windows = [windows[0] + 2, windows[0] + 2]
                    if windows[0] > 29:
                        windows = [29, 29]
                
        DISPLAYSURF.blit(im_l_aff, (0, 0))
        if help:
            DISPLAYSURF.blit(im_l_aff, (640 + marge_x, marge_y))
        DISPLAYSURF.blit(im_r_aff, (640 + marge_x - off_x, marge_y - off_y))        
        DISPLAYSURF.blit(im_result, (0, 480 + 10))
        
        if im_echelle:
            DISPLAYSURF.blit(im_echelle, (650, 960 - 60))
        
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
        message = "windows(w/x) : (" + str(windows[0]) + ", " + str(windows[1]) + ")" 
        print_GUI(DISPLAYSURF, message, (lim_print_x + 400, lim_print_y + 50), font)
        message = "type affichage(a) : " + type_affichage + \
                  "   seuil(t/y) : " + str(thresh)
        print_GUI(DISPLAYSURF, message, (lim_print_x, lim_print_y + 80), font)
        message = "visualisation supersposition(h) : " + \
                  ("active" if help else "non active")
        print_GUI(DISPLAYSURF, message, (lim_print_x, lim_print_y + 110), font)
        message = "DISP SIMPLE (F) SAD (D)  RANK (R)  CENSUS (C)"
        print_GUI(DISPLAYSURF, message, (lim_print_x, lim_print_y + 150), font)
        
        pygame.display.update()
        fpsClock.tick(FPS)
        
    
      
       