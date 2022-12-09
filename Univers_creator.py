#import des modules
import pygame
import math
from math import sqrt
import tkinter as tk
import random as rd


#paramètres de la fenêtre (longueur x hauteur)
WIDTH, HEIGHT = 1920, 1000




#classe Astre qui régit la physique et le déplacement des astres du système
class Astre:

    G = 6.67428e-11 #constante gravitationnelle

    def __init__(self, x, y, rayon, couleur, masse,TIMESTEP,SCALE):
        #définition des attributs
        self.x = x #position x
        self.y = y #position y
        self.rayon = rayon #rayon de l'astre
        self.couleur = couleur
        self.masse = masse
        self.TIMESTEP=TIMESTEP #pas de temps pour le calcul des déplacements
        self.SCALE= SCALE #échelle pour la fenêtre de simulation
        self.orbit_couleur=(112,114,110) #couleur des orbites (gris clair)


        self.orbit = []  #liste des orbites
        self.centre_syst = False #objet défini comme le centre du système (par défaut non)
        self.distance_centre_syst = 0 #distance par rapport au centre du système

        self.x_vel = 0 #vélocité radiale de l'astre
        self.y_vel = 0 #vélocité tangentielle

    def draw(self, win): #méthode qui définit les coordonnées et dessine l'astre et son orbite sur la fenêtre de simulation
        x = self.x * self.SCALE + WIDTH / 2 #coordonnée x
        y = self.y * self.SCALE + HEIGHT / 2 #coordonnée y

        if len(self.orbit) > 2: #si on a déjà des coordonnées pour l'orbite
            updated_points = [] #on va créer une nouvelles listes pour les nouveaux points
            for point in self.orbit: #on parcourt les points d'orbites
                x, y = point
                x = x * self.SCALE + WIDTH / 2
                y = y * self.SCALE + HEIGHT / 2
                updated_points.append((x, y)) #on ajoute les nouveaux points

            pygame.draw.lines(win, self.orbit_couleur, False, updated_points, 1) #on trace l'orbite

        pygame.draw.circle(win, self.couleur, (x, y), self.rayon) #trace l'astre



    def attraction(self, other): #définit la force par attraction gravitationnelle entre deux astres
        #on calcule la distance entre les deux astres (norme du vecteur entre les deux astres)
        other_x, other_y = other.x, other.y
        distance_x = other_x - self.x
        distance_y = other_y - self.y
        distance = math.sqrt(distance_x ** 2 + distance_y ** 2)

        if other.centre_syst: #si le second objet est le centre du syst on a directement la distance par rapport au centre du syst
            self.distance_centre_syst = distance

        force = self.G * self.masse * other.masse / distance**2 #interaction gravitationnelle
        theta = math.atan2(distance_y, distance_x) #on calcule l'angle pour récupérer force tangentielle et radiale
        force_x = math.cos(theta) * force #force radiale
        force_y = math.sin(theta) * force #force tangentielle
        return force_x, force_y

    def update_position(self, Astres): #mise à jour de la position des astres
        total_fx = total_fy = 0 #crée des valeurs pour la sommes des forces
        for astre in Astres: #permet de prendre chaque astre et ajouter la somme des forces
            if self == astre:
                continue

            fx, fy = self.attraction(astre) #appel de la fonction attraction pour sommer les forces
            total_fx += fx
            total_fy += fy

        self.x_vel += total_fx / self.masse * self.TIMESTEP #nouveau vecteur vitesse radiale
        self.y_vel += total_fy / self.masse * self.TIMESTEP #nouveau vecteur vitesse tangentielle

        self.x += self.x_vel * self.TIMESTEP #nouvelle position en x
        self.y += self.y_vel * self.TIMESTEP #nouvelle position en y
        self.orbit.append((self.x, self.y)) #on ajoute le point de passage à l'orbite




