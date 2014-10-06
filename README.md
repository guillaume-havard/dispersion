dispersion
==========

Test de génération d'image de profondeur à partir de deux images 
stéréoscopiques

Méthodes testées
----------------
* Comparaison simple
* SDA
* Rank
* Census

**Filtres :**  
Ajout de méthodes pour des filtres median/moyen.
Tester leur efficacité en étant utilisant sur les images de base avant les
calculs ou sur les images résultats.


Résultats
---------
La méthode de rank et de census donnent les meilleurs résultats.
Avec le census les zones sont bruitées mais avec un filtre le résultat est
satisfaisant.  
Pour être utilisable la méthode de census nécessite une fenetre assez large,
au moins 9.

L'utilisation de filtres avant les calculs ne semble cependant n'être
d'aucune aide.

**Décalage en Y**  
Si les images sont un peu décalé (1 pixel suffit) les calculs sont faussés.
Je pense que si les images ont des orientations différentes le résultat sera
le même.

C'est pour cela que nous n'arriverons pas avoir des résultats satisfaisant
avec nos images.

Lecture
-------
http://www-ist.cea.fr/publicea/exl-doc/200900004995.pdf
http://www.tyzx.com/PDFs/census.pdf
*census amélioré* http://www.researchgate.net/publication/228458512_Local_stereo_matching_algorithm_Using_small-color_census_and_sparse_adaptive_support_weight
https://siddhantahuja.wordpress.com/tag/stereo-matching/

Pour les images
---------------
http://vision.middlebury.edu/stereo/code/code/imagedirs.zip
