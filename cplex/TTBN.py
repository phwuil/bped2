from bped2.pedigree import *
import bped2.view as pview
import sandbox.doLazyProg as laz
import sandbox.doLBP as lbp
import sandbox.doTTBN as ttbn
from time import *
import numpy as np
import matplotlib.pyplot as plt
import os, psutil
import math

f = 0.05
nb_ped = 30
nb_people = [10,20,50,100,200,300,500,1000,1500,2000,2200,2400]
nb_Gen_Max = [3,3,4,4,4,4,4,5,5,6,6,6]
# nb_people = [10,20,50,100,200,300,500,1000,1500,2000,2100,2200,2300,2400]
# nb_Gen_Max = [3,3,4,4,4,4,4,5,5,6,6,6,6,6]
nb_Gen_Min = [math.ceil(x/2) for x in nb_Gen_Max]
cl = 3

mean_gen_ttbn = []
errorValues_ttbn = []
max_ttbn = []
min_ttbn = []

mean_gen_laz = []
errorValues_laz = []
max_laz = []
min_laz = []

for p,g_max,g_min in zip(nb_people,nb_Gen_Max,nb_Gen_Min):
    tab_ttbn = np.zeros(nb_ped)
    tab_laz = np.zeros(nb_ped)
    for nb in range(nb_ped):
        nbChild = random.randint(6, 12)
        g = random.randint(g_min, g_max)
        ped = Pedigree()
        ped.gen_ped(nb, p, g, nbChild, cl, 0.03)
        bn_compact = pview.ped_to_bn_compact(ped, f)
        pview.save(ped, f'../cplex/samples/TTBN/pedigree_{p}_{g}_{nbChild}_{cl}_G{nb}')
        pview.save_bn(bn_compact, f'../cplex/bn/TTBN/bn_compact_{p}_{g}_{nbChild}_{cl}_G{nb}')

        t1 = process_time()
        ttbn.doTTBN(f'../cplex/bn/TTBN/bn_compact_{p}_{g}_{nbChild}_{cl}_G{nb}.bif')
        t2 = process_time()
        t2 = t2 - t1
        tab_ttbn[nb] = t2
        if p < 2500:
            t3 = process_time()
            laz.doLazyProg(f'../cplex/bn/TTBN/bn_compact_{p}_{g}_{nbChild}_{cl}_G{nb}.bif')
            t4 = process_time()
            t4 = t4 - t3
            tab_laz[nb] = t4
        else:
            tab_laz[nb] = None

    max_ttbn.append(tab_ttbn.max())
    min_ttbn.append(tab_ttbn.min())
    errorValues_ttbn.append(tab_ttbn.std())
    mean_gen_ttbn.append(tab_ttbn.mean())

    max_laz.append(tab_laz.max())
    min_laz.append(tab_laz.min())
    errorValues_laz.append(tab_laz.std())
    mean_gen_laz.append(tab_laz.mean())

f1 = plt.figure(1)
plt.errorbar(nb_people, mean_gen_ttbn, yerr = errorValues_ttbn, ecolor='red',color='blue')
plt.errorbar(nb_people, mean_gen_laz, yerr = errorValues_laz, ecolor='green',color='magenta')
plt.legend(['TTBN','LP'])
plt.title('Temps de calcul de l\'inférence d\'un BNC avec TTBN et LP')
plt.xlabel('Taille du pedigree')
plt.ylabel('Temps en sec')
plt.savefig('../cplex/figure/TTBN/Temps de calcul de l\'inférence d\'un BNC avec TTBN et LP',bbox_inches='tight')
f1.show()

f2 = plt.figure(2)
plt.errorbar(nb_people, mean_gen_ttbn, yerr = errorValues_ttbn, ecolor='red')
plt.title('Temps de calcul de l\'inférence d\'un BNC en fonction du pedigree avec TTBN')
plt.xlabel('Taille du pedigree')
plt.ylabel('Temps en sec')
plt.savefig('../cplex/figure/TTBN/Temps de calcul de l\'inférence d\'un BNC en fonction du pedigree avec ecart-type')
f2.show()


f3 = plt.figure(3)
plt.plot(nb_people, mean_gen_ttbn, label='mean')
plt.plot(nb_people, max_ttbn, label='max')
plt.plot(nb_people, min_ttbn, label='min')
plt.legend(['mean','max','min'])
plt.title('Temps de calcul de l\'inférence d\'un BNC en fonction du pedigree avec TTBN')
plt.xlabel('Taille du pedigree')
plt.ylabel('Temps en sec')
plt.savefig('../cplex/figure/TTBN/Temps de calcul de l\'inférence moyenne d\'un BNC, min et max en fonction du pedigree')
f3.show()

