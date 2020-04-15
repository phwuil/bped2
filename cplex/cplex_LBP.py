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
nb_ped = 50
# nb_people = [10,20,50,100,200,300,500,1000,1500,2000,3000,4000,5000,7500,10000]
# nb_Gen_Max = [3,3,4,4,4,4,4,5,5,6,6,7,8,9,10]
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

        t3 = process_time()
        laz.doLazyProg(f'../cplex/bn/LBP/bn_compact_{p}_{g}_{nbChild}_{cl}_G{nb}.bif')
        t4 = process_time()

        t2 = t2 - t1
        t4 = t4 - t3

        tab_lbp[nb] = t2
        tab_laz[nb] = t4

    max_lbp.append(tab_lbp.max())
    min_lbp.append(tab_lbp.min())
    errorValues_lbp.append(tab_lbp.std())
    mean_gen_lbp.append(tab_lbp.mean())

    max_laz.append(tab_laz.max())
    min_laz.append(tab_laz.min())
    errorValues_laz.append(tab_laz.std())
    mean_gen_laz.append(tab_laz.mean())

f3 = plt.figure(3)
plt.errorbar(nb_people, mean_gen_lbp, yerr = errorValues_lbp, ecolor='red')
plt.errorbar(nb_people, mean_gen_laz, yerr = errorValues_laz, ecolor='green')
plt.legend(['lbp','lazy'])
plt.title('Temps de calcul de l\'inférence d\'un BN compact en fonction de la taille du pedigree avec LBP')
plt.xlabel('Taille du pedigree')
plt.ylabel('Temps en sec')
plt.savefig('../cplex/figure/LBP/Temps de calcul de l\'inférence d\'un BN compact en fonction de la taille du pedigree avec ecart-type')
f3.show()

x = nb_ped * len(nb_people)
tmp = nb_people.copy()
tmp.append(5000)
tmp.append(7500)
gen = random.randint(5,10)
c = random.randint(6, 12)
ped_5000 = Pedigree()
ped_5000.gen_ped(1, 5000, gen, c, cl, 0.03)
bn_5000 = pview.ped_to_bn_compact(ped_5000, f)
pview.save(ped_5000, f'../cplex/samples/LBP/pedigree_{5000}_{gen}_{c}_{cl}_G{1}')
pview.save_bn(bn_5000, f'../cplex/bn/LBP/bn_compact_{5000}_{gen}_{c}_{cl}_G{1}')
t1 = process_time()
lbp.doLBP(f'../cplex/bn/LBP/bn_compact_{5000}_{gen}_{c}_{cl}_G{1}.bif')
t2 = process_time()
t2 = t2 - t1
mean_gen_lbp.append(t2)
errorValues_lbp.append(0)

gen = random.randint(6,11)
c = random.randint(6, 12)
ped_7500 = Pedigree()
ped_7500.gen_ped(1, 7500, gen, c, cl, 0.03)
bn_10000 = pview.ped_to_bn_compact(ped_7500, f)
pview.save(ped_5000, f'../cplex/samples/LBP/pedigree_{7500}_{gen}_{c}_{cl}_G{1}')
pview.save_bn(bn_5000, f'../cplex/bn/LBP/bn_compact_{7500}_{gen}_{c}_{cl}_G{1}')
t1 = process_time()
lbp.doLBP(f'../cplex/bn/LBP/bn_compact_{7500}_{gen}_{c}_{cl}_G{1}.bif')
t2 = process_time()
t2 = t2 - t1
mean_gen_lbp.append(t2)
errorValues_lbp.append(0)

f1 = plt.figure(1)
plt.errorbar(tmp, mean_gen_lbp, yerr = errorValues_lbp, ecolor='red')
plt.errorbar(nb_people, mean_gen_laz, yerr = errorValues_laz, ecolor='green')
plt.legend(['lbp','lazy'])
plt.title('Temps de calcul de l\'inférence d\'un BN compact en fonction de la taille du pedigree avec LBP')
plt.xlabel('Taille du pedigree')
plt.ylabel('Temps en sec')
plt.savefig('../cplex/figure/LBP/Temps de calcul de l\'inférence d\'un BN compact en fonction de la taille du pedigree avec ecart-type')
f1.show()

f2 = plt.figure(2)
plt.plot(nb_people, mean_gen_lbp, label='mean')
plt.plot(nb_people, max_lbp, label='max')
plt.plot(nb_people, min_lbp, label='min')
plt.legend(['mean','max','min'])
plt.title('Temps de calcul de l\'inférence d\'un BN compact en fonction de la taille du pedigree avec LBP')
plt.xlabel('Taille du pedigree')
plt.ylabel('Temps en sec')
plt.savefig('../cplex/figure/LBP/Temps de calcul de l\'inférence moyenne d\'un BN compact , min et max en fonction de la taille du pedigree')
f2.show()