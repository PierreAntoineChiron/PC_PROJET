import multiprocessing as mp
import sys,os,time,random

#-----------------------------------------------------------
def fils_calculette(queue):

    while True:
        global res
        commande = queue.get()
        print("Le fils à recu ", commande)
        res=eval(commande)

        print("Dans fils, le résultat =", res)
        queue.put(res)

        print("Le fils a envoyé", res)
        time.sleep(1)

        return
    
#-----------------------------------------------------------

if __name__ == "__main__" :
    N=4

    queue = mp.Queue()
    for i in range(N):
        calculateur = mp.Process(target=fils_calculette, args=(queue,))
        calculateur.start()
        time.sleep(0.5)

        # Le pere envoie au fils un calcul aléatoire à faire et récupère le résultat

        opd1 = random.randint(1,10)
        opd2 = random.randint(1,10)
        operateur=random.choice(['+', '-', '*', '/','**','%','//'])
        str_commande = str(opd1) + operateur + str(opd2)

        queue.put(str_commande)
        print("Le père va demander à faire : ", str_commande)
        reponse = queue.get()
        print("Le Pere a recu ", reponse)
        print('-'* 60)
        time.sleep(1)