#Classe Planet: optimisation de la classe Astre spécialement pour le système solaire (démo)+ affichage des distances des orbites
#tous les commentaires de la classe Astre sont valables pour la classe Planete
class Planete:
    AU = 149.6e9 #unité astronomique en m
    G = 6.67428e-11 #constante gravitationnelle
    SCALE = 250 / AU  # 1 unité de distance = 250 pixels
    TIMESTEP = 3600*24 # 1 jour d'intervalle entre chaque prise de position

    def __init__(self, x, y, rayon, couleur, masse):
        self.x = x
        self.y = y
        self.rayon = rayon
        self.couleur = couleur
        self.masse = masse

        self.orbit = []
        self.centre = False
        self.distance_to_sun = 0 #distance au soleil

        self.x_vel = 0
        self.y_vel = 0

    def draw(self, win):
        x = self.x * self.SCALE + WIDTH / 2
        y = self.y * self.SCALE + HEIGHT / 2

        if len(self.orbit) > 2:
            updated_points = []
            for point in self.orbit:
                x, y = point
                x = x * self.SCALE + WIDTH / 2
                y = y * self.SCALE + HEIGHT / 2
                updated_points.append((x, y))

            pygame.draw.lines(win, self.couleur, False, updated_points, 2)

        pygame.draw.circle(win, self.couleur, (x, y), self.rayon)

        if not self.centre: #on ajoute les distance des astres (en km)
            distance_text = pygame.font.SysFont("comicsans", 16).render(f"{round(self.distance_to_sun/1000, 1)}km", 1, (255,255,255))
            win.blit(distance_text, (x - distance_text.get_width()/2, y - distance_text.get_height()/2))

    def attraction(self, other):
        other_x, other_y = other.x, other.y
        distance_x = other_x - self.x
        distance_y = other_y - self.y
        distance = math.sqrt(distance_x ** 2 + distance_y ** 2)

        if other.centre:
            self.distance_to_sun = distance

        force = self.G * self.masse * other.masse / distance**2
        theta = math.atan2(distance_y, distance_x)
        force_x = math.cos(theta) * force
        force_y = math.sin(theta) * force
        return force_x, force_y

    def update_position(self, planets):
        total_fx = total_fy = 0
        for planet in planets:
            if self == planet:
                continue

            fx, fy = self.attraction(planet)
            total_fx += fx
            total_fy += fy

        self.x_vel += total_fx / self.masse * self.TIMESTEP
        self.y_vel += total_fy / self.masse * self.TIMESTEP

        self.x += self.x_vel * self.TIMESTEP
        self.y += self.y_vel * self.TIMESTEP
        self.orbit.append((self.x, self.y))




#Menu permettant de choisir le système à créer
def choix_type():
    conf=tk.Tk() #création de la fenêtre à partir e la classe Tkinter
    conf.geometry('300x140') #taille de la fenêtre
    conf.title("Création de l'univers") #nom de la fenêtre
    #modes de configuration et boutons pour faire le choix
    MODES = [ ( "Système solaire (démo)" , 0),("Système planétaite",2),( "Galaxie" , 1)]
    v = tk.IntVar ()
    v.set ( 0 ) # on initialise par défaut la valeur à démo
    for texte, mode in MODES:
        b = tk.Radiobutton (conf, text = texte, variable = v, value = mode)
        b.pack ()
    bouton=tk.Button(conf,text='valider', command=conf.destroy) #bouton valider qui ferme la fenêtre
    bouton.pack()
    conf.mainloop() #mainloop pour la fenêtre (imposée pour faire fonctionner une fenêtre Tkinter)
    return v.get() #on récupère le mode de système (démo/système planétaire/galaxie)




#Création de la galaxie

def Galaxie():
    conf=tk.Tk()
    conf.geometry('300x220')
    conf.title("Création de la Galaxie")
    #choix du type de galaxie
    message = tk.Label(text="Renseignez le type de Galaxie ")
    message.pack()
    TYPES_Galaxie = [ ( "Spirale" , 0),("Irrégulière",1)]
    type_galaxie = tk.IntVar ()
    type_galaxie.set ( 0 ) # initialise en galaxie spirale par défaut
    for texte, mode in TYPES_Galaxie:
        b = tk.Radiobutton (conf, text = texte, variable = type_galaxie, value = mode)
        b.pack ()

    #choix d'un trou noir central ou non
    message = tk.Label(text="Choisissez si vous voulez un trou noir central ")
    message.pack()
    MODES = [ ( "Oui" , 0),( "Non" , 1)]
    type_trou_noir = tk.IntVar ()
    type_trou_noir.set ( 0 ) # initialise avec trou noir par défaut
    for texte, mode in MODES:
        c = tk.Radiobutton (conf, text = texte, variable = type_trou_noir, value = mode)
        c.pack ()

    bouton=tk.Button(conf,text='valider', command=conf.destroy)
    bouton.pack()
    conf.mainloop()
    return type_galaxie.get(),type_trou_noir.get() # on récupère le type de galaxie (spirale/irrégulière) et si il y  un trou noir




