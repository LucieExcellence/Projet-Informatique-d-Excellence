



import numpy as np
import random as rd
n=17
Bl=1
Blc=2
Ja=3
V=4
N=5
R=6
objectif=[(0,0),(16,12),(12,16),(12,4),(4,12),(4,0),(0,4)]
direction=[(0,1),(1,1),(1,0),(0,-1),(-1,-1),(-1,0)]
#Chaque Joueur est représenté par un chiffre
ORDI=1
ORDI_test=6


def init_plateau():
    plateau= -np.ones((n,n))
    for i in range(4,13):
        for j in range (4,13):
            plateau[i,j]=0 # on créer un carré de 0 pour la zone jouable
    for i in range (0,4):
        for j in range (4,5+i):
            plateau[i,j]=Bl # on place les pions bleus (1)
    for i in range (9,13):
        for j in range (4,5+i-9):
            plateau[i,j]=V # on place les pions verts (4)
    for i in range (9,13):
        for j in range (13,14+i-9):
            plateau[i,j]=N # on place les pions noirs (5)
    for i in range (4,8):
        for j in range (i-4,4):
            plateau[i,j]=Blc # on place les pions blancs (2)
    for i in range (4,8):
        for j in range (i+5,13):
            plateau[i,j]=Ja # on place les pions jaunes (3)
    for i in range (13,17):
        for j in range(9+i-13,13):
            plateau[i,j]=R # on place les pions rouges (6)
    return plateau
plateau = init_plateau()

def tableau_distance(): # renvoie un tableau contenant les distances de chaque case à la case d'arrivée. Ce tableau fonctionne sur le carré central ( vert contre jaune)
    l=9*[0]
    for i in range(len(l)):
        l[i]=9*[0] # on créer une liste de 9 sous listes
    for i in range(len(l)):
        for j in range (len(l)):
            l[j][i]=8-i+j # correspond à la distance entre la case voulue et la case objectif.
    return l


def initialisation_position_pion(plateau):
    #renvoie une liste contenant les coordonées des pions de chaque joueur
    positions_pions=[[]] # le numéro du joueur correspond au rang de la liste des positions de ses pions dans positions_pions
    (l,c)=np.shape(plateau)
    for joueur in range (1,7):
        pions_joueur=[]
        for i in range(0,l):
            for j in range(0,c):
                if plateau[i,j]==joueur:
                    pions_joueur.append((i,j))
        positions_pions.append(pions_joueur)  #on créé une liste de liste des positions des pions de chaque joueur
    return positions_pions


def debut_jeu(): #fonction qui lance toutes les fonctions d'initialisation
    P=init_plateau()
    T=tableau_distance()
    posi_pion=initialisation_position_pion(plateau)
    return [P,Bl,posi_pion,T]







def mouv_simple_possible(caseD,etat):
#renvoie une liste des coordonées des cases d'arrivées possibles pour un pion donné en un déplacement simple
    P,J, posi_pion, T = etat
    l,c = caseD
    mouv_simple=[]
    for (dl,dc) in direction:
        if -1<l+dl<17 and -1<c+dc<17 and P[l+dl,c+dc]==0:
        # on vérifie que la case d'arrivée est libre et dans le plateau
            mouv_simple.append([(l,c),(l+dl,c+dc)])
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

def deplace(etat,caseD,caseA): # on change les cases de depart et d'arrivée et la liste des positions du pion
    P,J,posi_pion,T =etat
    (i,j)=caseD
    (k,l)=caseA
    P[i,j], P[k,l]= P[k,l],P[i,j] #la case d'arrivée prend la valeur du joueur et celle de départ devient 0
    posi_pion[J].remove(caseD)  #on enleve le pion de départ de la liste des pions du joueur
    posi_pion[J].append(caseA) #on ajoute la position d'arrivée à la liste des pions du joueur


def saut(etat,L,caseD):#renvoie toutes les positions que va pouvoir atteindre un pion donné en echainant des sauts #pour L il faut rentrer une liste vide
    P,J,posi_pion,T = etat
    chemin=[]
    for caseA in mouv_saut_possible(caseD,etat):
        if caseA not in L: #on vérifie que l'on ne revient pas sur nos pas
            chs=saut(etat,L+[caseD],caseA) #on ajoute au chemin à ne pas emprunter la case d'où l'on vient et on recommence à chercher les sauts possibles depuis la case d'arrivée qui est la nouvelle de départ
            if len(chs)==0: #si il ne peut pas aller plus loin on note juste la case d'arrivée
                chemin.append([caseD,caseA])
            else :
                for ch in chs: #sinon pour chaque nouvelle case possible, on note le chemin que l'on a fait pour y arriver
                    chemin.append([caseD]+ch)
    return(chemin)

