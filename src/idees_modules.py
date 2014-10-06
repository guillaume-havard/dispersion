 #! /usr/bin/python3

"""
Pas utilise pour le moment
"""

def test_computation(image1, image2, offset, functions):
    """
    Fonction temporaire pour tester les fonctions
    
    im_l [in] : pygame.Surface left image
    im_r [in] : pygame.Surface right image
    offset [in] : set with x and y offset for dispersion computation
    functions[in] : set with a len of 3 
                    0 -> set of (filter, window)
                    1 -> (comparison, window)
                    2 -> (color, window)
                    
    return : pygame.Surface dispersion image 
    """

    # comparaison taille
    # verification functions
    
    im_res = image1.copy()
    im_res.fill((0, 0, 0))
    
    pix_image1 = pygame.PixelArray(image1)
    pix_image2 = pygame.PixelArray(image2)
    pix_res = pygame.PixelArray(im_res)
    
    # filters
    base1 = pix_image1
    base2 = pix_image2
    for prep_filter, win  in functions[0]:
        new1 = []
        new2 = []
        for x in range(image1.get_width()):
            new1.append([])
            new2.append([])
            for y in range(image1.get_height()):
                new1[x].append(prep_filter(base2, (x, y), win))
                new2[x].append(prep_filter(base2, (x, y), win))
        
        base1 = new1
        base2 = new2
    
    # comparaison
    comp = []
    for x in range(image1.get_width()):
        comp.append([])
        for y in range(image1.get_height()):
            comp[x].append(functions[1][0](base1, base2, (x,y), functions[1][1]))
    
    # mise au propre
    maximum = 255 #max(comp)
    for x in range(image1.get_width()):
        for y in range(image1.get_height()):
            pix_res[x][y] = functions[2](comp, (x, y), maximum)
    
    
    del pix_image1
    del pix_image2
    del pix_res
    
    
    # /!\ à la gestion des fenetres
    
    return im_res

# Chaque fois entre = 1 pix, sortie = 1 pix.
def filter_(image, pos, windows):
    """    
    image [in] :
    pos [in] : position of the pixel to filter
    windows [in] : windows for the res computation
    
    return : Int
    """    
    pass
#def comparaison_(images, pos, windows): # ?? Comme ca toutes les func on les
# memes arguments.
def comparaison_(image1, image2, pos, windows):
    """    
    image [in] : Int
    pos [in] : position of the pixel to filter
    windows [in] : windows for the res computation
    
    return : Int
    """
    
    
    pass
def color_(image, pos, maximum):
    """    
    image1 [in] :
    image2 [in] :
    pos [in] : position of the pixel to filter
    windows [in] : windows for the res computation
    
    return : pygame.Color
    """
    pass
    

# --- Test dispersion sur l'OE ---

def filter_grey_level(image, pos, windows):
    """    
    image [in] :
    pos [in] : position of the pixel to filter
    windows [in] : windows for the res computation
    
    return : Int
    """
    return (image[pos[0]][pos[1]])
    
def comparaison_levels(image1, image2, pos, windows):
    """    
    image [in] :
    pos [in] : position of the pixel to filter
    windows [in] : windows for the res computation
    
    return : Int
    """
    ret = 0
    
    if abs(p_l - p_r) < threshold:                    
        pix_disp[x][y] = level_to_color((p_l + p_r) / 2)
    
def color_level_to_hue(image, pos, maximum):
    """    
    image1 [in] :
    image2 [in] :
    pos [in] : position of the pixel to filter
    windows [in] : windows for the res computation
    
    return : pygame.Color
    """
    pass    

