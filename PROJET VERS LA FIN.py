import numpy as np
import random as rd
n=17
Bl=1
Blc=2
J=3
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
            plateau[i,j]=J # on place les pions jaunes (3)
    for i in range (13,17):
        for j in range()
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
    return P,Bl,posi_pion,T

etat= debut_jeu() 
     

    

                  
def mouv_simple_possible(caseD,etat):  
#renvoie une liste des coordonées des cases d'arrivées possibles pour un pion donné en un déplacement simple
    P,J, posi_pion, T = etat 
    l,c = caseD
    mouv_simple_possible=[]
    for (dl,dc) in direction:
        if -1<l+dl<17 and -1<c+dc<17 and P[l+dl,c+dc]==0: 
        # on vérifie que la case d'arrivée est libre et dans le plateau 
            mouv_simple_possible.append((l+dl,c+dc))
    return mouv_simple_possible  
    

def mouv_saut_possible(caseD, etat):  
#renvoie une liste des coordonées des cases d'arrivées possibles pour un pion donné en un déplacement sauté
    P,J,posi_pion , T =etat
    l,c = caseD
    mouv_saut_possible=[]
    for (dl,dc) in direction:
        if 0<l+dl<16 and 0<c+dc<16 and P[l+dl,c+dc]!=0 and P[l+dl,c+dc]!=-1 and P[l+2*dl,c+2*dc]==0: 
        # enchainement case occupée/case vide dans le plateau 
            mouv_saut_possible.append((l+2*dl,c+2*dc))
    return mouv_saut_possible
    
def deplace(etat,caseD, caseA): # on change les cases de depart et d'arrivée et la liste des positions du pion
    P,J,posi_pion,T =etat
    (i,j)=caseD
    (k,l)=caseA
    P[i,j], P[k,l]= P[k,l],P[i,j] #la case d'arrivée prend la valeur du joueur et celle de départ devient 0
    pos[J].remove(caseD)  #on enleve le pion de départ de la liste des pions du joueur
    pos[J].append(caseA) #on ajoute la position d'arrivée à la liste des pions du joueur 
    
    
def saut(etat,L,caseD):#renvoie toutes les positions que va pouvoir atteindre un pion donné en echainant des sauts #pour L il faut rentrer une liste vide 
    P,J,posi_pion,T =etat
    chemin=[]
    for caseA in mouv_saut_possible(caseD,etat): 
        if caseA not in L: #on vérifie que l'on ne revient pas sur nos pas 
            chs=saut(P,L+[caseD],caseA) #on ajoute au chemin à ne pas emprunter la case d'où l'on vient et on recommence à chercher les sauts possibles depuis la case d'arrivée qui est la nouvelle de départ 
            if len(chs)==0: #si il ne peut pas aller plus loin on note juste la case d'arrivée
                chemin.append([caseD,caseA])
            else :
                for ch in chs: #sinon pour chaque nouvelle case possible, on note le chemin que l'on a fait pour y arriver
                    chemin.append([caseD]+ch)
    return(chemin)  

def toutes_les_positions(etat, caseD):#on fusionne les fonctionssaut et mouv_simple_possible pour avoir la liste de toutes les cases atteignable
    P,J, posi_pion,T= etat 
    L=[]
    return  saut(P,L,caseD)+ mouv_simple_possible(caseD,P)

def translation(etat,caseD):# fonction qui renvoie, pour une case de départ sa case équivalente dans le carré central( vert contre jaune)
    P , J , posi_pion , T = etat
    (l,c)=caseD
    if J==Bl or J==R:
        l,c=16-c,l-c+8
    if J == Blc or J== N:
        l,c= l-c+8,l 
    return l,c 

def distance(etat,caseD):
    P,J,posi_pion, T =etat
    l,c=translation(J,caseD)
    if J== Bl or Blc or V:
        return T[l-4][c-4]# le -4 vient du fait que notre tableau de distance ne prend pas en compte les lignes et colonnes vides du plateau 
    else:
        return 16-T[l-4][c-4]       
       

    
     
def differentiel(caseD,caseA,etat): #calcul la distance parcourue par un pion
     P,J,posi_pion,T=etat
     return distance(P, J,caseD,T)-distance(P,J,caseA,T)   


def meilleur_position(etat,L,caseD):# compare la distance parcourue pour toutes les cases atteignbles et choisit la meilleure case (celle qui aura avancer le plus)
    P,J,posi_pion,T=etat
    position= caseD
    d=0
    toutes_les_posi= toutes_les_positions(etat, caseD)
    for i in range( len(toutes_les_posi)):
        D=differentiel(caseD,toutes_les_posi[i],P,J,T)
        if D>d:
            position= toutes_les_posi[i]
            d=D
    return (position,d) 



def meilleurpion(etat): #compare les différentiels entre les pions
    P,J,posi_pion,T=etat
    caseD=posi_pion[J][0]
    positions_possibles=toutes_les_positions(etat,caseD)
    caseA,Maxdif=meilleur_position(etat,posi_pion[J][0],positions_possibles) 
    meilleurdepart=posi_pion[J][0]
    for i in range(1,10):
        caseD=posi_pion[J][i]
        positions_possibles=toutes_les_positions(P,posi_pion[J][i])
        caseA,difi=meilleur_position(J,P,T,caseD,positions_possibles)
        if difi>Maxdif:
            Maxdif=difi
            meilleur_depart=caseD
            meilleurearrivee=caseA
    return meilleurdepart,meilleurearrivée       

def hasard(etat):
    P,J,posi_pion,T=etat
    position=posi_pion[J]
    L=[]
    R=[0,1,2,3,4,5,6,7,8,9]
    A = rd.choice(R)
    for i in range(10):
        L.append(toutes_les_positions(etat,position[i]))
    I = L[A]
    a=rd.choice(I)
    return position_pion[J][A],a   #renvoie la position du pion choisi au hasard, une position possible de ce pion choisie au hasard.     

def coup_ordi(etat): 
    return meilleurpion(etat)

def coup_ordi_test(etat):
    return hasard(etat)

def coup(etat):
    P,J,posi_pion,T=etat
    if J==ORDI:
        return coup_ordi(etat)
    if J== ORDI_test:
        return coup_ordi_test(etat)
        
def fin_du_jeu(etat):
    P,J,posi_pion,T=etat
    for i in range(10):
        d= distance(etat,posi_pion[i],T) 
        if d>4:
            return True
        return False
        
def change_joueur(etat):
    P,J,posi_pion,T=etat
    if J== 1:
        J=6
    elif J==6:
        J=1
    return etat




def prog_principal():
    etat= debut_jeu()
    P,J,posi_pion,T=etat
    fini= False
    while not fini:
        coups= coup(etat)
        etat =deplace(etat,coups)
        fin_du_jeu(etat)
        etat= change_joueur(etat)
    print('bravo_joueur_'+ string(J))
               
               
               
               
               
               
               
