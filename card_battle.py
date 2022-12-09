import random as rd

class Pile:
    def __init__(self):
        self.pile= list()
    def estVide(self):
        return not self.pile
    def hauteur(self):
        return len(self.pile)
    def sommet(self):
        if not self.estVide(): return self.pile[-1]
        else: print("Pas de sommet, la pile est vide")
    def empiler(self,valeur):
        self.pile.append(valeur)
    def depiler (self):
        if not self.estVide():
            return self.pile.pop()
        else:
            raise IndexError("On ne peux pas dépiler une pile vide")


def valeurcarte(id):
    id=id%13
    carte=0
    if id==0: carte=12
    elif id<9: carte=id+2
    else: carte=id
    return carte

def signecarte(id):
    id=valeurcarte(id)
    if id<9:
        carte=id
    else:
        carte=""
        if id==12:
            carte="As"
        if id==11:
            carte="Roi"
        if id==10:
            carte="Dame"
        else:
            carte="Valet"
    return carte

def couleurcarte(id):
    couleur=""
    a=id%4
    if a==0: couleur="pique"
    elif a==1: couleur="coeur"
    elif a==2: couleur="carreau"
    else: couleur="trèfle"
    return couleur


## question 1
liste=[]
for i in range(0,52):
    liste.append(i)
rd.shuffle(liste)
print(liste)

#question 2
paquet=Pile()
for i in liste:
    paquet.empiler(i)

#Question 3
paquet1=Pile()
paquet2=Pile()
for i in range (paquet.hauteur()):
    a=paquet.depiler()
    if i%2==0:
        paquet1.empiler(a)
    else:
        paquet2.empiler(a)




##Question 5
carte1=paquet1.depiler()
print(carte1)
carte2=paquet2.depiler()
print(carte2)
##
def test(carte1,carte2):
    res=0
    valeur1=valeurcarte(carte1)
    valeur2=valeurcarte(carte2)
    if valeur1>valeur2:
        res=1
    elif valeur1<valeur2:
        res=2
    return res

##question 6
pilejeu1=Pile()
pilejeu2=Pile()

def jouer1carte(pilejeu,paquet):
    a=paquet.depiler()
    pilejeu.empiler(a)

#Question 7
def ramasse(paquet,pilejeu1,pilejeu2):
    pile=Pile()
    pile.pile=list(pilejeu1.pile)
    while not pilejeu2.estVide():
        pile.empiler(pilejeu2.depiler())
    while not paquet.estVide():
        pile.empiler(paquet.depiler())
    paquet.pile=list(pile.pile)
    pilejeu1=Pile()
    pilejeu2=Pile()
    return paquet



##Question 8
def finTour(paquet1,paquet2):
    res=0
    if paquet1.estVide():
        res=1
    elif paquet2.estVide():
        res=2
    return res



## Jeu
#distribution des cartes
liste=[]
for i in range(0,52):
    liste.append(i)
rd.shuffle(liste)
print(liste)

paquet=Pile()
for i in liste:
    paquet.empiler(i)

paquet1=Pile()   #création paquet joueur 1
paquet2=Pile()   #création paquet joueur 1
for i in range (paquet.hauteur()):
    a=paquet.depiler()
    if i%2==0:
        paquet1.empiler(a)    #remplissage paquet joueur 1
    else:
        paquet2.empiler(a)    #remplissage paquet joueur 1

pilejeu1=Pile() #création Pile de jeu joueur 1
pilejeu2=Pile() #création pile de jeu joueur 2


while finTour(paquet1,paquet2)==0:
    jouer1carte(pilejeu1,paquet1)
    jouer1carte(pilejeu2,paquet2)
    carte1=pilejeu1.depiler()
    print("Joueur 1 joue ",signecarte(carte1)," de ", couleurcarte(carte1))
    carte2=pilejeu2.depiler()
    print("Joueur 2 joue ",signecarte(carte2)," de ", couleurcarte(carte2))

    gagnant=test(carte1,carte2)
    if gagnant==1:
        paquet1=ramasse(paquet1,pilejeu1,pilejeu2)
        print("Joueur 1 gagne la manche")
    elif gagnant==2:
        paquet2=ramasse(paquet2,pilejeu1,pilejeu2)
        print("Joueur 2 gagne la manche")
    else:
        while gagnant==0:
            print("Bataille !")
            pilejeu1.empiler(carte1)
            pilejeu2.empiler(carte2)
            jouer1carte(pilejeu1,paquet1)
            print("Joueur 1 joue une carte face cachée")
            jouer1carte(pilejeu2,paquet2)
            print("Joueue 2 joue une carte face cachée")
            jouer1carte(pilejeu1,paquet1)
            jouer1carte(pilejeu2,paquet2)
            carte1=pilejeu1.depiler()
            print("Joueur 1 joue ",signecarte(carte1)," de ", couleurcarte(carte1))
            carte2=pilejeu2.depiler()
            print("Joueur 2 joue ",signecarte(carte2)," de ", couleurcarte(carte2))
            gagnant=test(carte1,carte2)

        if gagnant==1:
            paquet1=ramasse(paquet1,pilejeu1,pilejeu2)
            print("Joueur 1 gagne la manche")
        else:
            paquet2=ramasse(paquet2,pilejeu1,pilejeu2)
            print("Joueur 2 gagne la manche")

if finTour(paquet1,paquet2)==1:
    print("Le joueur 2 gagne la partie")
else:
    print("Le joueur 1 gagne la partie")












