 #! /usr/bin/python3

"""
Affiche un histogramme d'une image.
"""
from dispersion import *

pygame.init()

#im = pygame.image.load('tsukubasad9x9disprange0-16color.png')
im = pygame.image.load('sad_hue_w3-3_0-0.bmp')
levels = image_to_levels(im, hue_level)

histo = histo_2D_int(levels)
tot = 0
hues = []
for key in iter(histo):
    print("{} : {}".format(key, histo[key]))
    tot += histo[key]
    hues.append(key)

hues.sort()
print(hues)    
print("nb pixels :", tot, "taille :", im.get_width(), "*", im.get_height(),
      "=", im.get_width()*im.get_height())
print("nb teintes :", len(histo))

pygame.quit()
