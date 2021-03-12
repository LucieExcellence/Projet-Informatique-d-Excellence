# CASTAN Nicolas  COIBA Simon CAMP Lucie FOLLIET Louise
# Le programme conçu permet de jouer différents mode's' de jeu. Le mode de jeu 1 permet de jouer contre l'ordinateur (5 intelligences artificielles), le mode 2 de faire jouer l'ordinateur tout seul, 5 joueurs jouants au hasard et 1 intelligemment. Enfin le mode de jeu 3 permet de faire jouer 6 ordinateurs intelligents.
#Lorsque vous jouez , vous pouvez le faire via l'interface graphique et pour lancer le jeu sans l'interface graphique prog_principal() permet de le faire dans la shell
#si vous jouez via l'interface graphiqe, le bouton mode de jeu trois lance la partie selon le mode de jeu trois automatiqument, si vous voulez jouer vous même contre l'ordinateur, effectuer clic gauche, clic droit comme indiqué.

import numpy as np
import random as rd
import math as m
from tkinter import *
n=17
#Chaque couleur de pion est représentée par un chiffre
Bl=1
Blc=2
Ja=3
V=4
N=5
R=6

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
            plateau[i,j]=Bl
            tr_B.append((i,j))
    for i in range (9,13):
        for j in range (4,5+i-9):
            plateau[i,j]=V 
            tr_V.append((i,j))
    for i in range (9,13):
        for j in range (13,14+i-9):
            plateau[i,j]=N 
            tr_N.append((i,j))
    for i in range (4,8):
        for j in range (i-4,4):
            plateau[i,j]=Blc 
            tr_Bl.append((i,j))
    for i in range (4,8):
        for j in range (i+5,13):
            plateau[i,j]=Ja 
            tr_Ja.append((i,j))
    for i in range (13,17):
        for j in range(9+i-13,13):
            plateau[i,j]=R
            tr_R.append((i,j))
    return [plateau,tr_B,tr_Bl,tr_Ja,tr_V,tr_N,tr_R]


def tableau_distance(): 
    '''renvoie un tableau contenant les distances de chaque case à la case d'arrivée. Ce tableau fonctionne sur le carré central ( vert contre jaune), il sera ensuite transposé pour chaque pion'''
    l=9*[0]
    for i in range(len(l)):
        l[i]=9*[0] # on créer une liste de 9 sous listes qui formeront le tableau
    for i in range(len(l)):
        for j in range (len(l)):
            l[j][i]=8-i+j # correspond à la distance entre la case voulue et la case objectif.
    return l

def translation(etat,caseD):
    '''fonction qui renvoie, pour une case de départ sa case équivalente dans le carré central(vert contre jaune), on effectue une translation du plateau pour faciliter les calculs de distances (plus facile a calculer dans un carré que dans un  losange.)'''
    P , J , posi_pion , T = etat
    l,c = caseD
    if J==Bl or J==R:
        l,c=16-c,l-c+8
    if J == Blc or J== N:
        l,c= l-c+8,l
    return l,c


def initialisation_position_pion(plateau):
    '''renvoie une liste contenant les coordonées des pions de chaque joueur'''
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


def debut_jeu(J):
    '''fonction qui lance toutes les fonctions d'initialisation et renvoie l'état du jeu'''
    P=init_plateau()
    T=tableau_distance()
    posi_pion=initialisation_position_pion(P[0])
    return [P[0],J,posi_pion,T]



# FONCTIONS EFFECTUANT LES MOUVEMENTS ET RETOURNANT TOUTES LES POSITIONS ATTEIGNABLES PAR UN PION

def mouv_simple_possible(caseD,etat):
    '''renvoie une liste de couples de coordonnées caseD/caseA atteignables pour une caseD donnée en un déplacement simple'''
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
                        mouv_simple.remove([(l,c),(l+dl,c+dc)]) #Si l'arrivée est dans un triangle adverse autre que celui d'en face, on ne peut pas y aller
    return mouv_simple


def mouv_saut_possible(caseD, etat):
    '''renvoie une liste de couples de coordonées caseD/caseA atteignables pour une caseD donnée en un déplacement sauté non enchaîné'''
    P,J,posi_pion , T =etat
    l,c = caseD
    mouv_saut=[]
    for (dl,dc) in direction:
        if 0<l+dl<16 and 0<c+dc<16 and P[l+dl,c+dc]!=0 and P[l+dl,c+dc]!=-1 and P[l+2*dl,c+2*dc]==0:
        # correspond à un enchainement case occupée/case vide dans le plateau
            mouv_saut.append((l+2*dl,c+2*dc))
    return mouv_saut