#Configuration de la galaxie

def config_galaxie(type_trou_noir):
    masse_sol=2*10**35 #1 masse solaire en kg
    if type_trou_noir==0: #si on a choisit un trou noir central on ouvre une fenêtre pour renseigner sa masse
        conf=tk.Tk()
        conf.geometry('300x110')
        conf.title("Création de la Galaxie")

        #si on a un trou noir on choisit ses caractéristiques
        message = tk.Label(text="Renseignez la masse moyenne du trou noir \n (en masse solaire)")
        message.pack()
        m_trou_noir=tk.DoubleVar()
        m_trou_noir.set(100) #par défaut on a 100 masses solaires
        Nombre=tk.Entry(conf,textvariable=m_trou_noir)
        Nombre.pack()
        bouton=tk.Button(conf,text='valider', command=conf.destroy)
        bouton.pack()
        conf.mainloop()
        masse_trou_noir=100*m_trou_noir.get()*masse_sol #on crée la masse du trou noir avec un facteur correctif (pour que le rendu soit correct)


    conf=tk.Tk()
    conf.geometry('300x200')
    conf.title("Création des étoiles")

    #choix du nombre d'étoiles
    message = tk.Label(text="Renseignez le nombre d'étoiles")
    message.pack()
    nb_étoiles=tk.IntVar()
    nb_étoiles.set(50)
    Nombre=tk.Entry(conf,textvariable=nb_étoiles)
    Nombre.pack()
    #choix de la masse moyenne des étoiles
    message = tk.Label(text="Renseignez la masse moyenne des étoiles \n (en masse solaire)")
    message.pack()
    mm_étoiles=tk.DoubleVar()
    mm_étoiles.set(1)
    Nombre=tk.Entry(conf,textvariable=mm_étoiles)
    Nombre.pack()

    bouton=tk.Button(conf,text='valider', command=conf.destroy)
    bouton.pack()
    conf.mainloop()

    Rayons=[14,12,10,10,6] #liste des rayons possibles des étoiles
    Liste_Rayons=[] #liste des rayons des étoiles de notre système
    Liste_Couleurs=[] #liste des couleurs des étoiles de notre système
    Liste_Masses=[] #liste des masse des étoiles de notre système
    for i in range(nb_étoiles.get()):
        Liste_Rayons.append(Rayons[rd.randint(0, len(Rayons))-1]) #pour chaque étoile on lui attribut aléatoirement un rayon
        Liste_Couleurs.append((255, 255, 255)) #toutes les étoiles sont blanches
        Liste_Masses.append(rd.uniform(1,3)*mm_étoiles.get()*masse_sol) #on crée la masse de chaque étoile par rapport à la masse moyenne

    if type_trou_noir==0: #si il y a un trou noir, on renvoit sa masse, le nb d'étoiles, la liste des rayons, des couleurs et des masses
        return nb_étoiles.get(),masse_trou_noir,Liste_Rayons,Liste_Couleurs,Liste_Masses
    else: #sinon on renvoit pareil mais sans la masse du trou noir (car il n'existe pas)
        return nb_étoiles.get(),Liste_Rayons,Liste_Couleurs,Liste_Masses




#Création du système planétaire

