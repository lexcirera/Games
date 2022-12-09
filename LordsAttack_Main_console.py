import random as rd
import time as tm

#paramètres carte:
taille_map=50
Liste_Artefacts=[["Artefact","Puissance divine"],["Artefact","Coalition divine"],["Artefact","Elevation divine"]]
nbmax_artefacts=4 #par tour
bordurex,bordurey=taille_map,taille_map


#paramètres initiaux joueurs:
nb_joueurs=20
armée=50000
puissance=1
lvl_joueur=1
lvl_troupes=1


##
#créations des joueurs:


def start():
    for i in range (taille_map):
        map.append(taille_map*[False])
    for i in range (1,nb_joueurs+1):
        numero="joueur"+str(i)
        x,y=rd.randint(0,bordurex-1),rd.randint(0,bordurey-1)
        while map[y][x] !=False:
            x,y=rd.randint(0,bordurex-1),rd.randint(0,bordurey-1)
        Joueur=[numero,x,y,lvl_joueur,puissance,armée,lvl_troupes,[],0,0,0]
        map[y][x]=Joueur
        Liste_Joueurs.append(Joueur)

def stats(joueur):
    nom=joueur[0]
    x,y=joueur[1],joueur[2]
    niveau=joueur[3]
    puissance=joueur[4]
    armée=joueur[5]
    niv_troupes=joueur[6]
    puipui,coa,elev=0,0,0
    if len(joueur[7])!=0:
        for artefact in joueur[7]:
            if artefact=="Puissance divine":
                puipui+=1
            if artefact=="Coalition divine":
                coa+=1
            if artefact=="Elevation divine":
                elev+=1
    kills=joueur[8]
    victoires=joueur[9]
    défaites=joueur[10]
    print("Nom: ", nom)
    print("Coordonnées: ","x: ",x," y: ",y)
    print("Niveau du joueur: ",niveau)
    print("Puissance du joueur: ",puissance)
    print("Taille de l'armée: ",armée)
    print("Niveau des troupes: ",niv_troupes)
    print("Artefacts trouvés: ",puipui," Puissance divine, ",coa," Coalition divine, ",elev," Elevation divine")
    print("Nombre joueurs tués: ",kills)
    print("Nombre batailles gagnées: ", victoires)
    print("Nombre batailles perdues: ",défaites)





#création artefacts
def crea_artefacts():
    nbartefacts=rd.randint(0,nbmax_artefacts)
    print(nbartefacts," nouveaux artefacts ont été placés sur la map")
    for i in range(0,nbartefacts):
        artefact=Liste_Artefacts[rd.randint(0,(len(Liste_Artefacts)-1))]
        x,y=rd.randint(0,len(map)-1),rd.randint(0,len(map)-1)
        while map[y][x] !=False:
            x,y=rd.randint(0,bordurex-1),rd.randint(0,bordurey-1)
        map[y][x]=artefact

#mélanger la liste des joueurs
def melanger_joueurs(Liste_joueurs):
    Liste_melange=[]
    n=len(Liste_joueurs)
    for i in range (n):
        pas=rd.randint(0,len(Liste_joueurs)-1)
        Liste_melange.append(Liste_joueurs[pas])
        del Liste_joueurs[pas]
    return Liste_melange


#deplacement joueurs
def deplacer_joueurs(Liste_joueurs):
    nbjoueurs=len(Liste_joueurs)
    for i in range (nbjoueurs):
        joueur=Liste_joueurs[i]
        x,y=joueur[1],joueur[2]
        nx,ny=rd.randint(0,taille_map-1),rd.randint(0,taille_map-1)
        while map[ny][nx] !=False:
            nx,ny=rd.randint(0,taille_map-1),rd.randint(0,taille_map-1)
        joueur[1]=nx
        joueur[2]=ny
        map[ny][nx]=joueur
        map[y][x]=False



#recherche d'artefacts
def recherche_artefacts(Joueur):
    x,y,lvl=Joueur[1],Joueur[2],Joueur[3]
    Artefacts=[]
    Artefacts_diff=[]
    for i in range (x-lvl,x+lvl+1):
        for j in range(y-lvl,y+lvl+1):
            if i<0: i=0
            if i>(len(map)-1): i=len(map)-1
            if j<0: j=0
            if j>(len(map)-1): j=len(map)-1
            if map[j][i] !=False:
                artefact_potentiel=map[j][i]
                if artefact_potentiel[0] =="Artefact":
                    coordonnées=[i,j]
                    Artefacts.append(coordonnées)
    for i in Artefacts:
        if i not in Artefacts_diff and i[0] !=Joueur[0]:
            Artefacts_diff.append(i)

    return Artefacts_diff

def artefact_plusproche(Joueur,Artefacts):
    dmin=taille_map
    x,y=Joueur[1],Joueur[2]
    nx,ny=taille_map,taille_map
    for pos in Artefacts:
        i,j=pos[0],pos[1]
        if ((abs(x-i))**2+(abs(y-j))**2)**0.5<int(dmin):
            dmin=((abs(x-i))**2+(abs(y-j))**2)**0.5
            nx,ny=i,j
    return nx,ny


