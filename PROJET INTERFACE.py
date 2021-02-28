import numpy as np
import random as rd
import math as m
from tkinter import *
n=17
Bl=1
Blc=2
Ja=3
V=4
N=5
R=6
#Chaque Joueur est représenté par un chiffre
objectif=[(0,0),(16,12),(12,16),(12,4),(4,12),(4,0),(0,4)]
direction=[(0,1),(1,1),(1,0),(0,-1),(-1,-1),(-1,0)]

#FONCTIONS INITIALES

def init_plateau():
    plateau= -np.ones((n,n))
    tr_B=[] #Les listes Tr regroupent toutes les coordonées des triangles :utilisé pour empecher de pénetrer dans ces triangles adverses
    tr_V=[]
    tr_N=[]
    tr_Bl=[]
    tr_Ja=[]
    tr_R=[]
    for i in range(4,13):
        for j in range (4,13):
            plateau[i,j]=0 # on créer un carré de 0 pour la zone jouable
    for i in range (0,4):
        for j in range (4,5+i):
            plateau[i,j]=Bl # on place les pions bleus (1)
            tr_B.append((i,j))
    for i in range (9,13):
        for j in range (4,5+i-9):
            plateau[i,j]=V # on place les pions verts (4)
            tr_V.append((i,j))
    for i in range (9,13):
        for j in range (13,14+i-9):
            plateau[i,j]=5 # on place les pions noirs (5)
            tr_N.append((i,j))
    for i in range (4,8):
        for j in range (i-4,4):
            plateau[i,j]=Blc # on place les pions blancs (2)
            tr_Bl.append((i,j))
    for i in range (4,8):
        for j in range (i+5,13):
            plateau[i,j]=Ja # on place les pions jaunes (3)
            tr_Ja.append((i,j))
    for i in range (13,17):
        for j in range(9+i-13,13):
            plateau[i,j]=R # on place les pions rouges (6)
            tr_R.append((i,j))
    return [plateau,tr_B,tr_Bl,tr_Ja,tr_V,tr_N,tr_R]


def tableau_distance(): # renvoie un tableau contenant les distances de chaque case à la case d'arrivée. Ce tableau fonctionne sur le carré central ( vert contre jaune), il sera ensuite transposé pour chaque pion
    l=9*[0]
    for i in range(len(l)):
        l[i]=9*[0] # on créer une liste de 9 sous listes
    for i in range(len(l)):
        for j in range (len(l)):
            l[j][i]=8-i+j # correspond à la distance entre la case voulue et la case objectif.
    return l

def translation(etat,caseD):# fonction qui renvoie, pour une case de départ sa case équivalente dans le carré central( vert contre jaune), on effectue une sorte de rotation du plateau pour faciliter les calculs de distances (plus facile a calculer dans un carré que dans un  losange.)
    P , J , posi_pion , T = etat
    l,c = caseD
    if J==Bl or J==R:
        l,c=16-c,l-c+8
    if J == Blc or J== N:
        l,c= l-c+8,l
    return l,c


def initialisation_position_pion(plateau):
    #renvoie une liste contenant les coordonées des pions de chaque joueur
    positions_pions=[[]] #numéro du joueur correspond au rang de la liste de ses pions dans positions_pions
    (l,c)=np.shape(plateau)
    for joueur in range (1,7):
        pions_joueur=[]
        for i in range(0,l):
            for j in range(0,c):
                if plateau[i,j]==joueur:
                    pions_joueur.append((i,j))
        positions_pions.append(pions_joueur)
    return positions_pions


def debut_jeu(J): #fonction qui lance toutes les fonctions d'initialisation
    P=init_plateau()
    T=tableau_distance()
    posi_pion=initialisation_position_pion(P[0])
    return [P[0],J,posi_pion,T]



# FONCTIONS EFFECTUANT LES MOUVEMENTS ET RETOURNANT TOUTES LES POSITIONS ATTEIGNABLES PAR UNE CASE

def mouv_simple_possible(caseD,etat):
#renvoie une liste des coordonées des cases d'arrivées possibles pour un pion donné en un déplacement simple
    P,J, posi_pion, T = etat
    l,c = caseD
    mouv_simple=[]
    triangle=init_plateau()
    for (dl,dc) in direction:
        if -1<l+dl<17 and -1<c+dc<17 and P[l+dl,c+dc]==0 :
            # on vérifie que la case d'arrivée est libre et dans le plateau
            mouv_simple.append([(l,c),(l+dl,c+dc)])
            for i in range(1,7):
                if i!= J and i!= 7-J:
                    if (l+dl,c+dc) in triangle[i]:
                        mouv_simple.remove([(l,c),(l+dl,c+dc)]) #Si l'arrivée est dans un triangle adverse, on ne peut pas y aller
    return mouv_simple


