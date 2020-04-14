from bped2.pedigree import *
import bped2.view as pview
import sandbox.doLBP as laz
from time import *
import numpy as np
import matplotlib.pyplot as plt
import os, psutil
import math

f = 0.05
nb_ped = 50
# nb_people = [10,20,50,100,200,300,500,1000,1500,2000,3000,4000,5000,7500,10000]
# nb_Gen_Max = [3,3,4,4,4,4,4,5,5,6,6,7,8,9,10]
nb_people = [10,20,50,100,200,300,500,1000,1500,2000,2100,2200,2300,2400]
nb_Gen_Max = [3,3,4,4,4,4,4,5,5,6,6,6,6,7]
nb_Gen_Min = [math.ceil(x/2) for x in nb_Gen_Max]
cl = 3

mean_gen_inf = []
errorValues_inf = []
max_inf = []
min_inf = []

for p,g_max,g_min in zip(nb_people,nb_Gen_Max,nb_Gen_Min):
    tab_inf = np.zeros(nb_ped)
    for nb in range(nb_ped):
        nbChild = random.randint(6, 12)
        g = random.randint(g_min, g_max)
        ped = Pedigree()
        ped.gen_ped(nb, p, g, nbChild, cl, 0.03)
        bn_compact = pview.ped_to_bn_compact(ped, f)
        pview.save(ped, f'../cplex/samples/LBP/pedigree_{p}_{g}_{nbChild}_{cl}_G{nb}')
        pview.save_bn(bn_compact, f'../cplex/bn/LBP/bn_compact_{p}_{g}_{nbChild}_{cl}_G{nb}')
        t1 = process_time()
        laz.doLBP(f'../cplex/bn/LBP/bn_compact_{p}_{g}_{nbChild}_{cl}_G{nb}.bif')
        t2 = process_time()
        t2 = t2 - t1
        tab_inf[nb] = t2

    max_inf.append(tab_inf.max())
    min_inf.append(tab_inf.min())
    errorValues_inf.append(tab_inf.std())
    mean_gen_inf.append(tab_inf.mean())


f1 = plt.figure(1)
plt.errorbar(nb_people, mean_gen_inf, yerr = errorValues_inf, ecolor='red')
plt.title('Temps de calcul de l\'inférence d\'un BN compact en fonction de la taille du pedigree avec LBP')
plt.xlabel('Taille du pedigree')
plt.ylabel('Temps en sec')
plt.savefig('../cplex/figure/LBP/Temps de calcul de l\'inférence d\'un BN compact en fonction de la taille du pedigree avec ecart-type')
f1.show()

f2 = plt.figure(2)
plt.plot(nb_people, mean_gen_inf, label='mean')
plt.plot(nb_people, max_inf, label='max')
plt.plot(nb_people, min_inf, label='min')
plt.legend(['mean','max','min'])
plt.title('Temps de calcul de l\'inférence d\'un BN compact en fonction de la taille du pedigree avec LBP')
plt.xlabel('Taille du pedigree')
plt.ylabel('Temps en sec')
plt.savefig('../cplex/figure/LBP/Temps de calcul de l\'inférence moyenne d\'un BN compact , min et max en fonction de la taille du pedigree')
f2.show()