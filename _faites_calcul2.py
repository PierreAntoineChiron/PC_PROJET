import multiprocessing as mp
import sys,os,time,random

#-----------------------------------------------------------
def fils_calculette(queue,o):

    a_envoyer = []
    while fin.value !=0 : # boucle tant que toutes les calculs ne sont pas récupérée
        commande = queue.get() # récupère le calcul à faire
        res=eval(commande[:-1]) # résout le calcul en enlevant l'identifiant
        lock_fin.acquire()
        fin.value-=1
        lock_fin.release()
        res = str(res) + str(commande[len(commande)-1]) # rajoute l'identifiant à la réponse
        a_envoyer.append(res) #stocke dans la liste a_envoyer
    
    for i in range(len(a_envoyer)): # envoie toutes le réponses qu'il a calculer 
        queue.put(a_envoyer[i])
    cf_sema.acquire()
    cf.value+=1
    cf_sema.release()

        



    
def pere_demandeur(queue,o):
    opd1 = random.randint(1,10)
    opd2 = random.randint(1,10)
    operateur=random.choice(['+', '-', '*', '/','**','%','//'])
    str_commande = str(opd1) + operateur + str(opd2) # création du calcul demandé
    print("Le père "+str(o) +  " va demander à faire : ", str_commande)
    str_commande = str_commande + str(o) # ajout de l'identifiant du père
    queue.put(str_commande) # envoie de la commande
    lock_fin.acquire()
    fin.value+=1 # incrémentation de fin
    lock_fin.release()
    test = 0
    x=0
    while x != 3 : # on attend que toutes les réponses aient été envoyé dans la file
        cf_sema.acquire()
        x=cf.value
        cf_sema.release()
        time.sleep(1)
        pass
    while test == 0 : # attend que le père trouve sa réponse
        reponse=queue.get()
        if int(reponse[len(reponse)-1])==o : # vérifie  l'identifant de la réponse qu'il a récupérée
            test = 1
        else :
            queue.put(reponse) # renvoie la réponse si ce n'est pas la sienne
        time.sleep(1)
    print("Le Pere  " + str(o) + " a recu ", reponse[:-1])

#-----------------------------------------------------------

if __name__ == "__main__" :

    lock_fin = mp.Semaphore(1)
    fin = mp.Value('i',0)  

    cf = mp.Value('i',0)
    cf_sema = mp.Semaphore(1)

    queue = mp.Queue()
    


    pere_demandeur1 = mp.Process(target=pere_demandeur, args=(queue,1,))
    pere_demandeur2 = mp.Process(target=pere_demandeur, args=(queue,2,))
    pere_demandeur3 = mp.Process(target=pere_demandeur, args=(queue,3,))
    pere_demandeur1.start()
    pere_demandeur2.start()
    pere_demandeur3.start()

    x=0
    while x !=3 : # attend que tous les calculs aient été envoyé
        lock_fin.acquire()
        x=fin.value
        lock_fin.release()
        pass

    calculateur1 = mp.Process(target=fils_calculette, args=(queue,1,))
    calculateur2 = mp.Process(target=fils_calculette, args=(queue,2,))
    calculateur3 = mp.Process(target=fils_calculette, args=(queue,3,))
    calculateur1.start()
    calculateur2.start()
    calculateur3.start()


    pere_demandeur1.join()
    pere_demandeur2.join()
    pere_demandeur3.join()
    calculateur1.join()
    calculateur2.join()
    calculateur3.join()
    print("Fin")
    