def Systeme_planetaire():
    conf=tk.Tk()
    conf.geometry('300x220')
    conf.title("Création du système planétaires")
    #choix du type de système
    message = tk.Label(text="Renseignez le type de système ")
    message.pack()
    TYPES_Syst = [ ( "Ordonné" , 0),( "Chaotique" , 1)]
    type_syst = tk.IntVar ()
    type_syst.set ( 0 ) # initialise par défaut en système ordonné
    for texte, mode in TYPES_Syst:
        b = tk.Radiobutton (conf, text = texte, variable = type_syst, value = mode)
        b.pack ()
    #choix du nombre de planètes
    message = tk.Label(text="Renseignez le nombre de planètes")
    message.pack()
    nb_planètes=tk.IntVar()
    nb_planètes.set(5)
    Nombre=tk.Entry(conf,textvariable=nb_planètes)
    Nombre.pack()
    bouton=tk.Button(conf,text='valider', command=conf.destroy)
    bouton.pack()
    conf.mainloop()
    return type_syst.get(),nb_planètes.get() #renvoie le type de syst et le nb de planètes




#Choix configuration du système planétaire (choix entre configuration automatique ou personnalisée)

def choix_config_planetes(nb_planètes):
    conf=tk.Tk()
    conf.geometry('360x140')
    conf.title("Choix de création")
    message = tk.Label(text="Choisis le type de personnalisation pour tes planètes:")
    message.pack()
    MODES = [ ( "Personnalisée" , 0),( "Automatique" , 1)]
    v = tk.IntVar ()
    v.set ( 1 ) # initialize
    for texte, mode in MODES:
        b = tk.Radiobutton (conf, text = texte, variable = v, value = mode)
        b.pack ()
    bouton=tk.Button(conf,text='valider', command=conf.destroy)
    bouton.pack()
    conf.mainloop()


    if v.get()==0: #si on choisit personnalisée on fait appelle à la fonction de config perso
        Liste_Rayons,Liste_Couleurs,Liste_Masses=conf_planetes_perso(nb_planètes)
    else: #sinon on fait appelle à la fonction de config automatique
        Liste_Rayons,Liste_Couleurs,Liste_Masses=conf_planetes_auto(nb_planètes)

    return Liste_Rayons,Liste_Couleurs,Liste_Masses #on récupère les listes de rayons, couleurs, et masses


#Configuration automatique

def conf_planetes_auto(nb_planètes):
    masse_moyenne=6*10**24 #masse terrestre en kg
    Rayons=[30,22,16,12,8] #liste des rayoons possibles
    Couleurs=[(255, 255, 255),(80, 78, 81),(100, 149, 237),(188, 39, 50)] #liste des couleurs possibles
    Liste_Rayons=[] #liste des rayons du syst
    Liste_Couleurs=[] #liste des couleurs
    Liste_Masses=[] #liste des masses
    for i in range(nb_planètes): #pour chaque planète on attribut aléatoirement un rayon, une couleur et une masse
        Liste_Rayons.append(Rayons[rd.randint(0, len(Rayons))-1])
        Liste_Couleurs.append(Couleurs[rd.randint(0,len(Couleurs)-1)])
        Liste_Masses.append(rd.uniform(0.01,100)*masse_moyenne)
    return Liste_Rayons,Liste_Couleurs,Liste_Masses #on récupère les listes de rayons, couleurs, et masses




#Configuration personnalisée

