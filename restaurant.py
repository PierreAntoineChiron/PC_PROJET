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

cpt = 0
cmd = 0

def client(nombre_commande2):
    while nombre_commande2!=0 : # tant que le nombre de commande voulue n'as pas été commandé il boucle
        if nombre_commande2!=0:
            x = random.randint(1,10) # initialise le numéro de la commande
            a = random.randint(0,25) # initialise le nom de la commande
            i=0
            while x!=0 or a!=0 : # tant que il n'as pas trouvé une place pour mettre la commande dans la liste "commande"
                lock.acquire()
                if commande[i]==0 : # si il n'y a pas de commande stockée à cette endroit
                    nombre_commande_demande.value+=1
                    commande[i]=x # on stocke la commande
                    nom_commande[i]=a # on stocke le nom de la commande
                    x=0
                    a=0
                lock.release()
                if i==49: # si on est arrivé au bout de la liste on la reparcours du début
                    i=-1
                i+=1
            attente = random.randint(1,2)
            #time.sleep(attente)
            #client(nombre_commande2-1)
            nombre_commande2-=1

    fin_de_journee.value=1
    tous_le_monde_a_fini_sema.acquire()
    tous_le_monde_a_fini.value+=1 
    tous_le_monde_a_fini_sema.release()
        

def serveur(numero,numero2,locker):
    while fin_de_journee.value == 0 or nombre_commande_servis.value <nombre_commande_voulu.value :
        time.sleep(1) # le serveur prend une petite pause
        if fin_de_journee.value == 0 or nombre_commande_servis.value <nombre_commande_voulu.value:
            x=0
            a=0
            i=0
            while x==0 and a==0 : # tant qu'il n'a pas trouvé de commande à préparer il boucle
                lock.acquire()
                if commande[i]!=0: # si il trouve une commande a préparer
                    x=commande[i] # il stocke le numéro
                    a=nom_commande[i] # il stocke le nom
                    commande[i]=0 # il remet à 0 dans la liste la commande qu'il a prise
                    nom_commande[i]=0
                lock.release()
                if i==49 : # si on arrive au bout de la liste commande on peut la reparcourir si le nombre de commande servis est toujours inférieur au nombre de commande demandée
                    if fin_de_journee.value!=0 and nombre_commande_servis.value > nombre_commande_voulu.value-1:
                        break
                    i=-1
                i+=1
            numero[0]=a # on stocke dans préparationX[0] la commande voulue
            numero[1]=x # on stocke dans préparationX[1] le nom du client
            time.sleep(random.randint(1,5))
            locker.acquire()
            numero2[0]=a # on stocke dans serviX[0] la commande qui a été faite
            numero2[1]=x # on stocke dans serviX[1] le nom du client
            locker.release()
            numero[0]=0 # on remet a 0 preparationX[0]
            numero[1]=0 # on remet a 0 preparationX[1]

    tous_le_monde_a_fini_sema.acquire()
    tous_le_monde_a_fini.value+=1
    tous_le_monde_a_fini_sema.release()


def major_dHomme(serveur,pret_lock,pret):
    while fin_de_journee.value==0 or nombre_commande_servis.value <nombre_commande_voulu.value or tous_le_monde_a_fini.value!=5 or verif.value!=1:
        lock.acquire()
        attente=[]
        attente2=[]

        for i in range(0,50): # il parcourt la list commande et stocke dans attente2 et attente toutes les commandes en attente
            if commande[i]!=0:
                l=[chr(ord('A')+nom_commande[i]),commande[i]]
                attente2.append(l)
                l=[nom_commande[i],commande[i]]
                attente.append(l)
        lock.release()

        # affichage des commandes en attente et du nombre de commande en attente
        move_to(5,0)    
        print(CLEARELN,end='')       # pour effacer toute ma ligne
        erase_line_from_beg_to_curs()
        en_couleur(lyst_colors[0])
        print( "Commande en attente : ", attente2[:])
        move_to(6,0) 
        print(CLEARELN,end='')          # pour effacer toute ma ligne
        erase_line_from_beg_to_curs()
        en_couleur(lyst_colors[0])
        print('Nombre de commande en attente : ' + str(len(attente)))


        for i in  range(len(serveur)) : # parcourt tous les serveurs
            if serveur[i][0]!=0: # si preparation[0] != 0, c'est à dire si le serveur est entrain de préparer une commande
                move_to(i+1,0) 
                print(CLEARELN,end='')        # pour effacer toute ma ligne
                erase_line_from_beg_to_curs()
                en_couleur(lyst_colors[0])
                print('Le serveur '+ str(i+1) + ' traite la commande ' + chr(ord('A')+serveur[i][0]) + ', ' +str(serveur[i][1])) # affichage de la commande en préparation
            else : # le serveur ne prépare aucune commande
                move_to(i+1,0)   
                print(CLEARELN,end='')        # pour effacer toute ma ligne
                erase_line_from_beg_to_curs()
                en_couleur(lyst_colors[0])  
                print('Le serveur '+ str(i+1) + ' ne traite pas de commande')

        termine = []
        for i in range(len(pret)): # parcours tous les commandes servit
            pret_lock[i].acquire()
            if pret[i][0]!=0 : # si servi[X] != 0 c'est à dire si le serveur X a servis une commande
                l = [chr(ord('A') + pret[i][0]),pret[i][1]]
                termine.append(l)
            pret[i][0]=0 # on remet à 0 pour ne l'afficher qu'une fois
            pret[i][1]=0 # on remet à 0 pour ne l'afficher qu'une fois
            pret_lock[i].release()


        if len(termine)!=0 : # si une commande a été servit on affiche la liste et on incrémente le nombre de commande servit
            for i in termine :
                nombre_commande_servis.value+=1
            move_to(7,0)   
            print(CLEARELN,end='')        # pour effacer toute ma ligne
            erase_line_from_beg_to_curs()
            en_couleur(lyst_colors[0])
            print('Commande servies au client : ', termine[:])
        else : # sinon on affiche qu'il n'y a eu aucune nouvelle commande de servit
            move_to(7,0) 
            print(CLEARELN,end='')          # pour effacer toute ma ligne
            erase_line_from_beg_to_curs()
            en_couleur(lyst_colors[0])
            print("Aucune nouvelle commande servies")
        

        time.sleep(1)
        if tous_le_monde_a_fini.value == 5 :
            verif.value +=1








if __name__ == "__main__" :
    effacer_ecran()
    lock = mp.Semaphore(1)
    servis1 = mp.Semaphore(1)
    servis2 = mp.Semaphore(1)
    servis3 = mp.Semaphore(1)
    servis4 = mp.Semaphore(1)
    tous_le_monde_a_fini_sema = mp.Semaphore(1)

    fin_de_journee=mp.Value('i',0)
    nombre_commande = mp.Value('i',49)
    nombre_commande_servis=mp.Value('i',0)
    nombre_commande_demande=mp.Value('i',0)
    nombre_commande_voulu=mp.Value('i',5)
    tous_le_monde_a_fini = mp.Value('i',0)
    verif = mp.Value('i',0)

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

    clientP = mp.Process(target=client,args=(nombre_commande_voulu.value,))
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
    


