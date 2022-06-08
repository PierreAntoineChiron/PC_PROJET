import multiprocessing as mp
import sys,os,time,random,numpy

#-----------------------------------------------------------
def fils_calculette(queue,o):

    a_envoyer = []
    while fin.value !=0 :
        commande = queue.get()
        print(commande)
        #g = lambda x : commande[0:3]
        lock_fin.acquire()
        fin.value-=1
        lock_fin.release()
        res = eval(commande[0](3))
        print(res)
        res = str(res) + str(commande[len(commande)-1])
        a_envoyer.append(res)
    
    for i in range(len(a_envoyer)):
        queue.put(a_envoyer[i])
    cf_sema.acquire()
    cf.value+=1
    cf_sema.release()

        



    
def pere_demandeur(queue,o):
    opd1 = random.randint(1,9)
    opd2 = random.randint(1,9)
    expo = lambda x : numpy.exp(x)
    operateur=random.choice(['+', '-', '*', '/','%'])
    str_commande = "x" +operateur+ str(opd1) + str(opd2)
    print("Le père "+ str(o) +  " va demander à faire : f(x) = " + str( str_commande[0:3]) + " avec x= " + str(str_commande[3]) )
    print(expo)
    str_commande = str_commande + str(o)
    queue.put(expo)
    lock_fin.acquire()
    fin.value+=1
    lock_fin.release()
    test = 0
    x=0
    while x != 3 :
        cf_sema.acquire()
        x=cf.value
        cf_sema.release()
        time.sleep(1)
        pass
    while test == 0 :
        reponse=queue.get()
        if int(reponse[len(reponse)-1])==o :
            test = 1
        else :
            queue.put(reponse)
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
    while x !=3 :
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
    