def conf_planetes_perso(nb_planètes):
    Liste_Rayons=[]
    Liste_Couleurs=[]
    Liste_Masses=[]
    masse_terre=6*10**24
    for  i in range(nb_planètes): #choix ddu rayon, couleur, masse pour chaque planète

        conf=tk.Tk()
        conf.geometry('400x450')
        titre="Création de la planète n° " +str(i+1)
        conf.title(titre)

        #config taille du rayon de la planète
        message = tk.Label(text="Renseignez le rayon de la planète")
        message.pack()
        RAYONS = [ ("ENORME", 20), ( "GRAND" , 16),( "MOYEN" , 12),( "PETIT", 8), ( "MINUSCULE", 6) ]
        rayon = tk.IntVar ()
        rayon.set ( 16 ) # initialise en rayon moyen
        for texte, mode in RAYONS:
            b = tk.Radiobutton (conf, text = texte, variable = rayon, value = mode)
            b.pack ()

        #config couleur de la planète
        message = tk.Label(text="Renseignez la couleur de la planète")
        message.pack()
        COULEURS = [ ( "BLANC" , 0),( "GRIS Foncé" , 1),( "BLEU", 2), ( "ROUGE", 3) ]
        couleur = tk.IntVar ()
        couleur.set ( 2 ) # initialise en planète bleue
        for texte, mode in COULEURS:
            b = tk.Radiobutton (conf, text = texte, variable = couleur, value = mode)
            b.pack ()

        #config masse de la planète
        message = tk.Label(text="Renseignez la masse moyenne de la planète \n (en nombre de masse terrestre)")
        message.pack()
        masse=tk.DoubleVar()
        masse.set(1)
        Nombre=tk.Entry(conf,textvariable=masse)
        Nombre.pack()

        #paramètrage fermeture fenêtre
        bouton=tk.Button(conf,text='valider', command=conf.destroy)
        bouton.pack()
        conf.mainloop()

        Liste_Rayons.append(rayon.get())#on ajoute le rayon à la liste des rayons
        #en fonction de la couleur on aura un code rgb
        if couleur.get()==0:
            rgb=(255, 255, 255) #blanc
        elif couleur.get()==1:
            rgb=(80, 78, 81) #gris foncé
        elif couleur.get()==2:
            rgb=(100, 149, 237) #bleu
        elif couleur.get()==3:
            rgb=(188, 39, 50) #rouge

        Liste_Couleurs.append(rgb) #on ajoute la couleur rgb
        Liste_Masses.append(masse.get()*masse_terre) #on ajoute la masse



    return Liste_Rayons,Liste_Couleurs,Liste_Masses #on renvoie la lsite des rayons,couleurs,masses




#Définition du vecteur velocité tangentielle

def vel(vel_moyenne,nb_objets_syst):
    Vel_y=[]
    for i in range(nb_objets_syst):
        Vel_y.append(rd.uniform(0.1,4)*vel_moyenne) #répartition autour des vitesses autour d'une vitesse moyenne

    return Vel_y #on récupère une liste de vitesses




#Définition des  positions cartésiennes des astres

def position(etat_syst,unité_distance,nb_objets_syst):
    Pos_x=[0]
    Pos_y=[0]
    if etat_syst==0: #système d'état ordonné: repartition des astres selon des ellipses concentriques
        for i in range(nb_objets_syst):
            Pos_x.append(((-1)**rd.randint(0,1))*(Pos_x[i]+rd.uniform(0.62,1.67)*unité_distance))
            Pos_y.append(((-1)**rd.randint(0,1))*(Pos_y[i]+rd.uniform(0.62,1.67)*unité_distance))

    else: #état chaotique/irrégulier: on place aléatoirement les astres
        for i in range(nb_objets_syst):
            Pos_x.append(rd.uniform(-10,10)*unité_distance) #placement aléatoire en x
            Pos_y.append(rd.uniform(-10,10)*unité_distance) #placement aléatoire en y

    Pos_x.pop(0) #on retire le premier élément x=0 qui a servit pour calculé les ellipses concentriques
    Pos_y.pop(0) #idem
    return Pos_x,Pos_y #on récupère les listes de positions x et y




#Définition de la distance par rapport au centre (norme du vecteur)

def distance_centre(x,y):
    return sqrt(x**2+y**2)




#Création de la liste des astres à partir des classes