def mouv_saut_possible(caseD, etat):
#renvoie une liste des coordonées des cases d'arrivées possibles pour un pion donné en un déplacement sauté
    P,J,posi_pion , T =etat
    l,c = caseD
    mouv_saut=[]
    for (dl,dc) in direction:
        if 0<l+dl<16 and 0<c+dc<16 and P[l+dl,c+dc]!=0 and P[l+dl,c+dc]!=-1 and P[l+2*dl,c+2*dc]==0:
        # enchainement case occupée/case vide dans le plateau
            mouv_saut.append((l+2*dl,c+2*dc))
    return mouv_saut



def saut(etat,L,caseD):#renvoie toutes les positions que va pouvoir atteindre un pion donné en echainant des sauts #L correspond à une liste vide une liste vide
    P,J,posi_pion,T = etat
    chemin=[]
    triangle=init_plateau()
    for caseA in mouv_saut_possible(caseD,etat):
        if caseA not in L: #on vérifie que l'on ne revient pas sur nos pas
            chs=saut(etat,L+[caseD],caseA) #on ajoute au chemin à ne pas emprunter la case d'où l'on vient et on recommence à chercher les sauts possibles depuis la case d'arrivée qui est la nouvelle case de départ
            if len(chs)==0: #si il ne peut pas aller plus loin on note juste la case d'arrivée
                chemin.append([caseD,caseA])
            else :
                for ch in chs: #sinon pour chaque nouvelle case possible, on note le chemin que l'on a fait pour y arriver
                    chemin.append([caseD]+ch)
    for L in chemin:
        for j in L:
            for i in range(1,7):
                if i!= J and i!= 7-J:
                    if j in triangle[i]:#Si case A est dans un triangle adverse, on ne peut pas y aller
                        L.remove(j)
    return(chemin)


def toutes_les_positions(etat, caseD):#on fusionne les fonctions saut et mouv_simple_possible pour avoir la liste de toutes les cases atteignables
    P,J, posi_pion,T= etat
    L=[]
    Y=[]
    S=saut(etat,L,caseD)
    for i in range(len(S)):
        for j in S[i]:
            Y.append([S[i][0],S[i][-1]])
            dernier=S[i][-1]
            S[i].remove(dernier)
    return  Y+ mouv_simple_possible(caseD,etat)




# STRATEGIE: ON CHOISI LE PION QUI VA SE RAPPROCHER LE PLUS DU SOMMET OPPOSÉ (L'OBJECTIF)

def distance(etat,caseD):# dans cette fonction on vient récupérer dans le tableau de distance calculé au début du programme la distance à l'objectif du pion donné de son équivalent dans le carré central (vert contre jaune)
    P,J,posi_pion, T=etat
    l,c=translation(etat,caseD)
    if J== Bl or J==Blc or J==V:
        return T[l-4][c-4]# le -4 vient du fait que notre tableau de distance ne prend pas en compte les lignes et colonnes vides du plateau
    else:
        return 16-T[l-4][c-4]


def differentiel(caseD,caseA,etat): #calcule la distance parcourue par un pion
     P,J,posi_pion,T=etat
     return distance(etat,caseD)-distance(etat,caseA)


def meilleur_position(etat,caseD):# compare la distance parcourue pour toutes les cases atteignables et choisit la meilleure case (celle qui aura permis d'avancer le plus)
    P,J,posi_pion,T=etat
    d=0
    L=[caseD]
    toutes_les_posi= toutes_les_positions(etat, caseD)
    for i in range(len(toutes_les_posi)):#on calcule pour un pion le différentiel de chaque case atteignable. si D est supérieur à l'ancien différentiel, alors on remplace d par D et la case d'arrivée.
        caseDd,caseA=toutes_les_posi[i]
        D=differentiel(caseDd,caseA,etat)
        if D>d:
            L = [caseA]
            d=D
        elif D==d:
            L.append(caseA)
    position = rd.choice(L) #Si plusieurs positions permettent la même avancée on choisit au hasard
    return (position,d)



