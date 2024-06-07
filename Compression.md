# Compression d'images JPEG

##### Crédit
Projet de L1BI 2023 à l'UVSQ

Emma Cluzet

## Description
  Le but de ce projet est de créer des images au format JPEG. Nous implémenterons une version simplifiée, mais très proche de la réalité. 
  ### Manipulation d'image
  Nous allons changer la manière de représenter chaque pixel, en transformant l’information RGB en une information YCbCr. Il s’agit de trois valeurs qui représentent pour Y la luminance (luminosité) et Cb et Cr la
  chrominance (couleur). 
 
  Pour pouvoir traiter une image, nous avons besoin que ses dimensions soient des multiples de 8. Pour le
  garantir, il faut faire du remplissage (padding), c’est à dire qu’on va ajouter des lignes et des colonnes de pixel
  noirs en bas et à droite de l’image.
   
  *Si on a une image de dimension 15×21, on obtiendra une image de dimension 16×24 avec une ligne supplémentaire et trois colonnes supplémentaires.*

  L’oeil est moins sensible aux informations de chrominance que de luminance. Pour exploiter cela, nous allons réduire la quantité d’information des canaux Cb et Cr en leur appliquant un sous-échantillonnage.
  Il s'agit de remplacer deux pixels adjacents par la moyenne des deux pixels.
  Pour retrouver une matrice de la bonne dimension, à partir d’une matrice obtenue par sous-échantillonnage, on répète chaque pixel deux fois.

  ### Bloc et traitement
  Dans le format JPEG, l’image est décomposée en une grille de blocs de taille 8×8 qui seront traités indépendamment.
  C’est ce découpage qui créé des artefacts carrés caractéristiques du jpeg quand la compression est trop forte.

  Les blocs sont d’abord transformés en leur représentation par fréquence en utilisant une transformée en cosinus discrète. La fonction dct2 donne la représentation en fréquence d’une matrice carrée (qui est une matrice carrée de la même dimension) et la fonction idct2 calcule la fonction inverse.
 
  On implémente plusieurs modes de compression. Dans le mode 0, on garde les blocs transformés tels quels. Dans le mode 1, on impose un seuil aux coefficients. 
  Il s’agit de remplacer tous les coefficients plus petit que ce seuil par 0. On choisit un seuil qui permet de supprimer beaucoup de coefficients sans trop dégrader l’image. 
  Dans le mode 2, en plus du filtrage à seuil, on applique le sous-échantillonnage à la chrominance (Cb et Cr).

  ### Ecriture dans un fichier
  On écrit l'information sous forme de texte. 
  
  Pour ouvir un fichier en mode écriture *f = open(path, 'w')*. 
  Pour écrire une ligne *f.write('maligne\n')*. 
  Si on a une une variable numérique *k*, pour obtenir la chaîne de caractères représentant cette valeur, il suffit de faire *str(k)*.

  On écrit quatres lignes contenant les informations de notre image. La première contiendra le type de fichier : "SJPG". Le deuxième contiendra les dimensions de l'image dans l'ordre *hauteur* puis *largeur*, 
  séparées par un espace. La troisième ligne contiendra le mode de compression, par exemple *"mode 1"*. La quatrième ligne contiendra "RLE" pour run length encoding sinon "NORLE".

  Ensuite, on écrit le contenu des blocs, d'abord ceux de Y, puis ceux de Cb et enfin ceux de Cr. Chaque bloc est écrit sur une ligne.

  Pour améliorer la compression on va utiliser le run length encoding (RLE). Il s'agit d'une méthode similaire au code LZW. Quand un caractère est répété plusieurs fois de suite, on va écrire le caractère et son nombre de répétions. 
  Dans notre cas, ce sont les 0 qui sont répétés de nombreuses fois. A la place des *k* 0 consécutifs, on écrira *"♯k"* où k est un entier.

  ### Décompression

  A partir d'une image compressée par ce code on recréé l'image en RGB qu'on pourra par la suite afficher. 

  ### Optimisations (faculatif)
