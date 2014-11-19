 #! /usr/bin/python3

"""
Application de test d'algorithme de calculs de disparite stereoscopique.

/!\ La taille des images est fixe (640, 480) pour la fenetre principale
"""
import sys
import pygame
from pygame.locals import *
import colorsys

from dispersion import *
 
def algo_SAD(im_l, im_r, pix_level, offset, window):
    print("level l...", end="")
    levels_l = image_to_levels(im_l, pix_level)  
    print("ok")    
    print("level r...", end="")                 
    levels_r = image_to_levels(im_r, pix_level)
    print("ok")
    print("SAD...", end="")
    sad = SAD(levels_l, levels_r, window, (0, 25), offset)    
    print("ok") 
    print("generation image...", end="")
    im_result = levels_to_image(sad, level_to_color)
    print("ok")
    """
    histo = histo_2D(sad)
    for key in iter(histo):
        print("{} : {}".format(key, histo[key]))
    """
    return im_result
     
def algo_rank_SAD(im_l, im_r, pix_level, offset, window):
    print("level l...", end="")
    levels_l = image_to_levels(im_l, pix_level)  
    print("ok") 
    print("level r...", end="")                 
    levels_r = image_to_levels(im_r, pix_level)
    print("ok")
    print("rank l...", end="")
    rank_l = dispertion_rank(levels_l, window)
    print("ok") 
    print("rank r...", end="")
    rank_r = dispertion_rank(levels_r, window) 
    print("ok")
    print("SAD...", end="")                   
    sad = SAD(rank_l, rank_r, window, (0, 16), offset)
    print("ok") 
    print("generation image...", end="")
    im_result = levels_to_image(sad, level_to_color)
    print("ok")
    
    return im_result

def algo_census_hamming(im_l, im_r, pix_level, offset, window):
    print("level l...", end="")
    levels_l = image_to_levels(im_l, pix_level)  
    print("ok") 
    print("level r...", end="")                 
    levels_r = image_to_levels(im_r, pix_level)
    print("ok")
    print("census l...", end="")
    census_l = dispertion_census(levels_l, window)
    print("ok")         
    print("census r...", end="")
    census_r = dispertion_census(levels_r, window) 
    print("ok")
    print("hamming...", end="")                   
    hamming = hamming_distance(census_l, census_r, (0, 16), offset)
    print("ok") 
    print("generation image...", end="")
    im_result = levels_to_image(hamming, level_to_color)
    print("ok")
    
    return im_result    
    
