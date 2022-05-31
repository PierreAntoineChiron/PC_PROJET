import multiprocessing as mp
import random,time

def process(nb_billes,o,tours):
    x = 0
    attente.value +=1
    #print("file : ",o, "nb_personne : ",attente.value)
    file.acquire()
    #print("attente : ",o)
    x = demande(nb_billes,o)
    file.release()
    attente.value -=1
    if x==1 :
        #print("le process : ",o," a bien recu l'autorisation de démarrer")
        for i in range(nb_billes) :
            billes.acquire()
        print("dort : ",o)
        time.sleep(random.random())
        #print("fin dodo : ",o)
        for i in range(nb_billes):
            billes.release()
            billes_nb.value +=1
        print("relaché : ",o," ",billes_nb.value)
        #print("process : ",o," a pris : ",nb_billes," et les a relachée")
        if tours !=0 :
            process(nb_billes,o,tours-1)
    else :
        print("on a un probleme")
        print(x)
    if tours==0:
        print("le process : ",o," a fini")


def demande(nb_billes,o):
    u = billes_nb.value
    while nb_billes > billes_nb.value and billes_nb.value!=9:
        if u != billes_nb.value :
            print(nb_billes, " ",billes_nb.value," ",o)
            u=billes_nb.value
        x=0
    if nb_billes <= billes_nb.value :
        billes_nb.value-=nb_billes
        return 1
    else :
        return 5

if __name__ == "__main__" :

    file = mp.Semaphore(1)
    billes = mp.Semaphore(9)
    billes_nb = mp.Value('i',9)
    attente = mp.Value('i',0)

    p1 = mp.Process(target=process,args=(8,1,5,))
    p2 = mp.Process(target=process,args=(5,2,4,))
    p3 = mp.Process(target=process,args=(2,3,3,))
    p4 = mp.Process(target=process,args=(6,4,1,))

    p1.start()
    p2.start()
    p3.start()
    p4.start()

    p1.join()
    p2.join()
    p3.join()
    p4.join()

    print("fin")


