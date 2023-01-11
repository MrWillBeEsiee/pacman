import random
import tkinter as tk
from tkinter import font  as tkfont
import numpy as np


##########################################################################
#
#   Partie I : variables du jeu  -  placez votre code dans cette section
#

color = "yellow"
loose = False
score = 0
score2 = 0
super = False
compteur = 0

def Eat():
    global score
    global super
    if (GUM[PacManPos[0]][PacManPos[1]] == 1 ):
        GUM[PacManPos[0]][PacManPos[1]] = 0
        score += 100
    if (GUM[PacManPos[0]][PacManPos[1]] == 3 ):
       GUM[PacManPos[0]][PacManPos[1]] = 0
       super = True
#########################################################################

# Plan du labyrinthe

# 0 vide
# 1 mur
# 2 maison des fantomes (ils peuvent circuler mais pas pacman)

def CreateArray(L):
   T = np.array(L,dtype=np.int32)
   T = T.transpose()  ## ainsi, on peut écrire TBL[x][y]
   return T

TBL = CreateArray([
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
        [1,3,0,0,0,1,0,0,0,0,0,0,0,0,1,0,0,0,3,1],
        [1,0,1,1,0,1,0,1,1,1,1,1,1,0,1,0,1,1,0,1],
        [1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1],
        [1,0,1,0,1,1,0,1,1,2,2,1,1,0,1,1,0,1,0,1],
        [1,0,0,0,0,0,0,1,2,2,2,2,1,0,0,0,0,0,0,1],
        [1,0,1,0,1,1,0,1,1,1,1,1,1,0,1,1,0,1,0,1],
        [1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1],
        [1,0,1,1,0,1,0,1,1,1,1,1,1,0,1,0,1,1,0,1],
        [1,3,0,0,0,1,0,0,0,0,0,0,0,0,1,0,0,0,3,1],
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1] ]);

HAUTEUR = TBL.shape [1]
LARGEUR = TBL.shape [0]

# placements des pacgums et des fantomes

def PlacementsGUM():  # placements des pacgums
   GUM = np.zeros(TBL.shape,dtype=np.int32)

   for x in range(LARGEUR):
      for y in range(HAUTEUR):
         if ( TBL[x][y] == 0):
            GUM[x][y] = 1
         if ( TBL[x][y] == 3):
            GUM[x][y] = 3
   return GUM

GUM = PlacementsGUM()

PacManPos = [5,5]