def creation_des_astres():
    type_syst=choix_type() #on fait appelle à la fonction pour faire le choix du système

    Astres=[] #liste vide pour les astres
    if type_syst==0: #on fait alors la démo avec le système solaire réel
        unité_distance=149.6*10**9 # = 1 unité astonomique en m
        BACK=(0,0,0) #couleur du fond de la simulation en noir


        #config réelle du soleil
        soleil = Planete(0, 0, 30, (255,255,0), 1.98892 * 10**30)
        soleil.centre = True #le soleil est bien le centre du système


        #config réelle de mercure
        mercure = Planete(0.387 * unité_distance, 0, 8, (80, 78, 81), 3.30 * 10**23)
        mercure.y_vel = -47.4 * 1000 #vitesse de mercure en m/s


        #config réelle de vénus
        venus = Planete(0.723 * unité_distance, 0, 14, (255,255,255), 4.8685 * 10**24)
        venus.y_vel = -35.02 * 1000


        #config réelle de la terre
        terre = Planete(-1 *unité_distance, 0, 16, (100, 149, 237), 5.9742 * 10**24)
        terre.y_vel = 29.783 * 1000


        #config réelle de mars
        mars = Planete(-1.524 * unité_distance, 0, 12, (188, 39, 50), 6.39 * 10**23)
        mars.y_vel = 24.077 * 1000


        Astres=[soleil,mercure,venus,terre,mars] #on met toutes les planètes dans la liste des astres




    else: #sinon on doit soit créer une galaxie soit un système planétaire

        if type_syst==2: #système planétaire
            etat_syst,nb_objets_syst=Systeme_planetaire() #on récupère l'état et le nb d'objets dedans
            Liste_Rayons,Liste_Couleurs,Liste_Masses=choix_config_planetes(nb_objets_syst) #on le configure

            TIMESTEP = 3*3600*24 # 3 jour/maj de simulation
            unité_distance=2*149.6*10**9 # = 2 unité astonomique en m
            SCALE=500/(10*149.6*10**9) # 500 pixels=10 unités astronomiques en m
            vel_moyenne=2.8*10**3 #vel moyenne d'une planète en m/s
            BACK=(0,0,0) #couleur du fond de la simulation en noir


        elif type_syst==1: #galaxie
            etat_syst,type_trou_noir=Galaxie() #on récupère l'état et si il y a un trou noir
            if type_trou_noir==0: #si il y en a un
                nb_objets_syst,masse_trou_noir,Liste_Rayons,Liste_Couleurs,Liste_Masses=config_galaxie(type_trou_noir)
            else: #sinon
                nb_objets_syst,Liste_Rayons,Liste_Couleurs,Liste_Masses=config_galaxie(type_trou_noir)

            TIMESTEP = 800*365*3600*24 # 800 années/maj de simulation
            unité_distance=20*9.461*10**15 # = 20 années lumières en m
            SCALE=50/unité_distance # 50 pixels = 20 années lumières en m
            vel_moyenne=240*10**3 #vel moyenne d'une étoile en m/s
            BACK=(46,58,81) #couleur du fond de la simulation en bleu foncé pour faire ressortir le potentiel trou noir


        Vel_y=vel(vel_moyenne,nb_objets_syst) #on déf les vecteurs vitesses des astres du syst
        Pos_x,Pos_y=position(etat_syst,unité_distance,nb_objets_syst) #de même pour leurs positions


        for i in range(nb_objets_syst): #on crée les astres avec la classe Astre
            Astres.append(Astre(Pos_x[i],Pos_y[i],Liste_Rayons[i],Liste_Couleurs[i],Liste_Masses[i],TIMESTEP,SCALE))
            if etat_syst==0: #si l'état est ordonné on fournit une vitesse
                #pour le sens de rotation
                if Pos_x[i]<0:
                    Astres[i].y_vel=Vel_y[i]*(1/distance_centre(Pos_x[i],Pos_y[i])*distance_centre(Pos_x[0],Pos_y[0])*1.5)
                else:
                    Astres[i].y_vel=-1*Vel_y[i]*(1/distance_centre(Pos_x[i],Pos_y[i])*distance_centre(Pos_x[0],Pos_y[0])*1.5)





        if type_syst==2: #si c'est un ystème planétaire on place l'étoile centrale (un soleil)
            Astres.append(Astre(0, 0, 30, (255, 255, 0), 1.98892 * 10**30,TIMESTEP,SCALE))
            Astres[0].centre_syst=True #le centre du syst

        elif type_syst==1 and type_trou_noir==0: #si c'est une galaxie avec un trou noir on place le trou noir
            Astres.append(Astre(0, 0, 30, (0,0,0), masse_trou_noir,TIMESTEP,SCALE))
            Astres[0].centre_syst=True# idem le trou noir est le centre du syst

    return Astres,BACK #on récupère la liste des astres et la couleur du fond pour la simulation




