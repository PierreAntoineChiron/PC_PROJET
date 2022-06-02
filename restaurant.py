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

def client(nombre_commande2):

    if nombre_commande2!=0:
        x = random.randint(1,10)
        a = random.randint(0,25)
        i=0
        while x!=0 and a!=0 :
            lock.acquire()
            if commande[i]==0 :
                commande[i]=x
                nom_commande[i]=a
                x=0
                a=0
            lock.release()
            if i==49:
                i=-1
            i+=1
        attente = random.randint(1,2)
        #time.sleep(attente)
        client(nombre_commande2-1)
    else :
        fin_de_journee.value=1

def serveur(numero,numero2,locker):
    if fin_de_journee.value == 0 or nombre_commande_servis.value <11:
        x=0
        a=0
        i=0
        while x==0 and a==0 :
            lock.acquire()
            if commande[i]!=0:
                x=commande[i]
                a=nom_commande[i]
                commande[i]=0
                nom_commande[i]=0
            lock.release()
            if i==49 :
                if fin_de_journee.value!=0 and nombre_commande_servis.value > 10:
                    break
                i=-1
            i+=1
        numero[0]=a
        numero[1]=x
        time.sleep(random.randint(1,5))
        locker.acquire()
        numero2[0]=a
        numero2[1]=x
        locker.release()
        numero[0]=0
        numero[1]=0

        if fin_de_journee.value == 0 or nombre_commande_servis.value <11:
            serveur(numero,numero2,locker)


def major_dHomme(serveur,pret_lock,pret):
    #print("je me lance")

    for i in  range(len(serveur)) :
        if serveur[i][0]!=0:
            move_to(i+1,0)         # pour effacer toute ma ligne
            erase_line_from_beg_to_curs()
            en_couleur(lyst_colors[0])
            print('Le serveur '+ str(i+1) + ' traite la commande ' + chr(ord('A')+serveur[i][0]) + ', ' +str(serveur[i][1]))
        else :
            move_to(i+1,0)         # pour effacer toute ma ligne
            erase_line_from_beg_to_curs()
            en_couleur(lyst_colors[0])
            print('Le serveur '+ str(i+1) + ' ne traite pas de commande')

    termine = []
    for i in range(len(pret)):
        pret_lock[i].acquire()
        if pret[i][0]!=0 :
            l = [pret[i][0],pret[i][1]]
            termine.append(l)
        pret_lock[i].release()
    
    if len(termine)!=0 :
        for i in termine :
            nombre_commande_servis.value+=1
            move_to(7,0)         # pour effacer toute ma ligne
            erase_line_from_beg_to_curs()
            en_couleur(lyst_colors[0])
            print('Commande '+ chr(ord('A')+i[0]) + ', ' + str(i[1]) + ' est servie au client')
    else :
        move_to(7,0)         # pour effacer toute ma ligne
        erase_line_from_beg_to_curs()
        en_couleur(lyst_colors[0])
        print("Aucune nouvelle commande servis")

    lock.acquire()
    #print("j'ai attraper le lock")
    attente=[]
    attente2=[]
    for i in range(0,50):
        if commande[i]!=0:
            l=[chr(ord('A')+nom_commande[i]),commande[i]]
            attente2.append(l)
            l=[nom_commande[i],commande[i]]
            attente.append(l)
    lock.release()
    #print("j'ai pas encore plante")
    move_to(5,0)         # pour effacer toute ma ligne
    erase_line_from_beg_to_curs()
    en_couleur(lyst_colors[0])
    print('Les commandes clients en attente : ' + str(attente2))
    move_to(6,0)         # pour effacer toute ma ligne
    erase_line_from_beg_to_curs()
    en_couleur(lyst_colors[0])
    print('Nombre de commande en attente : ' + str(len(attente)))
    
    move_to(8,0)         # pour effacer toute ma ligne
    erase_line_from_beg_to_curs()
    en_couleur(lyst_colors[0])
    print(nombre_commande_servis.value,' ',fin_de_journee.value)


    if fin_de_journee.value==0 or nombre_commande_servis.value <11:
        time.sleep(1)
        major_dHomme(serveur,pret_lock,pret)





if __name__ == "__main__" :
    lock = mp.Semaphore(1)
    servis1 = mp.Semaphore(1)
    servis2 = mp.Semaphore(1)
    servis3 = mp.Semaphore(1)
    servis4 = mp.Semaphore(1)

    fin_de_journee=mp.Value('i',0)
    nombre_commande = mp.Value('i',49)
    nombre_commande_servis=mp.Value('i',0)

    commande=mp.Array('i',50)
    nom_commande = mp.Array('i',50)

    preparation1 = mp.Array('i',2)
    preparation2 = mp.Array('i',2)
    preparation3 = mp.Array('i',2)
    preparation4 = mp.Array('i',2)
    servi1 = mp.Array('i',2)
    servi2 = mp.Array('i',2)
    servi3 = mp.Array('i',2)
    servi4 = mp.Array('i',2)


    serveur_liste = [preparation1,preparation2,preparation3,preparation4]
    pret_lock = [servis1,servis2,servis3,servis4]
    pret = [servi1,servi2,servi3,servi4]

    clientP = mp.Process(target=client,args=(10,))
    major_dHommeP = mp.Process(target=major_dHomme,args=(serveur_liste,pret_lock,pret,))
    serveur1 = mp.Process(target=serveur, args=(preparation1,servi1,servis1,))
    serveur2 = mp.Process(target=serveur, args=(preparation2,servi2,servis2,))
    serveur3 = mp.Process(target=serveur, args=(preparation3,servi3,servis3,))
    serveur4 = mp.Process(target=serveur, args=(preparation4,servi4,servis4,))

    clientP.start()
    major_dHommeP.start()
    serveur1.start()
    serveur2.start()
    serveur3.start()
    serveur4.start()

    clientP.join()
    major_dHommeP.join()
    serveur1.join()
    serveur2.join()
    serveur3.join()
    serveur4.join()

    print("Le restaurant a finit sa journée")
    attente2=[]
    for i in range(0,50):
        if commande[i]!=0:
            l=[chr(ord('A')+nom_commande[i]),commande[i]]
            attente2.append(l)
    print(attente2)


# numero = preparation
# numero2 = servi

