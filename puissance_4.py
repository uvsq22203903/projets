from tkinter import*
import random
import time

#création d'une fenêtre

fen=Tk()
fen.title("Puissance 4")
fen.geometry("900x900")
Zone=Canvas(fen,width=900,height=900,bg="white")
Zone.place(x=350,y=0)

#Déclaration des fonctions
victoire=False
notfull=True

def dessin_grille():
#dessine une grille de 7 colonnes et 6 lignes (8 traits verticaux et 7 traits horizontaux)
    x=100
    y=100
    while x<=800:
        x1=x
        y1=100
        x2=x
        y2=700
        Zone.create_line(x1,y1,x2,y2,width=2,fill="black")
        x+=100
    while y<=700:
        x1=100
        y1=y
        x2=800
        y2=y
        Zone.create_line(x1,y1,x2,y2,width=2,fill="black")
        y+=100

def affichage_final(victoire,vainqueur):
#affiche le joueur qui a gagné
    if victoire==True:
        if vainqueur==1:
            texteLabel = Label(fen, text = "Le joueur 1 a gagné !")
            texteLabel.pack()
        else:
            texteLabel = Label(fen, text = "Le joueur 2 a gagné !")
            texteLabel.pack()
    else:
        texteLabel = Label(fen, text = "Match nul, personne n'a gagné.")
        texteLabel.pack()

def initialisation():
#on définit aléatoirement qui commence et le tableau du jeu
    Who_start=random.randint(0,1)
    global joueur
    if Who_start==0:
        texteLabel = Label(fen, text = "J1 commence")
        texteLabel.pack()
        joueur=1
    else:
        texteLabel = Label(fen, text = "J2 commence")
        texteLabel.pack()
        joueur=2
    global jeu
    jeu=[[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0]]
    global victoire
    victoire=False
    global notfull
    notfull=True
    global fini
    fini=False

def attendre_clic(event):
#donne les coordonnées auxquelles l'utilisateur a cliqué
    global xclic
    global yclic
    global joueur
    global notfull
    global victoire
    global fini
    xclic=event.x
    yclic=event.y
    vainqueur=0
    if victoire==False and notfull==True:
#on s'assure que le joueur n'a pas cliqué sur une colonne remplie
        ligne=-1
        if ligne==-1:
            colonne=recherche_colonne(xclic)
            ligne=recherche_ligne(colonne,jeu)
        if ligne!=-1:
            dessin_jeton(ligne,colonne,joueur)
            actualiser_Jeu(colonne,ligne,joueur,jeu)
            vainqueur,victoire=controle_alignement(jeu,joueur)
            joueur=changement_joueur(joueur)
#on regarde si le tableau est rempli
            ligne=0
            colonne=0
            try:
                while jeu[colonne][ligne]!=0:
                    ligne+=1
                    if ligne==6:
                        colonne+=1
                        ligne=0
            except IndexError:
                notfull=False
    if (victoire and fini==False) or (notfull==False and fini==False):
        affichage_final(victoire,vainqueur)
        fini=True

def dessin_jeton(ligne,colonne,joueur):
#dessine un jeton en haut de la grille, de la couleur associée au joueur, puis le fait glisser jusqu'à sa ligne
    y=ligne*100+100
    x=colonne*100+100
    if joueur==1:
        jeton=Zone.create_oval(x, 0, x+100, 100, width=1, outline="red", fill="red")
        y_deplacement=700
        while y_deplacement!=y:
            Zone.move(jeton,0,5)
            y_deplacement-=5
            Zone.update()
            time.sleep(0.01)
    else:
        jeton=Zone.create_oval(x, 0, x+100, 100, width=1, outline="yellow", fill="yellow")
        y_deplacement=700
        while y_deplacement!=y:
            Zone.move(jeton,0,5)
            y_deplacement-=5
            Zone.update()
            time.sleep(0.01)

def actualiser_Jeu(colonne,ligne,joueur,jeu):
#complète le tableau à l'endroit où le joueur a joué en y mettant son numéro
    jeu[colonne][ligne]=joueur
    #return jeu

def recherche_colonne(x):
#recherche la colonne où l'utilisateur a cliqué
    colo=(x-100)//100
    return colo

def recherche_ligne(colo,j):
#recherche la ligne où l'utilisateur a cliqué et vérifie que la colonne n'est pas déjà complète
    i=0
    try:
        while j[colo][i]!=0:
            i=i+1
        return i
    except IndexError:
        texteLabel = Label(fen, text = "Cette colonne est complète.")
        texteLabel.pack()
        return -1

def controle_alignement(jeu,joueur):
#regarde s'il y a un alignement quelconque des pions d'un joueur
    vainqueur,victoire=alignement_horizontal(jeu,joueur)
    if victoire==False:
        vainqueur,victoire=alignement_vertical(jeu,joueur)
        if victoire==False:
            vainqueur,victoire=alignement_diagonal(jeu,joueur)
    return(vainqueur,victoire)

def alignement_vertical(jeu,joueur):
#regarde s'il y a un alignement de pions en vertical
    for col in range(7):
        for li in range(3):
            if jeu[col][li]==joueur and jeu[col][li+1]==joueur and jeu[col][li+2]==joueur and jeu[col][li+3]==joueur:
                vainqueur=joueur
                victoire=True
                return(vainqueur,victoire)
            else:
                vainqueur=0
                victoire=False
    if victoire==0:
        return(vainqueur,victoire)

def alignement_horizontal(jeu,joueur):
#regarde s'il y a un alignement de pions en horizontal
    for li in range(6):
        for col in range(4):
            if jeu[col][li]==joueur and jeu[col+1][li]==joueur and jeu[col+2][li]==joueur and jeu[col+3][li]==joueur:
                vainqueur=joueur
                victoire=True
                return(vainqueur,victoire)
            else:
                vainqueur=0
                victoire=False
    if victoire==0:
        return(vainqueur,victoire)

def alignement_diagonal(jeu,joueur):
#regarde s'il y a un alignement de pions en diagonal
    for li in range(3):
        for col in range(4):
            if jeu[col][li]==joueur and jeu[col+1][li+1]==joueur and jeu[col+2][li+2]==joueur and jeu[col+3][li+3]==joueur:
                vainqueur=joueur
                victoire=True
                return(vainqueur,victoire)
            elif jeu[col][li+3]==joueur and jeu[col+1][li+2]==joueur and jeu[col+2][li+1]==joueur and jeu[col+3][li]==joueur:
                vainqueur=joueur
                victoire=True
                return(vainqueur,victoire)
            else:
                vainqueur=0
                victoire=False
    if victoire==0:
        return(vainqueur,victoire)

def changement_joueur(joueur):
# on passe au joueur suivant
    if joueur==1:
        joueur=2
    else:
        joueur=1
    return joueur

#Programme principal
dessin_grille()
initialisation()
fen.bind("<Button-1>",attendre_clic)
fen.mainloop()