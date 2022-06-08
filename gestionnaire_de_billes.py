import multiprocessing as mp
import os, sys, random, time

# Quelques codes d'échappement (tous ne sont pas utilisés)
CLEARSCR="\x1B[2J\x1B[;H"          #  Clear SCreen
CLEAREOS = "\x1B[J"                #  Clear End Of Screen
CLEARELN = "\x1B[2K"               #  Clear Entire LiNe
CLEARCUP = "\x1B[1J"               #  Clear Curseur UP
GOTOYX   = "\x1B[%.2d;%.2dH"       #  ('H' ou 'f') : Goto at (y,x), voir le code

DELAFCURSOR = "\x1B[K"             #  effacer après la position du curseur
CRLF  = "\r\n"                     #  Retour à la ligne

# VT100 : Actions sur le curseur
CURSON   = "\x1B[?25h"             #  Curseur visible
CURSOFF  = "\x1B[?25l"             #  Curseur invisible

# Actions sur les caractères affichables
NORMAL = "\x1B[0m"                  #  Normal
BOLD = "\x1B[1m"                    #  Gras
UNDERLINE = "\x1B[4m"               #  Souligné

# VT100 : Couleurs : "22" pour normal intensity
CL_BLACK="\033[22;30m"                  #  Noir. NE PAS UTILISER. On verra rien !!
CL_RED="\033[22;31m"                    #  Rouge
CL_GREEN="\033[22;32m"                  #  Vert
CL_BROWN = "\033[22;33m"                #  Brun
CL_BLUE="\033[22;34m"                   #  Bleu
CL_MAGENTA="\033[22;35m"                #  Magenta
CL_CYAN="\033[22;36m"                   #  Cyan
CL_GRAY="\033[22;37m"                   #  Gris

# "01" pour quoi ? (bold ?)
CL_DARKGRAY="\033[01;30m"               #  Gris foncé
CL_LIGHTRED="\033[01;31m"               #  Rouge clair
CL_LIGHTGREEN="\033[01;32m"             #  Vert clair
CL_YELLOW="\033[01;33m"                 #  Jaune
CL_LIGHTBLU= "\033[01;34m"              #  Bleu clair
CL_LIGHTMAGENTA="\033[01;35m"           #  Magenta clair
CL_LIGHTCYAN="\033[01;36m"              #  Cyan clair
CL_WHITE="\033[01;37m"                  #  Blanc

lyst_colors=[CL_WHITE, CL_RED, CL_GREEN, CL_BROWN , CL_BLUE, CL_MAGENTA, CL_CYAN, CL_GRAY,
                CL_DARKGRAY, CL_LIGHTRED, CL_LIGHTGREEN,  CL_LIGHTBLU, CL_YELLOW, CL_LIGHTMAGENTA, CL_LIGHTCYAN]

def effacer_ecran() : print(CLEARSCR,end='')
def erase_line_from_beg_to_curs() : print("\033[1K",end='')
def curseur_invisible() : print(CURSOFF,end='')
def curseur_visible() : print(CURSON,end='')
def move_to(lig, col) : print("\033[" + str(lig) + ";" + str(col) + "f",end='')

def en_couleur(Coul) : print(Coul,end='')

def process(nb_billes,o,tours,etat):
    if nb_billes <= billes_nb_depart.value :
        while tours!=0 :
            x = 0
            attente.value +=1
            etat.value = 1
            file.acquire()
            x = demande(nb_billes,o)
            file.release()
            attente.value -=1
            etat.value = 2
            if x==1 :
                ajouter = 0
                for i in range(nb_billes) :
                    billes.acquire()
                time.sleep(2)
                for i in range(nb_billes):
                    billes.release()
                    ajouter +=1
                billes_nb.value +=ajouter
                tours-=1

    if tours==0:
        etat.value =3
        fin_de_journee.value+=1
    
    else :
        etat.value =4
        fin_de_journee.value+=1


def demande(nb_billes,o):
    u = billes_nb.value
    while nb_billes > billes_nb.value and billes_nb.value!=9:
        if u != billes_nb.value :
            u=billes_nb.value
        x=0
    if nb_billes <= billes_nb.value :
        billes_nb.value-=nb_billes
        return 1
    else :
        return 5

def major_dHomme(liste_etat,nombre_bille):
    verif =0
    while fin_de_journee.value != 4 and verif !=3:
        for i in range(4):
            move_to(i+1,0) 
            print(CLEARELN,end='')        # pour effacer toute ma ligne
            erase_line_from_beg_to_curs()
            en_couleur(lyst_colors[0])
            x = liste_etat[i].value
            if x == 1 :
                print('Le process '+ str(i+1) + " est dans l'état d'attente et il veut : " + str(nombre_bille[i]) +  " billes" )
            if x == 2 :
                print("Le process "+ str(i+1) + " a eu l'autorisation et utilise : " + str(nombre_bille[i]) + " billes")
            if x == 3 :
                print("Le process : " + str(i+1) + " a finit ses tâches")
            if x == 4 :
                print("Le process : " + str(i+1) + " a demandé plus de billes qu'il n'y en a de base")
        if fin_de_journee.value == 4 :
            verif +=1


if __name__ == "__main__" :
    effacer_ecran()
    file = mp.Semaphore(1)
    billes = mp.Semaphore(9)
    billes_nb_depart = mp.Value('i',9)
    billes_nb = mp.Value('i',9)
    attente = mp.Value('i',0)
    fin_de_journee = mp.Value('i',0)
    etat1 = mp.Value('i',0)
    etat2 = mp.Value('i',0)
    etat3 = mp.Value('i',0)
    etat4 = mp.Value('i',0)

    nombre_bille = [10,9,2,6]
    tours = [5,4,3,5]
    etat = [etat1,etat2,etat3,etat4]

    p1 = mp.Process(target=process,args=(nombre_bille[0],1,tours[0],etat1,))
    p2 = mp.Process(target=process,args=(nombre_bille[1],2,tours[1],etat2,))
    p3 = mp.Process(target=process,args=(nombre_bille[2],3,tours[2],etat3,))
    p4 = mp.Process(target=process,args=(nombre_bille[3],4,tours[3],etat4,))
    MH = mp.Process(target=major_dHomme,args=(etat,nombre_bille,))

    p1.start()
    p2.start()
    p3.start()
    p4.start()
    MH.start()

    p1.join()
    p2.join()
    p3.join()
    p4.join()
    MH.join()

    print("fin")



