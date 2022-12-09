import pylab        # module intégrant Mathplotlib et Numpy
pylab.ion()         # mode interactif : ON

Couleurs = ([(230/256, 140/256, 100/256),(170/256, 230/256, 100/256),(100/256, 160/256, 230/256),
             (230/256, 230/256, 100/256),(230/256, 100/256, 120/256),(100/256, 100/256, 230/256),
             (200/256, 100/256, 230/256),(100/256, 240/256, 190/256),(240/256, 160/256, 100/256),
             (90/256, 150/256, 240/256)])

def nonVide(pile): return len(pile)!=0
def empiler(pile,x): pile.append(x)
def depiler(pile):
    if nonVide(pile): return pile.pop()
def sommet(pile):
    if nonVide(pile): return pile[-1][0]
    else : return 0
def affiche(L):
    return [sommet(tour) for tour in L]


def deplace_disque(L,n,p,q,r):
    """ Procédure déplaçant n disques de la tour p à la tour r à l'aide de la tour intermédiaire q
        L est une liste de 3 listes (les 3 tours) représentants les disques sur chacune des tours """
    #a compléter

def deplace_disque_iteratif(L,n,p,q,r):
    def petit_disque(L):
        """determiner l'indice du plus petit disque"""
        #a compléter
    def deplacer_petit_disque(L,i):
        """deplace le plus petit disque"""
        #a compléter

    def plus_petit(L,j,k):
        """ renvoie un tuple
        si les piles sont vides on renvoie le tuple (len(L),len(L))
        sinon les piles sont non vides le plus petit des deux en premier
        sinon renvoie la pile nonVide en premier"""
        #a compléter

    def deplacer_autre_disque(L,i):
        """deplace si possible le disque plus grand que le premier"""
        #a compléter

    #a compléter

def jeux_manuel(L):
    """  """
    T1=0
    while T1!=3 :
        T1=4
        while T1 not in (0,1,2,3) :
            T1=int(input("choisir la tour où enlever un disque (0, 1, 2 ou 3 pour arrêter) : "))
        if (T1!=3) and (L[T1]!=[]) :
            T2=3
            while T2 not in (0,1,2) :
                T2=int(input("choisir la tour de destination : "))
            x = L[T1].pop()
            L[T2].append(x)
            affiche_image(L)
            pylab.waitforbuttonpress(timeout=-1)
            pylab.draw_if_interactive()
            pylab.pause(0.2)

def affiche_fond_d_image(n):
    # affiche les trois tours vides pour un jeu de n disques
    pylab.clf()
    largeur = 3*2*n+4
    hauteur = n+6
    axes_Tours = ([-(2*n+1),0,(2*n+1)]) # abscisses des axes des trois tours
    pylab.axis([int(-largeur/2),int(largeur/2),-2,hauteur-2])
    F = pylab.gca()                     # F peut être vu comme un objet ’figure’
    color_R,color_G,color_B = 130/256, 120/256, 80/256
    for i in range (3) :
        Tour = pylab.Rectangle((axes_Tours[i]-0.5,0),1,n+1,color=(color_R,color_G,color_B))
        F.add_patch(Tour)
        Base = pylab.Rectangle((axes_Tours[i]-n,-1),2*n,1,color=(color_R,color_G,color_B))
        F.add_patch(Base)
    pylab.draw()


def affiche_image(L):
    # affiche l'état du jeu représenté par le tableau L
    # L[i] contient les descriptions des disques de la tour i,
    # Un disque est représenté par son numéro et sa couleur
    n = len(L[0]) + len(L[1]) + len(L[2])
    affiche_fond_d_image(n)
    axes_Tours = ([-(2*n+1),0,(2*n+1)]) # abscisses des axes des trois tours
    F = pylab.gca()
    num_tour = 0
    for Tour in L:
        compteur_de_disque = 0
        for disque in Tour:
            rect = pylab.Rectangle((axes_Tours[num_tour]-disque[0],compteur_de_disque),2*disque[0],1,color=disque[1])
            F.add_patch(rect)
            compteur_de_disque += 1
        num_tour += 1
    pylab.draw_if_interactive()
    pylab.pause(0.1)


def affiche_jeu_initial(n):
    affiche_fond_d_image(n)
    # création des disques de la première tour
    Tour_0=[]
    for i in range(n):
        disque = [n-i,Couleurs[i%10]]
        Tour_0.append(disque)
    L = [Tour_0, [], []]
    affiche_image(L)
    pylab.pause(2)
    return L

def Tour_de_Hanoi():
    n=int(input("donner le nombre de disques de la tour 0 : "))
    L=affiche_jeu_initial(n)
    jeux_manuel(L)
#   deplace_disque(L,n,0,1,2)
#   deplace_disque_iteratif(L,n,0,1,2)

Tour_de_Hanoi()