def recup_artefact(Joueur,x,y):
    artefact=map[y][x]
    print("Le ", Joueur[0], " récupère l'artefact", artefact[1])
    map[y][x]=False
    attribut=artefact[1]
    Joueur[7].append(attribut)
    if attribut=="Puissance divine":
        Joueur[4]+=1
    if attribut=="Coalition divine":
        Joueur[5]+=10000
    if attribut=="Elevation divine":
        Joueur[6]+=1


#recherche de joueurs
def recherche_joueurs(Joueur):
    x,y,lvl=Joueur[1],Joueur[2],Joueur[3]
    Voisins=[]
    Voisins_diff=[]
    for i in range (x-lvl,x+lvl+1):
        for j in range(y-lvl,y+lvl+1):
            if i<0: i=0
            if i>(len(map)-1): i=len(map)-1
            if j<0: j=0
            if j>(len(map)-1): j=len(map)-1
            if map[j][i] !=False:
                voisin_potentiel=map[j][i]
                if voisin_potentiel[0] !="Artefact":
                    coordonnées=[voisin_potentiel[1],voisin_potentiel[2]]
                    Voisins.append(voisin_potentiel)
    for i in Voisins:
        if i not in Voisins_diff and i[0] !=Joueur[0]:
            Voisins_diff.append(i)

    return Voisins_diff

def ennemi_plusproche(Joueur,Voisins):
    dmin=taille_map
    x,y=Joueur[1],Joueur[2]
    nx,ny=taille_map,taille_map
    for pos in Voisins:
        i,j=pos[1],pos[2]
        if ((abs(x-i))**2+(abs(y-j))**2)**0.5<int(dmin):
            dmin=((abs(x-i))**2+(abs(y-j))**2)**0.5
            nx,ny=i,j
    return nx,ny

#combat
def attaque(joueur1,joueur2):
    attaquant=joueur1[0]
    defenseur=joueur2[0]
    print(attaquant," attaque ",defenseur)
    armee1=joueur1[5]
    armee2=joueur2[5]
    p1=rd.randint(50,100)
    p2=rd.randint(50,100)
    armee1=int((p1/100)*armee1)
    armee2=int((p2/100)*armee2)
    puissance1=armee1*joueur1[6]*joueur1[4]
    puissance2=armee2*joueur2[6]*joueur2[4]
    if puissance2<puissance1:
        print("L'attaquant gagne le combat!")
        joueur1[9]+=1
        joueur2[10]+=1
        joueur1[5]-=int(0.1*armee1)
        joueur2[5]-=int(0.4*max(armee1,armee2))
    else:
        print("Le defenseur a repoussé l'envahisseur!")
        joueur2[9]+=1
        joueur1[10]+=1
        joueur1[5]-=int(0.4*max(armee1,armee2))
        joueur2[5]-=int(0.1*armee2)

    if joueur1[5]<=0:
        kill(joueur1)
        joueur2[8]+=1
    if joueur2[5]<=0:
        kill(joueur2)
        joueur1[8]+=1


def kill(joueur):
    print ("Le ", joueur[0]," est mort, paix à son âme")
    Test=False
    for i in range (len(Liste_Joueurs)):
        if Test==False:
            joueur2=Liste_Joueurs[i]
            if joueur[0]==joueur2[0]:
                joueur2[5]=0
                Liste_Joueurs.pop(i)
                map[joueur[2]][joueur[1]]=False
                Test=True



def attente(joueur):
    print("Le ", joueur[0], " se renforce !")
    lvl=rd.randint(0,1)
    joueur[3]+=lvl
    joueur[5]+=int((rd.randint(10,100)/100)*joueur[5])





##
map=[]
Liste_Joueurs=[]
start()


tour=1

while len(Liste_Joueurs)>1:
    print("Début du tour ",tour)
    print("Il reste ",len(Liste_Joueurs)," joueurs vivants")
    Liste_Joueurs=melanger_joueurs(Liste_Joueurs)
    print("Création des artefacts !")
    crea_artefacts()
    deplacer_joueurs(Liste_Joueurs)
    for i in range(len(Liste_Joueurs)):
        if i<len(Liste_Joueurs):
            joueur=Liste_Joueurs[i]
            print("C'est au ",joueur[0]," de jouer!")
            print("Le ",joueur[0]," recherche des artefacts")
            artefacts_potentiels=recherche_artefacts(joueur)
            if len(artefacts_potentiels)!=0:
                x,y=artefact_plusproche(joueur,artefacts_potentiels)
                recup_artefact(joueur,x,y)
            ennemis_potentiels=recherche_joueurs(joueur)
            if len(ennemis_potentiels)==0:
                attente(joueur)
            else:
                x,y=ennemi_plusproche(joueur,ennemis_potentiels)
                ennemi=map[y][x]
                attaque(joueur,ennemi)
            print("Le ", joueur[0]," a terminé son tour!")
    print("Fin du tour !")
    tour+=1

vainqueur=Liste_Joueurs[0]
print("Le vainqueur est ",vainqueur[0])
print("Il aura fallut ",tour," tours!")
print("Voici ses statistiques:")
print(stats(vainqueur))






























