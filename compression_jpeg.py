"""
Le but de ce projet est de créer des images au format JPEG. On teste le code avec des images compressées.
Une fois les images chargées, on obtient un tableau numpy à trois dimensions.
Soit une matrice dont les éléments sont des triplets d'entiers dans [0, 2555] qui représentent les intensités en rouge, vert, bleu (RGB).

"""

import numpy as np
import PIL as pil
from PIL import Image
from tkinter import filedialog
from tkinter import simpledialog
from random import*
from math import sqrt, log10
import spicy as sp

# -----------------------
# Définition de fonctions
# -----------------------


def save(matPix, filename):
    Image.fromarray(matPix).save(filename)

def load(filename):
    return np.array(pil.Image.open(filename))


# Fonction qui calcule la proximité de deux images
# Deux images identiques ont un PSNR de 100, des images très proches ont un PSNR d'environ 40


def psnr(original, compressed):
    mse = np.mean((original - compressed) ** 2)
    max_pixel = 255.0
    psnr = 20 * log10(max_pixel / sqrt(mse))
    return psnr


# Fonction qui donne la représentation en fréquence d'une matrice carrée

def dct2(a):
    return sp.fft.dct(sp.fft.dct(a, axis=0, norm='ortho'), axis=1, norm='ortho')

# Fonction qui calcule la fonction inverse
def idct2(a):
    return sp.fft.idct(sp.fft.idct(a, axis=0, norm='ortho'), axis=1, norm='ortho')


# Transforme une image RGB en une image YCbCr
# Y représente la luminance
# Cb et Cr représentent la chrominance


def YCbCr(mat_img):
    MatYCbCr = np.empty(mat_img.shape)
    for i in range(mat_img.shape[0]):
        for j in range(mat_img.shape[1]):
            Y = 0.299*mat_img[i,j,0] + 0.587*mat_img[i,j,1] + 0.114*mat_img[i,j,2]
            Cb = -0.1687*mat_img[i,j,0] - 0.3313*mat_img[i,j,1] + 0.5*mat_img[i,j,2] + 128
            Cr = 0.5*mat_img[i,j,0] - 0.4187*mat_img[i,j,1] - 0.0813*mat_img[i,j,2] + 128
            MatYCbCr[i,j]=(Y,Cb,Cr)
    return MatYCbCr


# Transforme une image YCbCr en une image RGB.
# Les valeurs sont des entiers dans [0,255] et pourront être codé sur un octet.


def RGB(mat):
    MatRGB = np.empty(mat.shape, dtype= np.uint8)
    for i in range(mat.shape[0]):
        for j in range(mat.shape[1]):
            R = mat[i,j,0] + 1.402 * (mat[i,j,2] - 128)
            G = mat[i,j,0] - 0.34414 * (mat[i,j,1] - 128) - 0.71414 * (mat[i,j,2] - 128)
            B = mat[i,j,0] + 1.772 * (mat[i,j,1] - 128)
            MatRGB[i,j]=(np.uint8(np.clip(R,0.0,255.0)), np.uint8(np.clip(G,0.0,255.0)), np.uint8(np.clip(B,0.0,255.0)))
    return MatRGB


"""
Pour traiter une image, on a besoin que ses dimensions soient des multiples de 8, 
on va rajouter des lignes et des colonnes noires en bas et à droite de l'image.
"""
# Fonction qui réalise ce padding ainsi que celle qui l’élimine et vérifier que
# l’application de ces deux transformations laissent l’image inchangée.


def padding(mat):
    global nb_ligne
    global nb_colonne
    nb_ligne = mat.shape[0] % 8
    nb_colonne = mat.shape[1] % 8
    MatPad = np.empty((mat.shape[0] + nb_ligne, mat.shape[1] + nb_colonne, 3), dtype= np.uint8)
    for i in range(mat.shape[0]):
        for j in range(mat.shape[1]):
            MatPad[i,j] = mat[i,j]
            
    return MatPad


def delete_padding(mat, nb_ligne, nb_colonne):
    MatUnpad = np.empty((mat.shape[0] - nb_ligne, mat.shape[1] - nb_colonne,3), dtype= np.uint8)
    for i in range(MatUnpad.shape[0]):
        for j in range(MatUnpad.shape[1]):
            MatUnpad[i,j] = mat[i,j]
    return MatUnpad