#Message d'introduction au lancement

def message_depart():
    conf=tk.Tk()
    conf.geometry('600x300')
    conf.title("Bienvenue !")
    message = tk.Label(text="Bienvenue dans Universe Simutalion! \n Une création de 62 (Léa ABITBOL) et 67 (Alexandre CIRERA) \n")
    message.pack()
    message = tk.Label(text="Avez-vous déjà souhaité être comme un dieu et pouvoir créer un univers? \n Et bien vous êtes au bon endroit! \n")
    message.pack()
    message = tk.Label(text="Auriez-vous besoin d'explications?")
    message.pack()
    CHOIX = [ ( "Oui je bien connaitre le principe" , 0),( "Non" , 1)]
    choix = tk.IntVar ()
    choix.set ( 0 ) # initialize
    for texte, mode in CHOIX:
        b = tk.Radiobutton (conf, text = texte, variable = choix, value = mode)
        b.pack ()


    bouton=tk.Button(conf,text='valider', command=conf.destroy)
    bouton.pack()
    conf.mainloop()
    return choix.get() #on récupère le choix de faire appelle ou non  au tutoriel




#Message du tutoriel

def message_tuto():
    conf=tk.Tk()
    conf.geometry('1000x850')
    conf.title("Tutoriel !")
    message = tk.Label(text="Bienvenue dans le tutoriel !\n \n Le concept est relativement simple : \n Tu as la possibilité de créer des galaxies (ou systèmes planétaires) complètement uniques \n puis lancer la simulation pour voir comment ils évoluent avec le temps!")
    message.pack()

    message = tk.Label(text="Le mode 'Système solaire (démo)' te permet d'observer notre cher Soleil et le balais cosmiques de toutes ces fidèles planètes \n qui lui tournent depuis maintenant plus de 4.6 milliards d'années! N'est ce pas magnifique lorsque tout est ordonné ainsi? \n Tu te rendras vite compte la chance que nous avons et que beaucoup de système que tu t'apprêtes à créer ne finiront \n pas aussi bien alors profite de la vue! \n \n")
    message.pack()

    message = tk.Label(text="Le mode 'Système planétaire' te permet de créer un système composé d'une étoile et d'un ensemble de planètes qui vont graviter autour. \n Tu pourras choisir si tu veux un sysème ordonné (planètes uniformément réparties sur des orbites elliptiques) ou chaotique (c'est beau le chaos !)\n Par la suite tu pourras choisir le type de personnalisation souhaité pour tes planètes: \n -Soit automatique (on fait tout pour toi profite) \n -Soit personnalisable où tu pourras choisir le rayon, la couleur et la masse de chaque planète ! \n (attention à toi si tu choisis de créer un grand système cette étape peut devenir très longue \n donc nous te recommandons une personnalisation automatique) \n \n")
    message.pack()
    message = tk.Label(text="Le mode 'Galaxie' te permet de créer une galaxie (énorme hein !?) \n Tu pourras choisir la forme de ta galaxie: \n une belle spirale comme notre magnifique Voie Lactée ou Irrégulière pour quelque chose de plus exotique! \n De plus, tu peux choisir si tu veux ou non un trou noir super massif en son centre (si tu en prends un tu pourras même choisir la taille du bestiau! \n Enfin tu pourras choisir le nombre d'étoiles que tu veux et leur masse moyenne! \n (pour le nombre d'étoiles nous de conseillons de ne pas dépasser 150 pour apprécier le spectacle! \n Après si tu as volé ton ordinateur à la Nasa avec 6762 étoiles ça doit être sympa \n \n")
    message.pack()
    message = tk.Label(text="Rien qu'avec ces paramètres tu as de quoi créer une infinité de systèmes (sans rire le nombre ne tiendrait pas sur ton écran)\n Chaque système que tu vas créer sera unique alors il faut l'apprécier car tu seras son créateur mais aussi son destructeur (RIP)  \n \n Il ne te reste plus qu'à lancer la simulation et admirer l'harmonie ou le chaos \n")
    message.pack()

    message = tk.Label(text="Pour arrêter la simulation tu n'as qu'à fermer la fenêtre de la simulation !")
    message.pack()

    message = tk.Label(text="P.S.: Si tu es HM billard cosmique, crée une galaxie sans trou noir, avec un grand nombre d'étoiles,une masse moyenne assez élevée \n et le spectacle devrait commencer assez rapidement !")
    message.pack()

    bouton=tk.Button(conf,text="Compris, c'est parti !", command=conf.destroy)
    bouton.pack()
    conf.mainloop()




