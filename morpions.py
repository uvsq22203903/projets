from tkinter import *
import random
####################
# Création fenêtre #
####################

root = Tk()
root.title("Morpions")
root.geometry("600x600")
zone = Canvas(root, width=600, height= 600, bg="white")
zone.place(x=0,y=0)


victory = False
notfull = True
def initialisation():
    start = random.randint(0,1)
    return

def dessin_grille():
    zone.create_line(200,0,200,600, width=1, fill= "black")
    zone.create_line(400,0,400,600,width= 1, fill="black")
    zone.create_line(0,200,600,200, width= 1, fill="black")
    zone.create_line(0,400,600,400, width= 1,fill="black")
    return

def dessin_jeton(ligne, colonne, joueur):
    y = ligne*200+200
    x = colonne*200+200
    if joueur ==2:
        rond = zone.create_oval(x, 0, x+200, width=1, outline="red")
    else:
        croix = zone.create_line()



def croix():
    zone.create_line(50,50,150,150,width=1, fill="red")
    zone.create_line(50,150,150,50, width=1, fill="red")
    return

def rond():
    return

def attendre_clic (jeu, event ,marque):
    # demande les coordonnées de la souris
    global xclic
    global yclic
    global notfull
    xclic=event.x
    yclic=event.y
    vainqueur=0
    if victory == False and notfull==True:
        dessin_jeton(xclic, yclic,joueur)
        print("clic")
    for i in range(jeu):
        for j in range (jeu):
            if marque == 0:
                jeu[i][j]
                return
            
def controle_colonne():
    return

def controle_ligne():
    return

def fermer_fenetre():
    root.destroy()

"""
jeu = [[0,0,0],[0,0,0],[0,0,0]]
print(jeu)
marque = 0
i,j=0,0
"""
#  print("Le but du jeu est d’aligner avant son adversaire 3 symboles identiques horizontalement, verticalement ou en diagonale. Chaque joueur a donc son propre symbole,cune croix pour l’un et un rond pour l’autre.")
# print(int(input("choisissez croix(1) ou rond(2) ")))



#######################
# PROGRAMME PRINCIPAL #
#######################
joueur = int(input("choisissez croix(1) ou rond(2) "))

dessin_grille()

croix()
# root.bind("<Button-1>",p)
root.mainloop()