def meilleurpion(etat): #compare les différentiels entre les pions d'un joueur
    P,J,posi_pion,T=etat
    caseD=posi_pion[J][0]#on prend comme position initiale la position du premier pion du joueur J
    caseA,Maxdif=meilleur_position(etat,caseD)
    meilleur_depart=posi_pion[J][0]
    meilleure_arrivee=caseA
    for i in range(1,10):
        caseD=posi_pion[J][i]
        caseA,difi=meilleur_position(etat,caseD)
        if difi>Maxdif: #On cherche le meilleur différenciel
            Maxdif=difi
            meilleur_depart=caseD
            meilleure_arrivee=caseA
    return meilleur_depart,meilleure_arrivee



#EFFECTUER LE DEPLACEMENT

def deplace(etat,caseD,caseA): # change les cases de depart,d'arrivée et la liste des positions du pion
    P,J,posi_pion,T =etat
    (i,j)=caseD
    (k,l)=caseA
    P[i,j], P[k,l]= P[k,l],P[i,j] #la case d'arrivée prend la valeur du joueur et celle de départ devient 0
    if caseD not in posi_pion[J]:
        return 'Vous vous êtes trompé de joueur'
    posi_pion[J].remove(caseD)  #on enleve le pion de départ de la liste des pions du joueur
    posi_pion[J].append(caseA) #on ajoute la position d'arrivée à la liste des pions du joueur


def change_joueur(etat):# fonction qui permet d'effectuer la rotation des joueurs. Ici on decide de ne jouer qu'à deux joueurs, les bleus contre les rouges.
    P,J,posi_pion,T=etat
    if etat[1]==6:
        etat[1]=0
    etat[1]+=1


# DEFINITION DES FONCTIONS QUI EFFECTUENT LES COUPS


def hasard(etat):#fonction qui determine au hasard un coup a jouer pour l'ordinateur qui joue de manière aléatoire.
    P,J,posi_pion,T=etat
    position=posi_pion[J]
    caseD=rd.choice(position)
    while toutes_les_positions(etat,caseD)==[]:
        caseD=rd.choice(position)
    caseA=rd.choice(toutes_les_positions(etat,caseD))[-1]
    return caseD,caseA#renvoie la position du pion choisi au hasard, une position possible de ce pion choisie au hasard.


def coup_ordi(etat): #mëme fonction que meilleur pion mais pour rendre la Programme plus lisible
    return meilleurpion(etat)


def fin_du_jeu(etat):#fonction qui détermine si il y a un gagnant
    P,J,posi_pion,T=etat
    for i in range(10):
        pion=posi_pion[J][i]
        d= distance(etat,pion) #si tous les pions sont à une distance de l'arrivée inférieure ou égale à 4 alors ils sont tous rangés dans le triangle d'arrivée donc la partie est terminée
        print(d,pion)
        if d>3:
            return False
    return True




def demande_coup(etat):
    P,J,posi_pion,T=etat
    fini=False
    while not fini:
        lD = int(input("sur quelle ligne se trouve le pion que vous voulez déplacer ?"))
        cD=int(input("sur quelle colonne se trouve le pion que vous voulez déplacer ?"))
        caseD= (lD,cD)
        lA = int(input("sur quelle ligne voulez-vous déplacer ce pion ?"))
        cA=int(input("sur quelle colonne voulez-vous déplacer ce pion ?"))
        caseA= (lA,cA)
        if [caseD,caseA] in toutes_les_positions(etat, caseD):
            fini=True
            return caseD, caseA
        else:
            fini=False
            print('Le coup est impossible')

def coup(etat,mode_de_jeu, J1):
    P,J,posi_pion,T=etat
    if mode_de_jeu == 1:
        if J == J1:
            return demande_coup(etat)
        else:
            return meilleurpion(etat)
    if mode_de_jeu == 2:
        if J == J1:
            return  demande_coup(etat)
        else:
            return  hasard(etat)
    if mode_de_jeu == 3:
        return meilleurpion(etat)


def prog_principal():#une fois lancée, cette fonction exécute une partie jusqu'à sa fin et renvoie le numéro du joueur qui à gagné.
    mode_de_jeu = int(input("Quel est le mode de jeu ?")) #rentrer : [humain,ordi](1) ou [humain,ordi_hazard](2) ou [ordi , ordi_hazard](3)
    joueurs = []
    if mode_de_jeu != 3:
        J1 = input("Choississez la couleur de vos pions")#Rentrer un entier entre 1 et 6
        J1=int(J1)
        J2 = 7-J1
    else:
        J1 = rd.randint(1,6)
        J2 = 7-J1
    joueurs.append(J1)
    joueurs.append(J2)
    J = rd.choice(joueurs) #choix du joueur qui commence la partie au hasard
    etat= debut_jeu(J)
    P,J,posi_pion,T=etat
    fini= False
    S=0
    while not fini:
        caseD, caseA = coup(etat,mode_de_jeu,J1)
        deplace(etat,caseD,caseA)
        fini=fin_du_jeu(etat)
        change_joueur(etat)
        S+=1
    if etat[1]==1 :
        J=6
    else :
        J = etat[1]-1
    print(etat)
    print('bravo_joueur_',J,S)

