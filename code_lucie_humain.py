## Joueur affronte un ordi
def debut_jeu(): #fonction qui lance toutes les fonctions d'initialisation
    P=init_plateau()
    T=tableau_distance()
    joueurs = []
    mode_de_jeu = input("Quel est le mode de jeu ?") #rentrer : [humain,ordi](1) ou [humain,ordi_hazard](2) ou [ordi , ordi_hazard](3)
    if mode_de_jeu != 3:
        J1 = input("Choississez la couleur de vos pions")#Rentrer un entier entre 1 et 6
        J2 = 7-J1
    else:
        J1 = rd.randint(1,6)
        J2 = 7-J1
    joueurs.append(J1)
    joueurs.append(J2)
    posi_pion=initialisation_position_pion(plateau)
    J = rd.choice(joueurs) #choix du joueur qui commence la partie au hasard
    return J,posi_pion,T

def demande_coup(etat):
    P,J,posi_pion,T=etat
    while False:
        CaseD = input("Quel poion voulez-vous déplacer ?")
        CaseA = input("Où voulez-vou sdéplacer ce pion ?")
        if CaseA is in toutes_les_positions(etat, caseD):
            return caseD, caseA
        else:
            print('Le coup est impossible')

def coup(etat):
    P,J,posi_pion,T=etat
    if mode_de_jeu == 1:
        if J = J1:
            coup = demande_coup(etat)
        else:
            coup = meilleurpion(etat)
    if mode_de_jeu == 2:
        if J = J1:
            coup = demande_coup(etat)
        else:
            coup = hasard(etat)
    if mode_de_jeu == 3:
        if J = J1:
            coup = meilleurpion(etat)
        else:
            coup = hasard(etat)






