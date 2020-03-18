from bped2.pedigree import *
from time import *
import numpy as np
import matplotlib.pyplot as plt

nb_ped = 50
nb_people = [10,20,50,100,200,300,500,1000]
nb_Gen_Max = [3,5,13,15,20,25,35,50]
nbChild = 4
cl = 4
mean = []

for p,g in zip(nb_people,nb_Gen_Max):
    tab = np.zeros(nb_ped)
    for nb in range(nb_ped):
        ped = Pedigree()
        t1 = process_time()
        ped.gen_ped(nb, p, g, nbChild, cl)
        t2 = process_time()
        ped.save(f'../cplex/pedigree_{p}_{g}_{nbChild}_{cl}_G{nb}')
        t2 = t2 - t1
        tab[nb] = t2
    mean.append(tab.mean())

f1 = plt.figure(1)
plt.plot(nb_people,mean)
plt.title('Temps d\'execution en fonction de la taille du pedigree')
plt.xlabel('Taille du pedigree')
plt.ylabel('Temps en sec')
plt.savefig('../data/figure/Temps d\'execution en fonction de la taille du pedigree')
f1.show()

f2 = plt.figure(2)
plt.plot(nb_people,np.log(mean))
plt.title('Log du temps d\'execution en fonction de la taille du pedigree')
plt.xlabel('Taille du pedigree')
plt.ylabel('log du temps en sec')
plt.savefig('../data/figure/Log du temps d\'execution en fonction de la taille du pedigree')
f2.show()