from bped2.pedigree import *
import bped2.view as pview
import sandbox.doLazyProg as laz
import sandbox.doLBP as lbp
from time import *
import numpy as np
import matplotlib.pyplot as plt
import os, psutil
import math

f = 0.05
nb_ped = 30
# nb_people = [10,20,50,100,200,300,500,1000,1500,2000,2200,2400,3000,4000,5000,7500,9000]
# nb_Gen_Max = [3,3,4,4,4,4,4,5,5,6,6,6,6,7,8,9,10]
nb_people = [10,20,50,100,200,300,500,1000,1500,2000,2100,2200,2300,2400]
nb_Gen_Max = [3,3,4,4,4,4,4,5,5,6,6,6,6,6]
nb_Gen_Min = [math.ceil(x/2) for x in nb_Gen_Max]
cl = 3

mean_gen_lbp = []
errorValues_lbp = []
max_lbp = []
min_lbp = []

mean_gen_laz = []
errorValues_laz = []
max_laz = []
min_laz = []

file = open('./data/data_lbp','w')
sen = Pedigree()
sen.load('../data/ped/senegal2013.ped')
len_sen = len(sen)

bn_sen = pview.ped_to_bn_compact(sen,f)
ie = pview.gum.LazyPropagation(bn_sen)
t1 = process_time()
ie.makeInference()
t2 = process_time()
time_sen_Lazy = t2 - t1

bn_sen = pview.ped_to_bn_compact(sen,f)
ie = pview.gum.LoopyBeliefPropagation(bn_sen)
t1 = process_time()
ie.makeInference()
t2 = process_time()
time_sen_LBP = t2 - t1

for p,g_max,g_min in zip(nb_people,nb_Gen_Max,nb_Gen_Min):
    tab_lbp = np.zeros(nb_ped)
    tab_laz = np.zeros(nb_ped)
    for nb in range(nb_ped):
        nbChild = random.randint(6, 12)
        g = random.randint(g_min, g_max)
        ped = Pedigree()
        ped.gen_ped(nb, p, g, nbChild, cl, 0.03)
        bn_compact = pview.ped_to_bn_compact(ped, f)
        pview.save(ped, f'../cplex/samples/LBP/pedigree_{p}_{g}_{nbChild}_{cl}_G{nb}')
        pview.save_bn(bn_compact, f'../cplex/bn/LBP/bn_compact_{p}_{g}_{nbChild}_{cl}_G{nb}')

        t1 = process_time()
        lbp.doLBP(f'../cplex/bn/LBP/bn_compact_{p}_{g}_{nbChild}_{cl}_G{nb}.bif')
        t2 = process_time()
        t2 = t2 - t1
        tab_lbp[nb] = t2
        file.write(f'{nb}\t{t2}\n')
        if p < 2500:
            t3 = process_time()
            laz.doLazyProg(f'../cplex/bn/LBP/bn_compact_{p}_{g}_{nbChild}_{cl}_G{nb}.bif')
            t4 = process_time()
            t4 = t4 - t3
            tab_laz[nb] = t4
        else:
            tab_laz[nb] = None

    file.write('-\n')
    max_lbp.append(tab_lbp.max())
    min_lbp.append(tab_lbp.min())
    errorValues_lbp.append(tab_lbp.std())
    mean_gen_lbp.append(tab_lbp.mean())

    max_laz.append(tab_laz.max())
    min_laz.append(tab_laz.min())
    errorValues_laz.append(tab_laz.std())
    mean_gen_laz.append(tab_laz.mean())

file.close()
f1 = plt.figure(1)
plt.errorbar(nb_people, mean_gen_lbp, yerr = errorValues_lbp, ecolor='red')
plt.errorbar(nb_people, mean_gen_laz, yerr = errorValues_laz, ecolor='green')
plt.plot(len_sen, time_sen_Lazy, 'xg')
plt.plot(len_sen, time_sen_LBP, 'xr')
plt.legend(['lbp','lazy','sen_lazy','sen_lbp'])
plt.title('Temps de calcul de l\'inférence d\'un BNC avec LBP et LP')
plt.xlabel('Taille du pedigree')
plt.ylabel('Temps en sec')
plt.savefig('../cplex/figure/LBP/Temps de calcul de l\'inférence d\'un BN compact en fonction de la taille du pedigree avec ecart-type')
f1.show()

#
# f1 = plt.figure(1)
# plt.plot(nb_people, mean_gen_lbp, label='mean')
# plt.plot(nb_people, max_lbp, label='max')
# plt.plot(nb_people, min_lbp, label='min')
# plt.legend(['mean','max','min'])
# plt.title('Temps de calcul de l\'inférence d\'un BNC en fonction du pedigree avec LBP')
# plt.xlabel('Taille du pedigree')
# plt.ylabel('Temps en sec')
# plt.savefig('../cplex/figure/LBP/Temps de calcul de l\'inférence moyenne d\'un BNC, min et max en fonction du pedigree')
# f1.show()
#
# f2 = plt.figure(2)
# plt.errorbar(nb_people, mean_gen_lbp, yerr = errorValues_lbp, ecolor='red')
# plt.title('Temps de calcul de l\'inférence d\'un BNC en fonction du pedigree avec LBP')
# plt.xlabel('Taille du pedigree')
# plt.ylabel('Temps en sec')
# plt.savefig('../cplex/figure/LBP/Temps de calcul de l\'inférence d\'un BNC en fonctiondu pedigree avec ecart-type')
# f2.show()