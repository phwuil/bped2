from bped2.pedigree import *
import bped2.view as pview
import sandbox.doLazyProg as laz
from time import *
import numpy as np
import matplotlib.pyplot as plt
import os, psutil

f = 0.05
nb_ped = 50
nb_people = [10,20,50,100,200,300,500,1000,1500,2000,2500]
nb_Gen_Max = [3,5,13,15,20,25,35,50,57,65,75]
nb_Gen_Min = [x//2 for x in nb_Gen_Max]
nbChild = 4
cl = 4

mean_gen_ped = []
mean_gen_bn = []
mean_gen_inf = []
mean_mem = []

errorValues_ped = []
errorValues_bn = []
errorValues_inf = []
errorValues_mem = []

max_ped = []
max_bn = []
max_inf = []
max_mem = []

min_ped = []
min_bn = []
min_inf = []
min_mem = []

pid = os.getpid()
py = psutil.Process(pid)

for p,g_max,g_min in zip(nb_people,nb_Gen_Max,nb_Gen_Min):
    tab_ped = np.zeros(nb_ped)
    tab_bn = np.zeros(nb_ped)
    tab_inf = np.zeros(nb_ped)
    tab_mem = np.zeros(nb_ped)

    for nb in range(nb_ped):
        g = random.randint(g_min,g_max)
        ped = Pedigree()
        t1 = process_time()
        ped.gen_ped(nb, p, g, nbChild, cl)
        t2 = process_time()

        t3 = process_time()
        bn = pview.ped_to_bn(ped,f)
        t4 = process_time()

        pview.save(ped,f'../cplex/samples/pedigree_{p}_{g}_{nbChild}_{cl}_G{nb}')
        pview.save_bn(bn,f'../cplex/bn/bn_{p}_{g}_{nbChild}_{cl}_G{nb}')

        t5 = process_time()
        laz.doLazyProg(f"../cplex/bn/bn_{p}_{g}_{nbChild}_{cl}_G{nb}.bif")
        t6 = process_time()

        pid = os.getpid()
        py = psutil.Process(pid)
        memoryUse = py.memory_info()[0]

        t2 = t2 - t1
        t4 = t4 - t3
        t6 = t6 - t5

        tab_ped[nb] = t2
        tab_bn[nb] = t4
        tab_inf[nb] = t6
        tab_mem[nb] = memoryUse
        memoryUse = None

    max_ped.append(tab_ped.max())
    max_bn.append(tab_bn.max())
    max_inf.append(tab_inf.max())
    max_mem.append(tab_mem.max())

    min_ped.append(tab_ped.min())
    min_bn.append(tab_bn.min())
    min_inf.append(tab_inf.min())
    min_mem.append(tab_mem.min())

    errorValues_ped.append(tab_ped.std())
    errorValues_bn.append(tab_bn.std())
    errorValues_inf.append(tab_inf.std())
    errorValues_mem.append(tab_mem.std())

    mean_gen_ped.append(tab_ped.mean())
    mean_gen_bn.append(tab_bn.mean())
    mean_gen_inf.append(tab_inf.mean())
    mean_mem.append(tab_mem.mean())


f1 = plt.figure(1)
plt.errorbar(nb_people, mean_gen_ped, yerr = errorValues_ped, ecolor='red')
plt.title('Temps d\'execution en fonction de la taille du pedigree')
plt.xlabel('Taille du pedigree')
plt.ylabel('Temps en sec')
plt.savefig('../cplex/figure/Temps d\'execution en fonction de la taille du pedigree avec ecart-type')
f1.show()

f2 = plt.figure(2)
plt.plot(nb_people, np.log(mean_gen_ped))
plt.title('Log du temps d\'execution en fonction de la taille du pedigree')
plt.xlabel('Taille du pedigree')
plt.ylabel('log du temps en sec')
plt.savefig('../cplex/figure/Log du temps d\'execution en fonction de la taille du pedigree')
f2.show()

f3 = plt.figure(3)
plt.plot(nb_people, mean_gen_ped, label='mean')
plt.plot(nb_people, max_ped, label='max')
plt.plot(nb_people, min_ped, label='min')
plt.legend(['mean','max','min'])
plt.title('Temps d\'execution en fonction de la taille du pedigree')
plt.xlabel('Taille du pedigree')
plt.ylabel('Temps en sec')
plt.savefig('../cplex/figure/Temps d\'execution moyen, min et max en fonction de la taille du pedigree')
f3.show()

f4 = plt.figure(4)
plt.errorbar(nb_people, mean_gen_bn, yerr = errorValues_bn, ecolor='red')
plt.title('Temps de génération du BN en fonction de la taille du pedigree')
plt.xlabel('Taille du pedigree')
plt.ylabel('Temps en sec')
plt.savefig('../cplex/figure/Temps de génération du BN en fonction de la taille du pedigree avec ecart-type')
f4.show()

f5 = plt.figure(5)
plt.plot(nb_people, mean_gen_bn, label='mean')
plt.plot(nb_people, max_bn, label='max')
plt.plot(nb_people, min_bn, label='min')
plt.legend(['mean','max','min'])
plt.title('Temps de génération du BN en fonction de la taille du pedigree')
plt.xlabel('Taille du pedigree')
plt.ylabel('Temps en sec')
plt.savefig('../cplex/figure/Temps de génération du BN moyen, min et max en fonction de la taille du pedigree')
f5.show()

f6 = plt.figure(6)
plt.errorbar(nb_people, mean_gen_inf, yerr = errorValues_inf, ecolor='red')
plt.title('Temps de calcul de l\'inférence en fonction de la taille du pedigree')
plt.xlabel('Taille du pedigree')
plt.ylabel('Temps en sec')
plt.savefig('../cplex/figure/Temps de calcul de l\'inférence en fonction de la taille du pedigree avec ecart-type')
f6.show()

f7 = plt.figure(7)
plt.plot(nb_people, mean_gen_inf, label='mean')
plt.plot(nb_people, max_inf, label='max')
plt.plot(nb_people, min_inf, label='min')
plt.legend(['mean','max','min'])
plt.title('Temps de calcul de l\'inférence en fonction de la taille du pedigree')
plt.xlabel('Taille du pedigree')
plt.ylabel('Temps en sec')
plt.savefig('../cplex/figure/Temps de calcul de l\'inférence moyenne, min et max en fonction de la taille du pedigree')
f7.show()

f8 = plt.figure(8)
plt.errorbar(nb_people, mean_mem, yerr = errorValues_mem, ecolor='red')
plt.title('Mémoire utilisée en fonction de la taille du pedigree')
plt.xlabel('Taille du pedigree')
plt.ylabel('Mémoire utilisée')
plt.savefig('../cplex/figure/Mémoire utilisée en fonction de la taille du pedigree avec ecart-type')
f8.show()

f9 = plt.figure(9)
plt.plot(nb_people, mean_mem, label='mean')
plt.plot(nb_people, max_mem, label='max')
plt.plot(nb_people, min_mem, label='min')
plt.legend(['mean','max','min'])
plt.title('Mémoire utilisée en fonction de la taille du pedigree')
plt.xlabel('Taille du pedigree')
plt.ylabel('Mémoire utilisée')
plt.savefig('../cplex/figure/Mémoire utilisée en moyenne, min et max en fonction de la taille du pedigree')
f9.show()


plt.show()
