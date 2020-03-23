from bped2.pedigree import *
import bped2.view as pview
from time import *
import numpy as np
import matplotlib.pyplot as plt

f = 0.05
nb_ped = 50
nb_people = [10,20,50,100,200,300,500,1000]
nb_Gen_Max = [3,5,13,15,20,25,35,50]
nbChild = 4
cl = 4

mean_gen_ped = []
mean_gen_bn = []

errorValues_ped = []
errorValues_bn = []

max_ped = []
max_bn = []

min_ped = []
min_bn = []

for p,g in zip(nb_people,nb_Gen_Max):
    tab_ped = np.zeros(nb_ped)
    tab_bn = np.zeros(nb_ped)

    for nb in range(nb_ped):
        ped = Pedigree()
        t1 = process_time()
        ped.gen_ped(nb, p, g, nbChild, cl)
        t2 = process_time()
        t3 = process_time()
        ped.ped_to_bn(f)
        t4 = process_time()
        pview.save(ped,f'../cplex/samples/pedigree_{p}_{g}_{nbChild}_{cl}_G{nb}')
        t2 = t2 - t1
        t4 = t4 - t3
        tab_ped[nb] = t2
        tab_bn[nb] = t4

    max_ped.append(tab_ped.max())
    max_bn.append(tab_bn.max())

    min_ped.append(tab_ped.min())
    min_bn.append(tab_bn.min())

    errorValues_ped.append(tab_ped.std())
    errorValues_bn.append(tab_bn.std())

    mean_gen_ped.append(tab_ped.mean())
    mean_gen_bn.append(tab_bn.mean())


print('moyenne', mean_gen_ped)
print('ecart type', errorValues_ped)

f1 = plt.figure(1)
plt.errorbar(nb_people, mean_gen_ped, yerr = errorValues_ped, ecolor='red')
plt.title('Temps d\'execution en fonction de la taille du pedigree')
plt.xlabel('Taille du pedigree')
plt.ylabel('Temps en sec')
plt.savefig('../data/figure/Temps d\'execution en fonction de la taille du pedigree avec ecart-type')
f1.show()

f2 = plt.figure(2)
plt.plot(nb_people, np.log(mean_gen_ped))
plt.title('Log du temps d\'execution en fonction de la taille du pedigree')
plt.xlabel('Taille du pedigree')
plt.ylabel('log du temps en sec')
plt.savefig('../data/figure/Log du temps d\'execution en fonction de la taille du pedigree')
f2.show()

f3 = plt.figure(3)
plt.plot(nb_people, mean_gen_ped, label='mean')
plt.plot(nb_people, max_ped, label='max')
plt.plot(nb_people, min_ped, label='min')
plt.legend(['mean','max','min'])
plt.title('Temps d\'execution en fonction de la taille du pedigree')
plt.xlabel('Taille du pedigree')
plt.ylabel('Temps en sec')
plt.savefig('../data/figure/Temps d\'execution moyen, min et max en fonction de la taille du pedigree')
f3.show()

f4 = plt.figure(4)
plt.errorbar(nb_people, mean_gen_bn, yerr = errorValues_bn, ecolor='red')
plt.title('Temps de génération du BN en fonction de la taille du pedigree')
plt.xlabel('Taille du pedigree')
plt.ylabel('Temps en sec')
plt.savefig('../data/figure/Temps de génération du BN en fonction de la taille du pedigree avec ecart-type')
f1.show()

f5 = plt.figure(5)
plt.plot(nb_people, mean_gen_bn, label='mean')
plt.plot(nb_people, max_bn, label='max')
plt.plot(nb_people, min_bn, label='min')
plt.legend(['mean','max','min'])
plt.title('Temps de génération du BN en fonction de la taille du pedigree')
plt.xlabel('Taille du pedigree')
plt.ylabel('Temps en sec')
plt.savefig('../data/figure/Temps de génération du BN moyen, min et max en fonction de la taille du pedigree')
f3.show()


plt.show()
