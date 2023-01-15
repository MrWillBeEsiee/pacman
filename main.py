import random
import tkinter as tk
from tkinter import font as tkfont
import numpy as np
from enum import Enum, auto

class Direction(Enum):
    HAUT = auto()
    BAS = auto()
    DROITE = auto()
    GAUCHE = auto()


##########################################################################
#
#   Partie I : variables du jeu  -  placez votre code dans cette section
#
#########################################################################

# Plan du labyrinthe

# 0 vide
# 1 mur
# 2 maison des fantomes (ils peuvent circuler mais pas pacman)

# transforme une liste de liste Python en TBL numpy équivalent à un tableau 2D en C
def CreateArray(L):
    T = np.array(L, dtype=np.int32)
    T = T.transpose()  ## ainsi, on peut écrire TBL[x][y]
    return T


TBL = CreateArray([
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1],
    [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
    [1, 0, 1, 0, 1, 1, 0, 1, 1, 2, 2, 1, 1, 0, 1, 1, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 1, 2, 2, 2, 2, 1, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 0, 1],
    [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
    [1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]);
# attention, on utilise TBL[x][y]

HAUTEUR = TBL.shape[1]
LARGEUR = TBL.shape[0]

score = 0
LOOSE = 0

# placements des pacgums et des fantomes

def PlacementsGUM():  # placements des pacgums
    GUM = np.zeros(TBL.shape, dtype=np.int32)

    for x in range(LARGEUR):
        for y in range(HAUTEUR):
            if (TBL[x][y] == 0 ):
                GUM[x][y] = 1
    GUM[1][1] = 3
    GUM[18][1] = 3
    GUM[1][9] = 3
    GUM[18][9] = 3
    return GUM
GUM = PlacementsGUM()




def DistanceCarteInit():
    CarteDistanceGum = TBL.copy()
    for x in range(LARGEUR):
        for y in range(HAUTEUR):
            if GUM[x][y] == 0 or GUM[x][y] == 3:
                CarteDistanceGum[x][y] = -1
            if TBL[x][y] != 0:
                CarteDistanceGum[x][y] = 99
            if GUM[x][y] == 1 or GUM[x][y] == 3:
                CarteDistanceGum[x][y] = 1
    return CarteDistanceGum

CarteDistanceGum = DistanceCarteInit()

PacManPos = [5, 5]



Ghosts = []
Ghosts.append([9, 4, "pink", Direction.HAUT])
Ghosts.append([9, 4, "orange", Direction.HAUT])
Ghosts.append([9, 4, "cyan", Direction.HAUT])
Ghosts.append([9, 4, "red", Direction.HAUT])

def DistanceCarteFantomesInit():
    CarteDistanceFantomes = TBL.copy()
    for x in range(LARGEUR):
        for y in range(HAUTEUR):
            if TBL[x][y] != 0:
                CarteDistanceFantomes[x][y] = 99
            else:
                CarteDistanceFantomes[x][y] = -1
    for i in Ghosts:
        if i[0] != 9 and  i[1] != 5:
            CarteDistanceFantomes[i[0]][i[1]] = 0
    return CarteDistanceFantomes

CarteDistanceFantomes = DistanceCarteFantomesInit()

loose = 0

##############################################################################
#
#  Debug : ne pas toucher (affichage des valeurs autours dans les cases

LTBL = 100
TBL1 = [["" for i in range(LTBL)] for j in range(LTBL)]
TBL2 = [["" for i in range(LTBL)] for j in range(LTBL)]


# info peut etre une valeur / un string vide / un string...
def SetInfo1(x, y, info):
    info = str(info)
    if x < 0: return
    if y < 0: return
    if x >= LTBL: return
    if y >= LTBL: return
    TBL1[x][y] = info


def SetInfo2(x, y, info):
    info = str(info)
    if x < 0: return
    if y < 0: return
    if x >= LTBL: return
    if y >= LTBL: return
    TBL2[x][y] = info


##############################################################################
#
#   Partie II :  AFFICHAGE -- NE PAS MODIFIER  jusqu'à la prochaine section
#
##############################################################################


ZOOM = 40  # taille d'une case en pixels
EPAISS = 8  # epaisseur des murs bleus en pixels

screeenWidth = (LARGEUR + 1) * ZOOM
screenHeight = (HAUTEUR + 2) * ZOOM

Window = tk.Tk()
Window.geometry(str(screeenWidth) + "x" + str(screenHeight))  # taille de la fenetre
Window.title("ESIEE - PACMAN")

# gestion de la pause

PAUSE_FLAG = False


def keydown(e):
    global PAUSE_FLAG
    if e.char == ' ':
        PAUSE_FLAG = not PAUSE_FLAG


Window.bind("<KeyPress>", keydown)

# création de la frame principale stockant plusieurs pages

F = tk.Frame(Window)
F.pack(side="top", fill="both", expand=True)
F.grid_rowconfigure(0, weight=1)
F.grid_columnconfigure(0, weight=1)

# gestion des différentes pages

ListePages = {}
PageActive = 0


def CreerUnePage(id):
    Frame = tk.Frame(F)
    ListePages[id] = Frame
    Frame.grid(row=0, column=0, sticky="nsew")
    return Frame


def AfficherPage(id):
    global PageActive
    PageActive = id
    ListePages[id].tkraise()


def WindowAnim():
    PlayOneTurn()
    Window.after(333, WindowAnim)


Window.after(100, WindowAnim)

# Ressources

PoliceTexte = tkfont.Font(family='Arial', size=22, weight="bold", slant="italic")

# création de la zone de dessin

Frame1 = CreerUnePage(0)

canvas = tk.Canvas(Frame1, width=screeenWidth, height=screenHeight)
canvas.place(x=0, y=0)
canvas.configure(background='black')


#  FNT AFFICHAGE


def To(coord):
    return coord * ZOOM + ZOOM


# dessine l'ensemble des éléments du jeu par dessus le décor

anim_bouche = 0
animPacman = [5, 10, 15, 10, 5]


def Affiche(PacmanColor, message):
    global anim_bouche

    def CreateCircle(x, y, r, coul):
        canvas.create_oval(x - r, y - r, x + r, y + r, fill=coul, width=0)

    canvas.delete("all")

    # murs

    for x in range(LARGEUR - 1):
        for y in range(HAUTEUR):
            if (TBL[x][y] == 1 and TBL[x + 1][y] == 1):
                xx = To(x)
                xxx = To(x + 1)
                yy = To(y)
                canvas.create_line(xx, yy, xxx, yy, width=EPAISS, fill="blue")

    for x in range(LARGEUR):
        for y in range(HAUTEUR - 1):
            if (TBL[x][y] == 1 and TBL[x][y + 1] == 1):
                xx = To(x)
                yy = To(y)
                yyy = To(y + 1)
                canvas.create_line(xx, yy, xx, yyy, width=EPAISS, fill="blue")

    # pacgum
    for x in range(LARGEUR):
        for y in range(HAUTEUR):
            if (GUM[x][y] == 1):
                xx = To(x)
                yy = To(y)
                e = 5
                canvas.create_oval(xx - e, yy - e, xx + e, yy + e, fill="orange")

    # superpacgum
    for x in range(LARGEUR):
        for y in range(HAUTEUR):
            if (GUM[x][y] == 3):
                xx = To(x)
                yy = To(y)
                e = 9
                canvas.create_oval(xx - e, yy - e, xx + e, yy + e, fill="orange")

    # extra info
    for x in range(LARGEUR):
        for y in range(HAUTEUR):
            xx = To(x)
            yy = To(y) - 11
            txt = TBL1[x][y]
            canvas.create_text(xx, yy, text=txt, fill="white", font=("Purisa", 8))

            # extra info 2
    for x in range(LARGEUR):
        for y in range(HAUTEUR):
            xx = To(x) + 10
            yy = To(y)
            txt = TBL2[x][y]
            canvas.create_text(xx, yy, text=txt, fill="yellow", font=("Purisa", 8))

    # dessine pacman
    xx = To(PacManPos[0])
    yy = To(PacManPos[1])
    e = 20
    anim_bouche = (anim_bouche + 1) % len(animPacman)
    ouv_bouche = animPacman[anim_bouche]
    tour = 360 - 2 * ouv_bouche
    canvas.create_oval(xx - e, yy - e, xx + e, yy + e, fill=PacmanColor)
    canvas.create_polygon(xx, yy, xx + e, yy + ouv_bouche, xx + e, yy - ouv_bouche, fill="black")  # bouche

    # dessine les fantomes
    dec = -3
    for P in Ghosts:
        xx = To(P[0])
        yy = To(P[1])
        e = 16

        coul = P[2]
        # corps du fantome
        CreateCircle(dec + xx, dec + yy - e + 6, e, coul)
        canvas.create_rectangle(dec + xx - e, dec + yy - e, dec + xx + e + 1, dec + yy + e, fill=coul, width=0)

        # oeil gauche
        CreateCircle(dec + xx - 7, dec + yy - 8, 5, "white")
        CreateCircle(dec + xx - 7, dec + yy - 8, 3, "black")

        # oeil droit
        CreateCircle(dec + xx + 7, dec + yy - 8, 5, "white")
        CreateCircle(dec + xx + 7, dec + yy - 8, 3, "black")

        dec += 3

    # texte

    canvas.create_text(screeenWidth // 2, screenHeight - 50, text="PAUSE : PRESS SPACE", fill="yellow",
                       font=PoliceTexte)
    canvas.create_text(screeenWidth // 2, screenHeight - 20, text=message, fill="yellow", font=PoliceTexte)

AfficherPage(0)


#########################################################################
#
#  Partie III :   Gestion de partie   -   placez votre code dans cette section
#
#########################################################################
def PointsATraiterInit():
    #Initilsation de la liste des

    L = []
    for x in range(LARGEUR):
        for y in range(HAUTEUR):
            if GUM[x][y] == 1 or GUM[x][y] == 3:
                L.append((x,y))
    return L

def Carte():
    points = PointsATraiterInit()
    CarteDistanceGum = DistanceCarteInit()
    for i in points:
        CarteDistanceGum[i[0]][i[1]] = 0
    L = []
    for k in range(20):
        for i in points:
            x = i[0]
            y = i[1]
            if CarteDistanceGum[x+1][y] == -1:
                CarteDistanceGum[x+1][y] = CarteDistanceGum[x][y]+1
                L.append((x+1,y))
            if CarteDistanceGum[x-1][y] == -1:
                CarteDistanceGum[x-1][y] = CarteDistanceGum[x][y]+1
                L.append((x-1,y))
            if CarteDistanceGum[x][y+1] == -1:
                CarteDistanceGum[x][y+1] = CarteDistanceGum[x][y]+1
                L.append((x,y+1))
            if CarteDistanceGum[x][y-1] == -1:
                CarteDistanceGum[x][y-1] = CarteDistanceGum[x][y]+1
                L.append((x,y-1))

        points.clear()
        points = [i for i in L]
        L.clear()
    return CarteDistanceGum

def CarteFantomes():
    CarteDistanceFantomes = DistanceCarteFantomesInit()
    points = []
    for i in Ghosts:
        if i[0] != 9 and i[1] != 5:
            points.append((i[0], i[1]))

    L = []
    for k in range(20):
        for i in points:
            x = i[0]
            y = i[1]
            if CarteDistanceFantomes[x+1][y] == -1:
                CarteDistanceFantomes[x+1][y] = CarteDistanceFantomes[x][y]+1
                L.append((x+1,y))
            if CarteDistanceFantomes[x-1][y] == -1:
                CarteDistanceFantomes[x-1][y] = CarteDistanceFantomes[x][y]+1
                L.append((x-1,y))
            if CarteDistanceFantomes[x][y+1] == -1:
                CarteDistanceFantomes[x][y+1] = CarteDistanceFantomes[x][y]+1
                L.append((x,y+1))
            if CarteDistanceFantomes[x][y-1] == -1:
                CarteDistanceFantomes[x][y-1] = CarteDistanceFantomes[x][y]+1
                L.append((x,y-1))
        points.clear()
        points = [i for i in L]
        L.clear()
    return CarteDistanceFantomes



enrage = 0
def PacManPossibleMove():
    L = []
    Dir = []
    x, y = PacManPos
    global enrage
    if enrage > 0:
        if (TBL[x][y - 1] == 0): L.append((0, -1, CarteDistanceFantomes[x][y - 1]))
        if (TBL[x][y + 1] == 0): L.append((0, 1, CarteDistanceFantomes[x][y + 1]))
        if (TBL[x + 1][y] == 0): L.append((1, 0, CarteDistanceFantomes[x + 1][y]))
        if (TBL[x - 1][y] == 0): L.append((-1, 0, CarteDistanceFantomes[x - 1][y]))

        Dir.append(L[0])
        L.pop(0)
        for i in L:
            if i[2] < Dir[0][2]:
                Dir.clear()
                Dir.append(i)
            if i[2] == Dir[0][2]:
                Dir.append(i)
        enrage-=1

    elif CarteDistanceFantomes[PacManPos[0]][PacManPos[1]] > 3:
        if (TBL[x][y - 1] == 0): L.append((0, -1, CarteDistanceGum[x][y-1]))
        if (TBL[x][y + 1] == 0): L.append((0, 1, CarteDistanceGum[x][y+1]))
        if (TBL[x + 1][y] == 0): L.append((1, 0, CarteDistanceGum[x+1][y]))
        if (TBL[x - 1][y] == 0): L.append((-1, 0, CarteDistanceGum[x-1][y]))

        Dir.append(L[0])
        del(L[0])

        for i in L:
            if i[2] < Dir[0][2]:
                Dir.clear()
                Dir.append(i)
            elif i[2] == Dir[0][2]:
                Dir.append(i)

    else:
        if (TBL[x][y - 1] == 0): L.append((0, -1, CarteDistanceFantomes[x][y - 1]))
        if (TBL[x][y + 1] == 0): L.append((0, 1, CarteDistanceFantomes[x][y + 1]))
        if (TBL[x + 1][y] == 0): L.append((1, 0, CarteDistanceFantomes[x + 1][y]))
        if (TBL[x - 1][y] == 0): L.append((-1, 0, CarteDistanceFantomes[x - 1][y]))
        Dir.append(L[0])
        L.pop(0)
        for i in L:
            if i[2] > Dir[0][2]:
                Dir.clear()
                Dir.append(i)
            if i[2] == Dir[0][2]:
                Dir.append(i)


    return Dir

def IAPacman():
    global CarteDistanceGum
    CarteDistanceGum = Carte()
    global PacManPos, Ghosts, score, enrage
    # deplacement Pacman
    L = PacManPossibleMove()
    choix = random.randrange(len(L))
    PacManPos[0] += L[choix][0]
    PacManPos[1] += L[choix][1]


    if(GUM[PacManPos[0], PacManPos[1]] == 1):
        GUM[PacManPos[0], PacManPos[1]] = 0
        score += 100
    if (GUM[PacManPos[0], PacManPos[1]] == 3):
        GUM[PacManPos[0], PacManPos[1]] = 0
        score += 2000
        global enrage
        enrage = 16

    for F in Ghosts:
        if F[0] == PacManPos[0] and F[1] == PacManPos[1] and enrage > 0:
            F[0] = 9
            F[1] = 4
        elif F[0] == PacManPos[0] and F[1] == PacManPos[1]:
            global LOOSE
            LOOSE = 1


    # juste pour montrer comment on se sert de la fonction SetInfo1
    for x in range(LARGEUR):
        for y in range(HAUTEUR):
            SetInfo1(x, y, CarteDistanceGum[x][y])



def CornerGetPossibility(F):
    L = []
    if TBL[F[0]-1][F[1]] == 0:
        L.append((-1, 0, Direction.GAUCHE))
    if TBL[F[0]+1][F[1]] == 0:
        L.append((1, 0, Direction.DROITE))
    if TBL[F[0]][F[1]-1] == 0:
        L.append((0, -1, Direction.HAUT))
    if TBL[F[0]][F[1]+1] == 0:
        L.append((0, 1, Direction.BAS))
    return L


def GhostsPossibleMove(F):
    L = []
    if F[3] == Direction.HAUT or F[3] == Direction.BAS:
        if TBL[F[0]-1][F[1]] == 0 or TBL[F[0]+1][F[1]] == 0:
            return CornerGetPossibility(F)
    if F[3] == Direction.GAUCHE or F[3] == Direction.DROITE:
        if TBL[F[0]][F[1]-1] == 0 or TBL[F[0]][F[1]+1] == 0:
            return CornerGetPossibility(F)


    if F[3] == Direction.HAUT:
        L.append((0, -1, Direction.HAUT))
    elif F[3] == Direction.BAS:
        L.append((0, 1, Direction.BAS))
    elif F[3] == Direction.DROITE:
        L.append((1, 0, Direction.DROITE))
    elif F[3] == Direction.GAUCHE:
        L.append((-1, 0, Direction.GAUCHE))
    return L


def IAGhosts():
    # deplacement Fantome
    for F in Ghosts:
        L = GhostsPossibleMove(F)
        choix = random.randrange(len(L))
        F[0] += L[choix][0]
        F[1] += L[choix][1]
        F[3] = L[choix][2]
        if F[0] == PacManPos[0] and F[1] == PacManPos[1] and enrage > 0:
            F[0] = 9
            F[1] = 4
        elif F[0] == PacManPos[0] and F[1] == PacManPos[1]:
            global LOOSE
            LOOSE = 1
    global CarteDistanceFantomes
    CarteDistanceFantomes = CarteFantomes()

    # juste pour montrer comment on se sert de la fonction SetInfo1
    for x in range(LARGEUR):
        for y in range(HAUTEUR):
            SetInfo2(x, y, CarteDistanceFantomes[x][y])


#  Boucle principale de votre jeu appelée toutes les 500ms

iteration = 0

def PlayOneTurn():
    global score
    global iteration
    global enrage
    color = "yellow"
    if not PAUSE_FLAG and not LOOSE:
        iteration += 1
        if iteration % 2 == 0:
            if enrage > 0:
                color = "white"
            IAPacman()
        else:
            IAGhosts()

    Affiche(PacmanColor=color, message=f"score : {score}")


###########################################:
#  demarrage de la fenetre - ne pas toucher

Window.mainloop()