def saut(etat,L,caseD):
    '''renvoie toutes les chemins de coordonnées caseD/caseA que va pouvoir parcourir un pion donné en echainant des sauts, L correspond a la liste des positions où l'on est déja allé'''
    P,J,posi_pion,T = etat
    chemin=[]
    triangle=init_plateau()
    for caseA in mouv_saut_possible(caseD,etat):
        if caseA not in L: #on vérifie que l'on ne revient pas sur nos pas
            chs=saut(etat,L+[caseD],caseA) 
            if len(chs)==0: 
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


def toutes_les_positions(etat, caseD):
    '''on utilise les fonctions saut et mouv_simple_possible pour avoir la liste de tous les couples de coordonnées caseD/caseA atteignables pour une caseD donnée'''
    P,J, posi_pion,T= etat
    L=[]
    Y=[]
    S=saut(etat,L,caseD)
    for i in range(len(S)):
        for j in S[i]:
            Y.append([S[i][0],S[i][-1]])
            dernier=S[i][-1]#On reforme des couples caseD/caseA à partir des chemins renvoyé par saut
            S[i].remove(dernier)
    return  Y+ mouv_simple_possible(caseD,etat)




# STRATEGIE: ON CHOISI LE PION QUI VA SE RAPPROCHER LE PLUS DU SOMMET OPPOSÉ (L'OBJECTIF)

def distance(etat,caseD):
    '''récupère dans le tableau de distance la distance à l'objectif du pion donné par son équivalent dans le carré central via la fonction translation (vert contre jaune)'''
    P,J,posi_pion, T=etat
    l,c=translation(etat,caseD)
    if J== Bl or J==Blc or J==V:
        return T[l-4][c-4]# le -4 vient du fait que notre tableau de distance ne prend pas en compte les lignes et colonnes hors du plateau
    else:
        return 16-T[l-4][c-4]


def differentiel(caseD,caseA,etat): 
    '''calcule la distance parcourue par un pion'''
     P,J,posi_pion,T=etat
     return distance(etat,caseD)-distance(etat,caseA)


def meilleur_position(etat,caseD):
    '''on choisit la meilleure case atteignalble pour un pion donné (celle qui aura permis d'avancer le plus)'''
    P,J,posi_pion,T=etat
    d=0
    L=[caseD]
    toutes_les_posi= toutes_les_positions(etat, caseD)
    for i in range(len(toutes_les_posi)):
        caseDd,caseA=toutes_les_posi[i]
        D=differentiel(caseDd,caseA,etat)
        if D>d:
            L = [caseA]
            d=D
        elif D==d:
            L.append(caseA)
    position = rd.choice(L) #Si plusieurs positions permettent la même avancée on choisit au hasard
    return (position,d)



def meilleurpion(etat): 
    '''compare les différentiels entre les pions d'un joueur'''
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

def deplace(etat,caseD,caseA): 
    '''change les cases de depart,d'arrivée et la liste des positions du pion'''
    P,J,posi_pion,T =etat
    (i,j)=caseD
    (k,l)=caseA
    deplace_G(caseA,caseD,etat)
    P[i,j], P[k,l]= P[k,l],P[i,j] #la case d'arrivée prend la valeur du joueur et celle de départ devient 0
    if caseD not in posi_pion[J]:
        return 'Vous vous êtes trompé de joueur'
    posi_pion[J].remove(caseD)  #on enleve le pion de départ de la liste des pions du joueur
    posi_pion[J].append(caseA) #on ajoute la position d'arrivée à la liste des pions du joueur


def change_joueur(etat):
    '''fonction qui permet d'effectuer la rotation des joueurs. Ici on decide de ne jouer qu'à deux joueurs, les bleus contre les rouges.'''
    P,J,posi_pion,T=etat
    if etat[1]==6:
        etat[1]=0
    etat[1]+=1


# DEFINITION DES FONCTIONS QUI EFFECTUENT LES COUPS


def hasard(etat):
    '''renvoie un couple caseD/caseA possible aléatoirement pour l'ordinateur qui joue au hasard.'''
    P,J,posi_pion,T=etat
    position=posi_pion[J]
    caseD=rd.choice(position)
    while toutes_les_positions(etat,caseD)==[]:
        caseD=rd.choice(position)
    caseA=rd.choice(toutes_les_positions(etat,caseD))[-1]
    return caseD,caseA#renvoie la position du pion choisi au hasard, une position possible de ce pion choisie au hasard.