def toutes_les_positions(etat, caseD):#on fusionne les fonctionssaut et mouv_simple_possible pour avoir la liste de toutes les cases atteignable
    P,J, posi_pion,T= etat
    L=[]
    Y=[]
    S=saut(etat,L,caseD)
    for i in range(len(S)):
        Y.append([S[i][0],S[i][-1]])
    return  Y+ mouv_simple_possible(caseD,etat)

def translation(etat,caseD):# fonction qui renvoie, pour une case de départ sa case équivalente dans le carré central( vert contre jaune), on effectue une sorte de rotation du plateau pour facilité les calcules de distances (plus facile a calculer dans unn carré que dans un  losange.
    P , J , posi_pion , T = etat
    l,c = caseD
    if J==Bl or J==R:
        l,c=16-c,l-c+8
    if J == Blc or J== N:
        l,c= l-c+8,l
    return l,c

def distance(etat,caseD):# dans cette fonction on vient récupérer dans le tableau de distance calculé au début du programme la distance à l'objectif de son équivalent dans le carré central (vert contre jaune)
    P,J,posi_pion, T=etat
    l,c=translation(etat,caseD)
    if J== Bl or J==Blc or J==V:
        return T[l-4][c-4]# le -4 vient du fait que notre tableau de distance ne prend pas en compte les lignes et colonnes vides du plateau
    else:
        return 16-T[l-4][c-4]




def differentiel(caseD,caseA,etat): #calcul la distance parcourue par un pion
     P,J,posi_pion,T=etat
     return distance(etat,caseD)-distance(etat,caseA)


def meilleur_position(etat,caseD):# compare la distance parcourue pour toutes les cases atteignbles et choisit la meilleure case (celle qui aura avancer le plus)
    P,J,posi_pion,T=etat
    position= caseD
    d=-1
    toutes_les_posi= toutes_les_positions(etat, caseD)
    for i in range(len(toutes_les_posi)):#on calcule pour un pion le différentiel de chaque case atteignable. si D est supérieur à l'ancien différentiel, alors on remplace d par D et la case d'arrivée.
        caseDd,caseA=toutes_les_posi[i]
        D=differentiel(caseDd,caseA,etat)
        if D>d:
            position= caseA
            d=D
    return (position,d)



def meilleurpion(etat): #compare les différentiels entre les pions
    P,J,posi_pion,T=etat
    caseD=posi_pion[J][0]#on prend comme position initiale la position du premier pion du joueur J
    caseA,Maxdif=meilleur_position(etat,caseD) #on regarde pour ce pion quelle est la meilleure case d'arrivée et on note le différentiel entre cette meilleure case d'arrivée et la case de départ
    meilleur_depart=posi_pion[J][0]
    meilleure_arrivee=caseA
    for i in range(1,10):#pour tous les autres pions, on réalise la même manipulation, si le différentiel est meilleur que pour la caseD, on remplace alors l'ancien référentiel par le nouveau et on change aussi la caseD par la position du nouveau pion.
        caseD=posi_pion[J][i]
        caseA,difi=meilleur_position(etat,caseD)
        if difi>Maxdif:
            Maxdif=difi
            meilleur_depart=caseD
            meilleure_arrivee=caseA
    return meilleur_depart,meilleure_arrivee


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


def coup(etat):#fonction qui effectue en fonction du joueur qui joue le coup chosit par l'intelligence artificielle qui joue.
    P,J,posi_pion,T=etat
    if J==ORDI:
        return coup_ordi(etat)
    if J== ORDI_test:
        return hasard(etat)

def fin_du_jeu(etat):#fonction qui détermine si il y a un gagnant
    P,J,posi_pion,T=etat
    for i in range(10):
        pion=posi_pion[J][i]
        d= distance(etat,pion) #si tous les pions sont à une distance de l'arrivée inférieure ou égale à 4 alors ils sont tous rangés dans le triangle d'arrivée donc la partie est terminée
        if d>3:
            return False
    return True

def change_joueur(etat):# fonction qui permet d'effectuer la rotation des joueurs. Ici on decide de ne jouer qu'à deux joueurs, les bleus contre les rouges.
    P,J,posi_pion,T=etat
    if J== 1:
        etat[1]=6
    elif J==6:
        etat[1]=1


def prog_principal():#une fois lancée, cette fonction exécute une partie jusqu'à sa fin et renvoie le numéro du joueur qui à gagné.
    etat= debut_jeu()
    P,J,posi_pion,T=etat
    fini= False
    s=0
    while not fini:
        caseD,caseA= coup(etat)
        deplace(etat,caseD,caseA)
        fini=fin_du_jeu(etat)
        change_joueur(etat)
        s+=1
    print('bravo_joueur_'+ str(J),s)
    print(etat)
    