# Fonction qui sous-échantillonne une matrice et renvoie une matrice deux fois plus petite
# On réduit la quantité d'informations des canaux Cb et Cr : remplacer deux pixels adjacents par la moyenne de deux pixels

def sous_echantillonage(matrice):
    nh =  matrice.shape[0]  # nh --> new height (hauteur)
    nw = matrice.shape[1]//2  # nw --> new width (largeur)
    newMat = np.empty((nh, nw,3), dtype= np.uint8)
    for i in range(nh):
        for j in range(0,nw,1):
            newMat[i,j] = (matrice[i,j*2] + matrice[i,j*2+1])

    return newMat

"""
Pour retrouver une matrice de la bonne dimension, à partir d'une matrice obtenue par sous-échantillonnage, on répète chaque pixel deux fois
"""
# Fonction qui multiplie par deux la deuxième dimension d’une matrice


def anti_sous_echantillonage(matrice):
    nh =  matrice.shape[0]
    nw = matrice.shape[1]*2
    newMat = np.empty((nh, nw,3), dtype= np.uint8)
    for i in range(nh):
        for j in range(0,nw-1,1):
            newMat[i,j] = matrice[i,j//2]
            newMat[i,j+1] = matrice[i,j//2]
    return newMat

"""
Dans le format JPEG, l'image est découpée en une grille de bloc 8x8 qui seront traités indépendamment.
"""
# Fonction qui découpe cette matrice en blocs 8 x 8 et les stocke dans une liste. L'ordre des blocs correspond à l'ordre de lecture d'une image.

# découpe 3 par 8
def decoupe(matrice):
    mat_decoupe = []
    for i in range(0, matrice.shape[1], 8):
        for j in range(0, matrice.shape[0], 8):
            mat_decoupe.append(matrice[i:i+8, j:j+8])
    mat_decoupe=np.array(mat_decoupe)
    return mat_decoupe


# fonction qui applique la transformée à chaque bloc d’une liste.


def frequence(liste_bloc):
    liste=[]
    for i in liste_bloc:
        liste.append(dct2(i))
    liste=np.array(liste)
    return liste

def pas_frequence(liste_bloc):
    liste = []
    for i in liste_bloc:
        liste.append(int(idct2(i)))
    liste=np.array(liste)
    return liste


"""
On implémente plusieurs modes de compression. Dans le mode 0, on garde les blocs transformés tels quels.
Dans le mode 1, on impose un seuil aux coefficients (remplacer tous les coefficients plus petit que ce seuil par 0)
"""
# filtrage des coefficients des blocs selon un seuil donné en argument.

def coefficient(liste_bloc,seuil):
    liste=[]
    for b in liste_bloc :
        b[(b>0) & (b < seuil)] = 0 
        b[(b<0) & (b > -seuil)] = 0 
        liste.append(b)
    
    return liste


def compression_0(image):
    yCbCr_image = YCbCr(image)
    padded_image = padding(yCbCr_image)
    blocs = decoupe(padded_image)

    return blocs

def compression_1(image, seuil):
    yCbCr_image = YCbCr(image)
    padded_image = padding(yCbCr_image)
    bloc = decoupe(padded_image)
    bloc[np.abs(bloc) < seuil] = 0

    return bloc





















# -------------------
# Programme Principal
# -------------------

test = load('./test.png')

test2 = YCbCr(test)
test3 = RGB(test2)
Image.fromarray(test2, 'YCbCr').show()
Image.fromarray(test3, 'RGB').show()

# ----------------------

pad = padding(test)
pad2 = delete_padding(pad, nb_ligne, nb_colonne)
Image.fromarray(pad2, 'RGB').show()

# ----------------------

se= sous_echantillonage(test)
Image.fromarray(se, 'RGB').show()
ase= anti_sous_echantillonage(se)
Image.fromarray(ase, 'RGB').show()
# ----------------------

bloc = decoupe(test)
print(bloc)

# ---------------------

freq = frequence(test)
print(freq)
pas_freq = pas_frequence(freq)
print(pas_freq)

# --------------------

coeff = coefficient(pas_freq, 10)
print(coeff)

# ---------------------

compress0 = compression_0(test)
compress1 = compression_1(test, 10)
print(compress0)
print(compress1)
