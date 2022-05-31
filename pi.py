from ast import arg
import random, time
import multiprocessing as mp

temps1 = time.time()
# calculer le nbr de hits dans un cercle unitaire (utilisé par les différentes méthodes)
def frequence_de_hits_pour_n_essais1(nb_iteration):
    count = 0
    for i in range(nb_iteration):
        x = random.random()
        y = random.random()
        # si le point est dans l’unit circle
        if x * x + y * y <= 1: count += 1
    lock.acquire()
    hit.value+=count
    lock.release()

def frequence_de_hits_pour_n_essais2(nb_iteration):
    count = 0
    for i in range(nb_iteration):
        x = -random.random()
        y = random.random()
        # si le point est dans l’unit circle
        if x * x + y * y <= 1: count += 1
    lock.acquire()
    hit.value+=count
    lock.release()

def frequence_de_hits_pour_n_essais3(nb_iteration):
    count = 0
    for i in range(nb_iteration):
        x = random.random()
        y = -random.random()
        # si le point est dans l’unit circle
        if x * x + y * y <= 1: count += 1
    lock.acquire()
    hit.value+=count
    lock.release()

def frequence_de_hits_pour_n_essais4(nb_iteration):
    count = 0
    for i in range(nb_iteration):
        x = -random.random()
        y = -random.random()
        # si le point est dans l’unit circle
        if x * x + y * y <= 1: count += 1
    lock.acquire()
    hit.value+=count
    lock.release()

# Nombre d’essai pour l’estimation
hit = mp.Value('i',0)
lock = mp.Semaphore(1)
nb_total_iteration = 2500000

process1 = mp.Process(target=frequence_de_hits_pour_n_essais1,args=(nb_total_iteration,))
process2 = mp.Process(target=frequence_de_hits_pour_n_essais2,args=(nb_total_iteration,))
process3 = mp.Process(target=frequence_de_hits_pour_n_essais3,args=(nb_total_iteration,))
process4 = mp.Process(target=frequence_de_hits_pour_n_essais4,args=(nb_total_iteration,))

process1.start()
process2.start()
process3.start()
process4.start()

process1.join()
process2.join()
process3.join()
process4.join()

temps2 = time.time()
print("multiprocess : ")
print("Le temps nécessaire au calcul de pi est ",temps2-temps1)
print("Valeur estimée Pi par la méthode Mono−Processus : ", hit.value / nb_total_iteration)


def frequence_de_hits_pour_n_essais(nb_iteration):
    count = 0
    for i in range(nb_iteration):
        x = random.random()
        y = random.random()
        # si le point est dans l’unit circle
        if x *x + y *y <= 1: count += 1
    return count
# Nombre d’essai pour l’estimation
nb_total_iteration = 10000000
temps3=time.time()
nb_hits=frequence_de_hits_pour_n_essais(nb_total_iteration)
temps4 = time.time()
print("mono_process : ")
print("Le temps nécessaire au calcul de pi est ",temps4-temps3)
print("Valeur estimée Pi par la méthode Mono−Processus : ", 4 * nb_hits / nb_total_iteration)
#TRACE :
# Calcul Mono−Processus : Valeur estimée Pi par la méthode Mono−Processus : 3.1412604