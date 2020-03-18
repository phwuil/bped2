from bped2.pedigree import *
from time import clock
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
        t1 = clock()
        ped.gen_ped(nb, p, g, nbChild, cl)
        t2 = clock()
        ped.save(f'../cplex/pedigree_{p}_{g}_{nbChild}_{cl}_G{nb}')
        t2 = t2 - t1
        tab[nb] = t2
    mean.append(tab.mean())

plt.plot(nb_people,mean)
plt.xlabel('Taille de N')
plt.ylabel('Temps')
plt.show()