Ghosts  = []
Ghosts.append(  [LARGEUR//2, HAUTEUR // 2 ,  "pink"  ,(0,-1)] )
Ghosts.append(  [LARGEUR//2, HAUTEUR // 2 ,  "orange",(0,-1)] )
Ghosts.append(  [LARGEUR//2, HAUTEUR // 2 ,  "cyan"  ,(0,-1)] )
Ghosts.append(  [LARGEUR//2, HAUTEUR // 2 ,  "red"   ,(0,-1)] )

##############################################################################
#
#   Partie II :  AFFICHAGE -- NE PAS MODIFIER  jusqu'à la prochaine section
#
##############################################################################



ZOOM = 40   # taille d'une case en pixels
EPAISS = 8  # epaisseur des murs bleus en pixels

screeenWidth = (LARGEUR+1) * ZOOM
screenHeight = (HAUTEUR+2) * ZOOM

Window = tk.Tk()
Window.geometry(str(screeenWidth)+"x"+str(screenHeight))   # taille de la fenetre
Window.title("ESIEE - PACMAN")

# gestion de la pause

PAUSE_FLAG = False

def keydown(e):
   global PAUSE_FLAG
   if e.char == ' ' :
      PAUSE_FLAG = not PAUSE_FLAG

Window.bind("<KeyPress>", keydown)
message = "Minh"

# création de la frame principale stockant plusieurs pages

F = tk.Frame(Window)
F.pack(side="top", fill="both", expand=True)
F.grid_rowconfigure(0, weight=1)
F.grid_columnconfigure(0, weight=1)


# gestion des différentes pages

ListePages  = {}
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
    MainLoop()
    Window.after(250,WindowAnim) #500

Window.after(100,WindowAnim)

# Ressources

PoliceTexte = tkfont.Font(family='Arial', size=22, weight="bold", slant="italic")

# création de la zone de dessin

Frame1 = CreerUnePage(0)

canvas = tk.Canvas( Frame1, width = screeenWidth, height = screenHeight )
canvas.place(x=0,y=0)
canvas.configure(background='black')


#  FNT AFFICHAGE


def To(coord):
   return coord * ZOOM + ZOOM

# dessine l'ensemble des éléments du jeu par dessus le décor

anim_bouche = 0
animPacman = [ 5,10,15,10,5]


def Affiche(PacmanColor,message,data1,data2,data3,data4):
   global anim_bouche

   def CreateCircle(x,y,r,coul):
      canvas.create_oval(x-r,y-r,x+r,y+r, fill=coul, width  = 0)

   canvas.delete("all")


   # murs

   for x in range(LARGEUR-1):
      for y in range(HAUTEUR):
         if ( TBL[x][y] == 1 and TBL[x+1][y] == 1 ):
            xx = To(x)
            xxx = To(x+1)
            yy = To(y)
            canvas.create_line(xx,yy,xxx,yy,width = EPAISS,fill="blue")

   for x in range(LARGEUR):
      for y in range(HAUTEUR-1):
         if ( TBL[x][y] == 1 and TBL[x][y+1] == 1 ):
            xx = To(x)
            yy = To(y)
            yyy = To(y+1)
            canvas.create_line(xx,yy,xx,yyy,width = EPAISS,fill="blue")

   # pacgum
   for x in range(LARGEUR):
      for y in range(HAUTEUR):
         if ( GUM[x][y] == 1):
            xx = To(x)
            yy = To(y)
            e = 5
            canvas.create_oval(xx-e,yy-e,xx+e,yy+e,fill="orange")

   # superpacgum
   for x in range(LARGEUR):
      for y in range(HAUTEUR):
         if ( GUM[x][y] == 3):
            xx = To(x)
            yy = To(y)
            e = 9
            canvas.create_oval(xx-e,yy-e,xx+e,yy+e,fill="orange")

   """
   #extra info
   for x in range(LARGEUR):
      for y in range(HAUTEUR):
         xx = To(x)
         yy = To(y) - 11
         txt = data1[x][y]
         canvas.create_text(xx,yy, text = txt, fill ="white", font=("Purisa", 8))

   #extra info 2
   for x in range(LARGEUR):
      for y in range(HAUTEUR):
         xx = To(x) + 10
         yy = To(y)
         txt = data2[x][y]
         canvas.create_text(xx,yy, text = txt, fill ="yellow", font=("Purisa", 8))
   """
   #extra info 3
   for x in range(LARGEUR):
      for y in range(HAUTEUR):
         xx = To(x)
         yy = To(y)
         txt = data3[x][y]
         canvas.create_text(xx,yy, text = txt, fill ="yellow", font=("Purisa", 8))

   #extra info 4
   for x in range(LARGEUR):
      for y in range(HAUTEUR):
         xx = To(x)
         yy = To(y) + 20
         txt = data4[x][y]
         canvas.create_text(xx,yy, text = txt, fill ="green", font=("Purisa", 8))

   # dessine pacman
   xx = To(PacManPos[0])
   yy = To(PacManPos[1])
   e = 20
   anim_bouche = (anim_bouche+1)%len(animPacman)
   ouv_bouche = animPacman[anim_bouche]
   tour = 360 - 2 * ouv_bouche
   canvas.create_oval(xx-e,yy-e, xx+e,yy+e, fill = PacmanColor)
   canvas.create_polygon(xx,yy,xx+e,yy+ouv_bouche,xx+e,yy-ouv_bouche, fill="black")  # bouche


   #dessine les fantomes
   dec = -3
   for P in Ghosts:
      xx = To(P[0])
      yy = To(P[1])
      e = 16

      coul = P[2]
      # corps du fantome
      CreateCircle(dec+xx,dec+yy-e+6,e,coul)
      canvas.create_rectangle(dec+xx-e,dec+yy-e,dec+xx+e+1,dec+yy+e, fill=coul, width  = 0)

      # oeil gauche
      CreateCircle(dec+xx-7,dec+yy-8,5,"white")
      CreateCircle(dec+xx-7,dec+yy-8,3,"black")

      # oeil droit
      CreateCircle(dec+xx+7,dec+yy-8,5,"white")
      CreateCircle(dec+xx+7,dec+yy-8,3,"black")

      dec += 3

   # texte

   canvas.create_text(screeenWidth // 2, screenHeight- 50 , text = "PAUSE : PRESS SPACE", fill ="yellow", font = PoliceTexte)
   canvas.create_text(screeenWidth // 2, screenHeight- 20 , text = message, fill ="yellow", font = PoliceTexte)


AfficherPage(0)

#########################################################################
#
#  Partie III :   Gestion de partie   -   placez votre code dans cette section
#

carte = CreateArray([
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
        [1,0,0,0,0,1,0,0,0,0,0,0,0,0,1,0,0,0,0,1],
        [1,0,1,1,0,1,0,1,1,1,1,1,1,0,1,0,1,1,0,1],
        [1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1],
        [1,0,1,0,1,1,0,1,1,2,2,1,1,0,1,1,0,1,0,1],
        [1,0,0,0,0,0,0,1,2,2,2,2,1,0,0,0,0,0,0,1],
        [1,0,1,0,1,1,0,1,1,1,1,1,1,0,1,1,0,1,0,1],
        [1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1],
        [1,0,1,1,0,1,0,1,1,1,1,1,1,0,1,0,1,1,0,1],
        [1,0,0,0,0,1,0,0,0,0,0,0,0,0,1,0,0,0,0,1],
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1] ]);

for x in range(20):
    for y in range(11):
        if ( carte[x][y] == 1 or carte[x][y] == 2):
            carte[x][y] = 999

def Carte():
   for x in range(LARGEUR-2):
    for y in range(HAUTEUR-2):
      if (GUM[x+1][y+1] == 1):
         carte[x+1][y+1] = 0
      elif (carte[x+1][y+1] != 999 and carte[x+1][y+1] != 0):
         carte[x+1][y+1] = 100

   for i in range(9):
    for x in range(LARGEUR-2):
        for y in range(HAUTEUR-2):

            value = carte[x+2][y+1]

            if (value > carte[x][y+1]):
               value = carte[x][y+1]

            if (value > carte[x+1][y+2]):
               value = carte[x+1][y+2]

            if (value > carte[x+1][y]):
               value = carte[x+1][y]

            if (carte[x+1][y+1] == 100):
               carte[x+1][y+1] = value + 1

            value = carte[18-x][10-y]

            if (GUM[18-x][9-y] == 1):
               carte[18-x][9-y] = 0
            elif (carte[18-x][9-y] != 999):
               carte[18-x][9-y] = 100

            if (value > carte[17-x][9-y]):
               value = carte[17-x][9-y]

            if (value > carte[19-x][9-y]):
               value = carte[19-x][9-y]

            if (value > carte[18-x][8-y]):
               value = carte[18-x][8-y]

            if (carte[18-x][9-y] == 100):
               carte[18-x][9-y] = value + 1





def GhostsMove(ghosts):
   x = ghosts[0]
   y = ghosts[1]
   gp = GhostsPossibleMove(x,y)

   if (TBL[x+ghosts[3][0]][y+ghosts[3][1]] == 1 or len(gp) > 2):
      if (TBL[x  ][y-1] == 1 and TBL[x  ][y+1] == 1):
         list = [(-1,0), (1,0)]
         ghosts[3] = random.choice(list)
      elif (TBL[x-1][y  ] == 1 and TBL[x+1][y  ] == 1):
         list = [(0,-1), (0,1)]
         ghosts[3] = random.choice(list)

   if (TBL[x+ghosts[3][0]][y+ghosts[3][1]] == 1 or len(gp) > 2):
      ghosts[3] = random.choice(GhostsPossibleMove(x,y))



carteghosts = CreateArray([
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
        [1,0,0,0,0,1,0,0,0,0,0,0,0,0,1,0,0,0,0,1],
        [1,0,1,1,0,1,0,1,1,1,1,1,1,0,1,0,1,1,0,1],
        [1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1],
        [1,0,1,0,1,1,0,1,1,2,2,1,1,0,1,1,0,1,0,1],
        [1,0,0,0,0,0,0,1,2,2,2,2,1,0,0,0,0,0,0,1],
        [1,0,1,0,1,1,0,1,1,1,1,1,1,0,1,1,0,1,0,1],
        [1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1],
        [1,0,1,1,0,1,0,1,1,1,1,1,1,0,1,0,1,1,0,1],
        [1,0,0,0,0,1,0,0,0,0,0,0,0,0,1,0,0,0,0,1],
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1] ]);

for x in range(20):
    for y in range(11):
        if ( carteghosts[x][y] == 1 or carteghosts[x][y] == 2):
            carteghosts[x][y] = 999


def Carteghosts():

   for x in range(LARGEUR-2):
    for y in range(HAUTEUR-2):
      if (carteghosts[x+1][y+1] != 999):
         carteghosts[x+1][y+1] = 100

   for F in Ghosts:
      carteghosts[F[0]][F[1]] = 0

   for i in range(20 ):
    for x in range(LARGEUR-2):
        for y in range(HAUTEUR-2):

            value = 99

            if (value > carteghosts[x+2][y+1]):
               value = carteghosts[x+2][y+1]

            if (value > carteghosts[x][y+1]):
               value = carteghosts[x][y+1]

            if (value > carteghosts[x+1][y+2]):
               value = carteghosts[x+1][y+2]

            if (value > carteghosts[x+1][y]):
               value = carteghosts[x+1][y]

            if (carteghosts[x+1][y+1] != 999):
               carteghosts[x+1][y+1] = value + 1

            value = 99

            for F in Ghosts:
               carteghosts[F[0]][F[1]] = 0

            if (value > carteghosts[18-x][10-y]):
               value = carteghosts[18-x][10-y]

            if (value > carteghosts[17-x][9-y]):
               value = carteghosts[17-x][9-y]

            if (value > carteghosts[19-x][9-y]):
               value = carteghosts[19-x][9-y]

            if (value > carteghosts[18-x][8-y]):
               value = carteghosts[18-x][8-y]

            if (carteghosts[18-x][9-y] != 999):
               carteghosts[18-x][9-y] = value + 1

#########################################################################

def PacManPossibleMove():
   L = []
   x,y = PacManPos
   if ( TBL[x  ][y-1] == 0 ): L.append((0,-1))
   if ( TBL[x  ][y+1] == 0 ): L.append((0, 1))
   if ( TBL[x+1][y  ] == 0 ): L.append(( 1,0))
   if ( TBL[x-1][y  ] == 0 ): L.append((-1,0))
   return L

def GhostsPossibleMove(x,y):
   L = []
   if ( TBL[x  ][y-1] == 2 or TBL[x  ][y-1] == 0): L.append((0,-1))
   if ( TBL[x  ][y+1] == 2 or TBL[x  ][y+1] == 0): L.append((0, 1))
   if ( TBL[x+1][y  ] == 2 or TBL[x+1][y  ] == 0): L.append(( 1,0))
   if ( TBL[x-1][y  ] == 2 or TBL[x-1][y  ] == 0): L.append((-1,0))
   return L

def IA():

   global loose
   global PacManPos, Ghosts
   global score2
   #deplacement Pacman

   """
   choix = random.randrange(len(L))
   PacManPos[0] += L[choix][0]
   PacManPos[1] += L[choix][1]
   """
   for F in Ghosts:
      if (not super):
         if (PacManPos[0] == F[0] and PacManPos[1] == F[1]):
            loose = True
      if (super):
         if (PacManPos[0] == F[0] and PacManPos[1] == F[1]):
            F[0] = LARGEUR//2
            F[1] = HAUTEUR//2
            score2 += 2000

   #deplacement Fantome
   for F in Ghosts:
      GhostsMove(F)
      F[0] += F[3][0]
      F[1] += F[3][1]
      if (not super):
         if (PacManPos[0] == F[0] and PacManPos[1] == F[1]):
            loose = True
      if (super):
         if (PacManPos[0] == F[0] and PacManPos[1] == F[1]):
            F[0] = LARGEUR//2
            F[1] = HAUTEUR//2
            score2 += 2000

   L = PacManPossibleMove()

   x=0
   y=0
   min = 100
   max = -100
   if (carteghosts[PacManPos[0]][PacManPos[1]] > 3 and not super):
      if min > carte[PacManPos[0]-1][PacManPos[1]]:
         min = carte[PacManPos[0]-1][PacManPos[1]]
         x = -1
         y = 0
      if min > carte[PacManPos[0]+1][PacManPos[1]]:
         min = carte[PacManPos[0]+1][PacManPos[1]]
         x = 1
         y = 0
      if min > carte[PacManPos[0]][PacManPos[1]-1]:
         min = carte[PacManPos[0]][PacManPos[1]-1]
         x = 0
         y = -1
      if min > carte[PacManPos[0]][PacManPos[1]+1]:
         min = carte[PacManPos[0]][PacManPos[1]+1]
         x = 0
         y = 1

   elif (carteghosts[PacManPos[0]][PacManPos[1]] < 4 and not super):
      if max < carteghosts[PacManPos[0]-1][PacManPos[1]] and carteghosts[PacManPos[0]-1][PacManPos[1]] < 900 :
         max = carteghosts[PacManPos[0]-1][PacManPos[1]]
         x = -1
         y = 0
      if max < carteghosts[PacManPos[0]+1][PacManPos[1]] and carteghosts[PacManPos[0]+1][PacManPos[1]] < 999 :
         max = carteghosts[PacManPos[0]+1][PacManPos[1]]
         x = 1
         y = 0
      if max < carteghosts[PacManPos[0]][PacManPos[1]-1] and carteghosts[PacManPos[0]][PacManPos[1]-1] < 999 :
         max = carteghosts[PacManPos[0]][PacManPos[1]-1]
         x = 0
         y = -1
      if max < carteghosts[PacManPos[0]][PacManPos[1]+1] and carteghosts[PacManPos[0]][PacManPos[1]+1] < 999 :
         max = carteghosts[PacManPos[0]][PacManPos[1]+1]
         x = 0
         y = 1

   elif (super):
      if min > carteghosts[PacManPos[0]-1][PacManPos[1]] and carte[PacManPos[0]-1][PacManPos[1]] != 999:
         min = carteghosts[PacManPos[0]-1][PacManPos[1]]
         x = -1
         y = 0
      if min > carteghosts[PacManPos[0]+1][PacManPos[1]] and carte[PacManPos[0]+1][PacManPos[1]] != 999:
         min = carteghosts[PacManPos[0]+1][PacManPos[1]]
         x = 1
         y = 0
      if min > carteghosts[PacManPos[0]][PacManPos[1]-1] and carte[PacManPos[0]][PacManPos[1]-1] != 999:
         min = carteghosts[PacManPos[0]][PacManPos[1]-1]
         x = 0
         y = -1
      if min > carteghosts[PacManPos[0]][PacManPos[1]+1] and carte[PacManPos[0]][PacManPos[1]+1] != 999:
         min = carteghosts[PacManPos[0]][PacManPos[1]+1]
         x = 0
         y = 1

   PacManPos[0] += x
   PacManPos[1] += y

   Carte()
   Carteghosts()

#  Boucle principale de votre jeu appelée toutes les 500ms
def MainLoop():
  global compteur
  global score
  global super
  if (not PAUSE_FLAG and not loose): IA()
  global color
  Affiche(PacmanColor = color, message = message, data1=TBL, data2=GUM, data3 = carte, data4 = carteghosts)
  Eat()
  if (super):
      color = "blue"
      global compteur
      compteur += 1
      if (compteur >= 16):
         compteur = 0
         super = False
  if (not super):
     color = "yellow"
  canvas.create_text(screeenWidth - 50, screenHeight- 50 , text = score + score2, fill ="yellow", font = PoliceTexte)
  canvas.create_text( 50, screenHeight- 50 , text = compteur, fill ="yellow", font = PoliceTexte)
###########################################:
#  demarrage de la fenetre - ne pas toucher

Window.mainloop()