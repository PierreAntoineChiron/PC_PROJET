# Cours hippique
# Version très basique, sans mutex sur l'écran, sans arbitre, sans annoncer le gagant, ... ...

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
#-------------------------------------------------------
import multiprocessing as mp
 
import os, time,math, random, sys, ctypes, signal
from re import M

# Définition de qq fonctions de gestion de l'écran
def effacer_ecran() : print(CLEARSCR,end='')
def erase_line_from_beg_to_curs() : print("\033[1K",end='')
def curseur_invisible() : print(CURSOFF,end='')
def curseur_visible() : print(CURSON,end='')
def move_to(lig, col) : print("\033[" + str(lig) + ";" + str(col) + "f",end='')

def en_couleur(Coul) : print(Coul,end='')
def en_rouge() : print(CL_RED,end='') # Un exemple !

#-------------------------------------------------------
# La tache d'un cheval
def un_cheval(ma_ligne : int, keep_running) : # ma_ligne commence à 0
    col=1
    t_total=0
    global position

    while col < LONGEUR_COURSE and keep_running.value :
        lock.acquire() # prend un jeton qui empêchera les autres process chevaux d'écrire si celui qui l'a pris n'as pas relachée le jeton
        move_to(ma_ligne+1,col)         # pour effacer toute ma ligne
        erase_line_from_beg_to_curs()
        en_couleur(lyst_colors[ma_ligne%len(lyst_colors)])
        print('('+chr(ord('A')+ma_ligne)+'/____\V') # changement d'apparence du cheval
        lock.release() # relache le jeton afin de laisser un autre process cheval écrire

        tab[ma_ligne]=col # stockage de l'emplacement du cheval afin d'afficher celui en tête et le dernier de la course
        col+=1
        
        temps=0.1 * random.randint(1,5)
        t_total += temps
        lock.acquire()
        seconde[ma_ligne]=t_total # stockage du temps total depuis le début de la course
        lock.release()
        try : # En cas d'interruption
            time.sleep(temps)
        finally : 
            pass

def arbitre():
    maxi =0
    mini=-1
    while maxi < LONGEUR_COURSE  and mini < LONGEUR_COURSE :
        lock.acquire()
        lst=tab[:] # récupération de la liste contenant la position des chevaux
        lock.release()
        maxi=max(lst) # récupération de la colonne du cheval gagnant
        mini = min(lst) # récupération de la colonne du cheval perdant
        ind_maxi=lst.index(maxi) # récupération de l'indice du cheval gagnant
        ind_mini=lst.index(mini) # récupaération de l'indice du cheval perdant

        if mini!=maxi : # si la course n'est pas finit, affichage du cheval gagant et perdant
            move_to(Nb_process+6,0)         # pour effacer toute ma ligne
            erase_line_from_beg_to_curs()
            en_couleur(lyst_colors[0])
            move_to(Nb_process+6,0)
            print("le cheval ", chr(ord('A')+ind_maxi), " est premier")
            move_to(Nb_process+7,0)         # pour effacer toute ma ligne
            erase_line_from_beg_to_curs()
            en_couleur(lyst_colors[0])
            move_to(Nb_process+7,0)
            print("le cheval ", chr(ord('A')+ind_mini), " est dernier")


    lock.acquire()
    sec = seconde[:] # récupération des temps totaux des chevaux
    lock.release()
    mini = min(sec) # récupération du temps total du gagnant
    ind_mini=sec.index(mini) # récupération du de l'indice du gagnant
    nom=[ind_mini]
    for i in range(Nb_process): # vérification si il y a une exaquo
        u = sec[i]
        if u == mini and i!=ind_mini :
            nom.append(i)
    if len(nom)!=1 : # affichage si exeaquo
        move_to(Nb_process+8,0)         # pour effacer toute ma ligne
        erase_line_from_beg_to_curs()
        en_couleur(lyst_colors[0])
        move_to(Nb_process+8,0)
        print("le cheval ", chr(ord('A')+nom[0]), " est exaequo ")
    


        
        
#------------------------------------------------   
def prise_en_compte_signaux(signum, frame) :
    # On vient ici en cas de CTRL-C p. ex.
    move_to(Nb_process+11, 1)
    print(f"Il y a eu interruption No {signum} au clavier ..., on finit proprement")
    
    for i in range(Nb_process): 
        mes_process[i].terminate() 
    
    move_to(Nb_process+12, 1)
    curseur_visible()
    en_couleur(CL_WHITE)
    print("Fini")
    sys.exit(0)

def prediction():
    try :
        predi = int(input("Veuillez prédire un gagnant (entrer un nombre entre 0 et 19): "))
        if predi <= 19 and predi >= 0:
            print("Bonne chance")
            return(predi)
        else:
            print("Un nombre, c'est bien, mais il est trop grand ou trop petit :( ")
            prediction()
    except :
        print("vous n'avez pas rentré un nombre, vous n'avez donc pas fait de prédiction")
        prediction()
# ---------------------------------------------------
# La partie principale :
if __name__ == "__main__" :
    predi = prediction()

    Nb_process = 20
    lock = mp.Semaphore(1) # semaphore permettant l'affichage en exclusion mutuelle
    tab=mp.Array('i', Nb_process)
    seconde=mp.Array('f', Nb_process)

    # Une liste de couleurs à affecter aléatoirement aux chevaux
    lyst_colors=[CL_WHITE, CL_RED, CL_GREEN, CL_BROWN , CL_BLUE, CL_MAGENTA, CL_CYAN, CL_GRAY,
                CL_DARKGRAY, CL_LIGHTRED, CL_LIGHTGREEN,  CL_LIGHTBLU, CL_YELLOW, CL_LIGHTMAGENTA, CL_LIGHTCYAN]
    
    LONGEUR_COURSE = 100 # Tout le monde aura la même copie (donc no need to have a 'value')
    
    keep_running=mp.Value(ctypes.c_bool, True)

    Nb_process=20
    temps_totaux = [0 for i in range(Nb_process) ]
    position = [0 for i in range(Nb_process) ]
    mes_process = [0 for i in range(Nb_process)]

    
    signal.signal(signal.SIGINT , prise_en_compte_signaux)
    signal.signal(signal.SIGQUIT , prise_en_compte_signaux)

    effacer_ecran()
    curseur_invisible()

    for i in range(Nb_process):  # Lancer     Nb_process  processus
        mes_process[i] = mp.Process(target=un_cheval, args= (i,keep_running,))
        mes_process[i].start()

    arbitre2=mp.Process(target=arbitre,args=())
    arbitre2.start()

    move_to(Nb_process+10, 1)
    print("tous lancés, Controle-C pour tout arrêter")


    # On attend la fin de la course
    for i in range(Nb_process): mes_process[i].join()
    arbitre2.join()

    move_to(Nb_process+12, 1)
    curseur_visible()
    print("Fini")