def coup_ordi(etat): 
    '''même fonction que meilleur pion mais pour rendre la Programme plus lisible'''
    return meilleurpion(etat)


def fin_du_jeu(etat):
    '''fonction qui détermine si la partie est gagnée'''
    P,J,posi_pion,T=etat
    for i in range(10):
        pion=posi_pion[J][i]
        d= distance(etat,pion) #si tous les pions sont à une distance de l'arrivée <3 alors ils sont tous rangés dans le triangle d'arrivée donc la partie est terminée
        if d>3:
            return False
    return True




def demande_coup(etat): 
    '''permet de jouer avec l'ordinateur sans l'interface graphique'''
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
    '''en fonction du mode de jeu, va faire jouer l'ordinateur'''
    P,J,posi_pion,T=etat
    if mode_de_jeu == 1:
        if J == J1:
            return demande_coup(etat)
        else:
            return meilleurpion(etat)
    if mode_de_jeu == 2:
        if J == J1:
            return  meilleurpion(etat)
        else:
            return  hasard(etat)
    if mode_de_jeu == 3:
        return meilleurpion(etat)


def prog_principal():
    '''une fois lancée, cette fonction exécute une partie jusqu'à sa fin et renvoie le numéro du joueur qui à gagné.'''
    mode_de_jeu=3
    joueurs = []
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
        print(etat[0])
    if etat[1]==1 :
        J=6
    else :
        J = etat[1]-1
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






def matrice(etat):#on modélise graphiquement le plateau
    P,J,posi_pion,T=etat
    for i in range(17):
        for j in range(17):
            c=int(P[i,j])
            if c!=-1:
                can.create_oval(j*taille,i*taille,j*taille+r,i*taille+r,fill=couleur[c])




def deplace_G(caseA,caseD,etat):# effectue le déplacement dans l'interface graphique
    P,J,posi_pion,T=etat
    yd,xd=caseD
    ya,xa=caseA
    c=int(P[yd,xd])# On recupere la couleur du pion à déplacer
    can.create_oval(xd*taille,yd*taille,xd*taille+r,yd*taille+r,fill='navajo white')
    can.create_oval(xa*taille,ya*taille,xa*taille+r,ya*taille+r,fill=couleur[c])



def clique_gauche(event,etat):
    global OKD,OKA,caseD,caseA
    yd=m.floor(event.x//taille)#associe les coordonnées du pixel selectionné à celles d'une case dans la matrice plateau
    xd=m.floor(event.y//taille)
    caseD=(xd,yd)
    OKD=True
    print(OKA,OKD)


def clique_droit(event,etat):
    global OKD,OKA
    ya=m.floor(event.x//taille)
    xa=m.floor(event.y//taille)
    caseA=(xa,ya)
    print(caseA)
    OKA=True
    fini=False
    if OKD and OKA:
        if caseD in etat[2][1]: #on verifie qu'on joue avec le bon joueur
            if [caseD,caseA] in toutes_les_positions(etat,caseD):#on vérifie que le coup est jouable
                deplace_G(caseA,caseD,etat)
                deplace(etat,caseD,caseA)
                fini=fin_du_jeu(etat)
                if fini :
                    print('bravo vous avez gagné')
                for j in range (2,7):
                    change_joueur(etat)
                    caseDO,caseAO=meilleurpion(etat)
                    deplace_G(caseAO,caseDO,etat)
                    deplace(etat,caseDO,caseAO)
                    fini=fin_du_jeu(etat)
                    if fini :
                        print('bravo joueur',j)
                change_joueur(etat)
                print(etat[1])
            else:
                print('recommencez le coup n\'est pas possible')
            OKA=False
            OKD=False
        else:
            print('vous vous êtes trompé de joueur')


#récupère les clics de souris
can.bind("<Button-3>",lambda event: clique_droit(event,etat))
can.bind("<Button-1>",lambda event: clique_gauche(event,etat))

bouton=Button(fen,text='Si vous désirez faire jouer le programme tout seul cliquez ici',command=lambda:prog_principal())
bouton.pack()


#Lance l'interface graphique

etat=debut_jeu(1)
can.pack()
OKA=False
OKD=False
CaseD=(0,0)
CaseA=(0,0)
matrice(etat)

fen.mainloop()