#INTERFACE GRAPHIQUE

#On crée une fenêtre


fen = Tk()
fen.title("Jeu des dames chinoises")
fen.geometry("650x650")
fen.minsize(500,500)
bienvenue=Label(fen,text='Bienvenue !Vous êtes le joueur bleu',fg='red')
regles=Label(fen,text='Pour jouer selectionnez un pion de départ avec le clic gauche et une case arrivée avec le clic droit',fg='red')
bienvenue.pack()
regles.pack()
taille=35
r=33
couleur=['navajo white','blue','white','yellow','green','black','red']


can = Canvas(fen, width=600, height=600, bg='navajo white')






def matrice(etat):
    P,J,posi_pion,T=etat
    for i in range(17):
        for j in range(17):
            c=int(P[i,j])
            if c!=-1:
                can.create_oval(j*taille,i*taille,j*taille+r,i*taille+r,fill=couleur[c])




def deplace_G(caseA,caseD,etat):# échange la couleur des pions de départ et d'arrivée
    P,J,posi_pion,T=etat
    yd,xd=caseD
    ya,xa=caseA
    print(yd,xd)
    print(P)
    c=int(P[yd,xd])# On recupere la couleur de départ
    can.create_oval(xd*taille,yd*taille,xd*taille+r,yd*taille+r,fill='navajo white')
    can.create_oval(xa*taille,ya*taille,xa*taille+r,ya*taille+r,fill=couleur[c])




def clique_gauche(event,etat):
    global OKD,OKA,caseD,caseA
    yd=m.floor(event.x//taille)
    xd=m.floor(event.y//taille)
    caseD=(xd,yd)
    OKD=True
    print(caseD)
    print(OKA,OKD)
    if OKD and OKA: #quand on a recuperé les deux cases, on effectue le déplacement et on fait jouer l'ordinateur
        if [caseD,caseA] in toutes_les_positions(etat,caseD):
            deplace_G(caseA,caseD,etat)
            deplace(etat,caseD,caseA)
            fini= False
            fini=fin_du_jeu(etat)
            if fin_du_jeu==True:
                fin=Label(fen,text='bravo vous avez gagné',fg='red')
                fin.pack()
            for _ in range (5):
                change_joueur(etat)
                caseDO,caseAO=meilleurpion(etat)
                deplace_G(caseAO,caseDO,etat)
                deplace(etat,caseDO,caseAO)
                change_joueur(etat)
                fini= False
                fini=fin_du_jeu(etat)
                if fin_du_jeu==True:
                    fin=Label(fen,text='Vous avez perdu',fg='red')
                    fin.pack()
        else:
            print('recommencez le coup n\'est pas possible')
        OKA=False
        OKD=False

def clique_droit(event,etat):
    global OKD,OKA
    ya=m.floor(event.x//taille)
    xa=m.floor(event.y//taille)
    caseA=(xa,ya)
    print(caseA)
    OKA=True
    if OKD and OKA:
        if [caseD,caseA] in toutes_les_positions(etat,caseD):
            deplace_G(caseA,caseD,etat)
            deplace(etat,caseD,caseA)
            fini= False
            fini=fin_du_jeu(etat)
            if fin_du_jeu==True:
                fin=Label(fen,text='bravo vous avez gagné',fg='red')
                fin.pack()
            for _ in range (5):
                change_joueur(etat)
                caseDO,caseAO=meilleurpion(etat)
                deplace_G(caseAO,caseDO,etat)
                deplace(etat,caseDO,caseAO)
                change_joueur(etat)
                fini= False
                fini=fin_du_jeu(etat)
                if fin_du_jeu==True:
                    fin=Label(fen,text='Vous avez perdu',fg='red')
                    fin.pack()
        else:
            print('recommencez le coup n\'est pas possible')
        OKA=False
        OKD=False



#récupère les clics de souris
can.bind("<Button-3>",lambda event: clique_droit(event,etat))
can.bind("<Button-1>",lambda event: clique_gauche(event,etat))



#Lance l'interface graphique
etat=debut_jeu(1)
can.pack()
OKA=False
OKD=False
CaseD=(0,0)
CaseA=(0,0)
matrice(etat)

fen.mainloop()