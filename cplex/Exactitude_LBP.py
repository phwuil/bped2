from bped2.pedigree import *
import bped2.view as pview
import sandbox.doLazyProg as laz
from time import *
import numpy as np
import matplotlib.pyplot as plt
import os, psutil
import math

f = 0.05
nb_ped = 50
nb_people = [10,20,50,100,200,300,500,1000,1500,2000,2100,2200,2300,2400]
#nb_Gen_Max = [3,4,7,10,15,20,25,30,35,40,50,60,70,80]
nb_Gen_Max = [3,3,4,4,4,4,4,5,5,6,6,6,6,7]
nb_Gen_Min = [math.ceil(x/2) for x in nb_Gen_Max]
cl = 3

mean_gen_diff = []
errorValues_diff = []
max_diff = []
min_diff = []

for p,g_max,g_min in zip(nb_people,nb_Gen_Max,nb_Gen_Min):
    tab_diff = np.zeros(nb_ped)
    for nb in range(nb_ped):
        nbChild = random.randint(6,12)
        g = random.randint(g_min,g_max)
        ped = Pedigree()
        ped.gen_ped(nb, p, g, nbChild, cl, 0.03)
        bn_compact = pview.ped_to_bn_compact(ped, f)
        pview.save(ped, f'../cplex/samples/LBP/pedigree_{p}_{g}_{nbChild}_{cl}_G{nb}')
        pview.save_bn(bn_compact, f'../cplex/bn/LBP/bn_compact_{p}_{g}_{nbChild}_{cl}_G{nb}')
        bn1 = pview.gum.BayesNet()
        bn1.loadBIF(f'../cplex/bn/LBP/bn_compact_{p}_{g}_{nbChild}_{cl}_G{nb}.bif')
        p1 = pview.gum.LoopyBeliefPropagation(bn1)

        bn2 = pview.gum.BayesNet()
        bn2.loadBIF(f'../cplex/bn/LBP/bn_compact_{p}_{g}_{nbChild}_{cl}_G{nb}.bif')
        p2 = pview.gum.LazyPropagation(bn2)

        tab_diff[nb] = (p1-p2).abs().max()

    max_diff.append(tab_diff.max())
    min_diff.append(tab_diff.min())
    errorValues_diff.append(tab_diff.std())
    mean_gen_diff.append(tab_diff.mean())

f1 = plt.figure(1)
plt.errorbar(nb_people, mean_gen_diff, yerr = errorValues_diff, ecolor='red')
plt.title('Temps de calcul de l\'inférence d\'un BN compact en fonction de la taille du pedigree avec LBP')
plt.xlabel('Taille du pedigree')
plt.ylabel('Différence')
plt.savefig('../cplex/figure/LBP/Différence de valeur d\'inférence entre LP et LBP en fonction de la taille du pedigree avec ecart-type')
f1.show()

f2 = plt.figure(2)
plt.plot(nb_people, mean_gen_diff, label='mean')
plt.plot(nb_people, max_diff, label='max')
plt.plot(nb_people, min_diff, label='min')
plt.legend(['mean','max','min'])
plt.title('Temps de calcul de l\'inférence d\'un BN compact en fonction de la taille du pedigree avec LBP')
plt.xlabel('Taille du pedigree')
plt.ylabel('Différence')
plt.savefig('../cplex/figure/LBP/Différence de valeur d\'inférence moyenne entre LP et LBP, min et max en fonction de la taille du pedigree')
f2.show()