if __name__ == "__main__":     
    marge_x = 180 # max offset between the two pictures on the x axis
    marge_y = 30 # max offset between the two pictures on the y axis
    off_x = 147 # offset between the two pictures
    off_y = -5 # offset between the two pictures
    thresh = 30  # max difference value to consider value alike.
    help = False # is the help activated ?
    window = 3 # window used with some algorithms
    
    pygame.init()
    FPS = 30 
    fpsClock = pygame.time.Clock()    
    DISPLAYSURF = pygame.display.set_mode((2*(640 + marge_x), 960))
    pygame.display.set_caption('Dispersion')
    pygame.key.set_repeat(100, 20)
    
    font = pygame.font.Font("freesansbold.ttf", 32)
    
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    
           
    #im_l = pygame.image.load('stereogramleft.jpg')
    #im_r = pygame.image.load('stereogramright.jpg')
    #im_l = pygame.image.load('tsukubaleft.jpg')
    #im_r = pygame.image.load('tsukubaright.jpg')
    #im_l = pygame.image.load('scene1.row3.col3.ppm')
    #im_r = pygame.image.load('scene1.row3.col4.ppm')
    #im_l = pygame.image.load('im2.ppm')
    #im_r = pygame.image.load('im6.ppm')
    #im_l = pygame.image.load('l_150.bmp')
    #im_r = pygame.image.load('r_150.bmp')
    im_l = pygame.image.load('l.bmp')
    im_r = pygame.image.load('r.bmp')
    #im_l_OE = pygame.image.load('l_OE.bmp')
    #im_r_OE = pygame.image.load('r_OE.bmp') 
    im_l_OE = pygame.image.load('l_pingouin_-horiz_40.bmp')
    im_r_OE = pygame.image.load('r_pingouin_-horiz_40.bmp')
    
    type_algorithme = "none"
    type_affichage = "hue"
    im_l_aff = im_l
    im_r_aff = im_r    
    im_l_comp = im_l
    im_r_comp = im_r     
    
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
                elif event.key == K_o:
                    off_x = 0
                    off_y = 0
                elif event.key == K_ESCAPE:
                    pygame.event.post(pygame.event.Event(QUIT))
                    
                elif event.key == K_a:
                    if type_affichage == "hue":
                        type_affichage = "OE"
                        im_l_aff = hue_image(im_l_OE)
                        im_r_aff = hue_image(im_r_OE)
                        im_l_comp = im_l_OE
                        im_r_comp = im_r_OE
                        if help:
                            im_r_aff.set_alpha(100)
                    elif type_affichage == "OE": 
                        type_affichage = "hue"  
                        im_l_aff = im_l
                        im_r_aff = im_r
                        im_l_comp = im_l
                        im_r_comp = im_r
                        if help:                        
                            im_r_aff.set_alpha(100)    
        
                elif event.key == K_f:
                    type_algorithme = "simple"
                    if type_affichage == "hue":
                        im_result = compute_dispersion_level(im_l_comp, im_r_comp, 
                                                        (off_x, off_y), thresh, 
                                                        hue_level)   
                    elif type_affichage == "OE":
                        im_result = compute_dispersion_level(im_l_comp, im_r_comp, 
                                                        (off_x, off_y), thresh, 
                                                        grey_level)                
                elif event.key == K_d:  
                    type_algorithme = "sad" 
                    im_result = algo_SAD(im_l_comp, im_r_comp, grey_level, 
                                         (off_x, off_y), window)
                    im_echelle = echelle(0.35)
                elif event.key == K_r:  
                    type_algorithme = "rank" 
                    im_result = algo_rank_SAD(im_l_comp, im_r_comp, grey_level,
                                              (off_x, off_y), window)
                    im_echelle = echelle(0.35)
                elif event.key == K_c:   
                    type_algorithme = "census"
                    im_result = algo_census_hamming(im_l_comp, im_r_comp, 
                                          grey_level, (off_x, off_y), window)
                    im_echelle = echelle(0.35)
                
                # Sauvegarde de l'echelle    
                elif event.key == K_e:                       
                    im_echelle = echelle(0.35)
                    pygame.image.save(im_echelle, "echelle_ratio.bmp")  
                # Sauvegarde de l'image calcculee    
                elif event.key == K_s:
                    message = type_algorithme + "_" + type_affichage + "_"
                    if type_algorithme == "simple":
                        message += str(thresh) + "_" 
                    else:
                        message += "w" + str(window) + "-" + \
                                   str(window) + "_"
                    message += str(off_x) + "-" + str(off_y) + ".bmp"
                    
                    pygame.image.save(im_result, message)  
                    
                    print("Sauvegarde", message)
                    #pygame.image.save(im_echelle, "echelle.bmp")
                    
                # Threshold difference
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
                # Window
                elif event.key == K_w:   
                    window = window - 2
                    if window < 1:
                        window = 1
                elif event.key == K_x:   
                    window = window + 2
                    if window > 29:
                        window = 29
                
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
        message = "offset(o: reset) : (" + str(off_x) + ", " + str(off_y) + ")" 
        print_GUI(DISPLAYSURF, message, (lim_print_x, lim_print_y + 50), font)
        message = "window(w/x) : (" + str(window) + ", " + str(window) + ")" 
        print_GUI(DISPLAYSURF, message, (lim_print_x + 400, lim_print_y + 50), font)
        message = "type affichage(a) : " + type_affichage + \
                  "   seuil(t/y) : " + str(thresh)
        print_GUI(DISPLAYSURF, message, (lim_print_x, lim_print_y + 80), font)
        message = "visualisation superposition(h) : " + \
                  ("active" if help else "non active")
        print_GUI(DISPLAYSURF, message, (lim_print_x, lim_print_y + 110), font)
        message = "DISP SIMPLE (F) SAD (D)  RANK (R)  CENSUS (C)"
        print_GUI(DISPLAYSURF, message, (lim_print_x, lim_print_y + 150), font)
        
        pygame.display.update()
        fpsClock.tick(FPS)
        
    
      
       