#Message une fois la simulation fermée

def message_fin_simulation():
    conf=tk.Tk()
    conf.geometry('550x250')
    conf.title("Bravo !")
    message = tk.Label(text="Félicitations tu as mis fin à un univers, \n Veux tu recommencer ?")
    message.pack()

    CHOIX = [ ( "Oui ! (mais je veux bien revoir le tutoriel)" , 0),( "Oui ! (sans tutoriel)" , 1),("Non, être un dieu est fatiguant",2)]
    choix = tk.IntVar ()
    choix.set ( 1 ) # initialize
    for texte, mode in CHOIX:
        b = tk.Radiobutton (conf, text = texte, variable = choix, value = mode)
        b.pack ()

    bouton=tk.Button(conf,text="Valider", command=conf.destroy)
    bouton.pack()
    conf.mainloop()
    return choix.get() #on récupère le choix de si le joueur veut relancer (avec ou sans tuto) ou quitter




#Message fermeture

def message_fin():
    conf=tk.Tk()
    conf.geometry('550x150')
    conf.title("Bravo !")
    message = tk.Label(text="Merci d'avoir joué à Univers Simulation ! \n En espérant que tu as passé un bon moment à te prendre pour un Céleste ! \n \n")
    message.pack()


    bouton=tk.Button(conf,text="Quitter", command=conf.destroy)
    bouton.pack()
    conf.mainloop()




#Gestion de la simulation à partir des astres fromés par les classes

def simulation():

    Astres,BACK=creation_des_astres() #on récupère les astres et le fond

    pygame.init() #on initialise pygame qui va faire la simulation


    WIN = pygame.display.set_mode((WIDTH, HEIGHT)) #on crée la fenêtre
    pygame.display.set_caption("Univers Simulation") #on la nomme
    run = True #flag pour la simulation
    clock = pygame.time.Clock() #horloge pour la mise à jour de la simulation



    while run: #tant que run=True  on continue la simumlation
        clock.tick(60)
        WIN.fill(BACK) #on remplit le fond avec sa couleur

        for event in pygame.event.get(): #on regarde les intéractions
            if event.type == pygame.QUIT: #si on clique sur la fenêtre "ferméé
                run = False #on arrête la simulation en changeant le flag
        for astre in Astres: #pour chaque astre
            astre.update_position(Astres) #on met à jour la position des tous les objets
            astre.draw(WIN) #on les trace

        pygame.display.update() #on met à jour la fenêtre

    pygame.quit() #on ferme pygame




#Fonction main qui gère l'ensemble du jeu du lancement à la fermeture

intro=False #dès qu'on lance le jeu par défaut on a pas vu le message d'introduction
choix_tuto=0 #par défaut on à pas vu le tutoriel


def main():
    global intro #on récupère les variables globales
    global choix_tuto #idem

    if intro==False: #si on a pas vu l'intro
        choix_tuto=message_depart() #on montre l'intro
        intro=True #une fois qu'on la vue on la retire jusqu'au prochain démarrage complet
    if choix_tuto==0: #si on veut voir le tuto
        message_tuto() #on montre le tuto
        choix_tuto=1 #puis on retire le tuto suaf si quelqu'un veut le revoir
    simulation() #on fait la simulation
    choix_suite=message_fin_simulation() #on montre le message de fin de simulation et propose de continuer ou quitter
    if choix_suite==0: #si on veut continuer mais revoir le tuto
        choix_tuto=0 #on réactive le tuto
        main() #on relance
    elif choix_suite==1: #si on veut pas revoir le tuto
        main() #on relance juste
    else: #sinon on veut quitter
        message_fin() #on montre le message de fin

main() #on lance main pour lancer le programme
















