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

mean_gen_ped = []
mean_gen_bn = []
mean_gen_inf = []
mean_gen_bn_compact = []
mean_gen_inf_compact = []
mean_clique = []
mean_csg = []

errorValues_ped = []
errorValues_bn = []
errorValues_inf = []
errorValues_bn_compact = []
errorValues_inf_compact = []
errorValues_clique = []
errorValues_csg = []

max_ped = []
max_bn = []
max_inf = []
max_bn_compact = []
max_inf_compact = []
max_clique = []
max_csg = []

min_ped = []
min_bn = []
min_inf = []
min_bn_compact = []
min_inf_compact = []
min_clique = []
min_csg = []

file = open('./data/data_lazy_no_compact','w')
sen = Pedigree()
sen.load('../data/ped/senegal2013.ped')
len_sen = len(sen)

bn_sen = pview.ped_to_bn_compact(sen,f)
ie = pview.gum.LazyPropagation(bn_sen)
t1 = process_time()
ie.makeInference()
t2 = process_time()
time_sen_compact = t2 - t1

bn_sen = pview.ped_to_bn(sen,f)
ie = pview.gum.LazyPropagation(bn_sen)
t1 = process_time()
ie.makeInference()
t2 = process_time()
time_sen_no_compact = t2 - t1

for p,g_max,g_min in zip(nb_people,nb_Gen_Max,nb_Gen_Min):
    tab_ped = np.zeros(nb_ped)
    tab_bn = np.zeros(nb_ped)
    tab_inf = np.zeros(nb_ped)
    tab_mem = np.zeros(nb_ped)
    tab_bn_compact = np.zeros(nb_ped)
    tab_inf_compact = np.zeros(nb_ped)
    tab_clique = np.zeros(nb_ped)
    tab_csg = np.zeros(nb_ped)

    for nb in range(nb_ped):

        nbChild = random.randint(6,12)

        g = random.randint(g_min,g_max)
        ped = Pedigree()
        t1 = process_time()
        ped.gen_ped(nb, p, g, nbChild, cl, 0.03)
        t2 = process_time()

        t3 = process_time()
        bn = pview.ped_to_bn(ped,f)
        t4 = process_time()

        t7 = process_time()
        #bn_compact = pview.ped_to_bn_compact(ped,f)
        t8 = process_time()

        pview.save(ped,f'../cplex/samples/compact/pedigree_{p}_{g}_{nbChild}_{cl}_G{nb}')
        pview.save_bn(bn,f'../cplex/bn/no_compact/bn_{p}_{g}_{nbChild}_{cl}_G{nb}')
        #pview.save_bn(bn_compact,f'../cplex/bn/bn_compact_{p}_{g}_{nbChild}_{cl}_G{nb}')

        t5 = process_time()
        laz.doLazyProg(f"../cplex/bn/no_compact/bn_{p}_{g}_{nbChild}_{cl}_G{nb}.bif")
        t6 = process_time()

        t9 = process_time()
        #laz.doLazyProg(f'../cplex/bn/bn_compact_{p}_{g}_{nbChild}_{cl}_G{nb}.bif')
        t10 = process_time()

        t2 = t2 - t1
        t4 = t4 - t3
        t6 = t6 - t5
        t8 = t8 - t7
        t10 = t10 - t9

        file.write(f'{nb}\t{t6}\n')

        tab_ped[nb] = t2
        tab_bn[nb] = t4
        tab_inf[nb] = t6
        tab_bn_compact[nb] = t8
        tab_inf_compact[nb] = t10
        #tab_clique[nb] = pview.max_clique_size(bn_compact)
        tab_csg[nb] = len(ped.all_consanguineous_ped(g))/p

    file.write('-\n')
    max_ped.append(tab_ped.max())
    max_bn.append(tab_bn.max())
    max_inf.append(tab_inf.max())
    max_bn_compact.append(tab_bn_compact.max())
    max_inf_compact.append(tab_inf_compact.max())
    max_clique.append(tab_clique.max())
    max_csg.append(tab_csg.max())

    min_ped.append(tab_ped.min())
    min_bn.append(tab_bn.min())
    min_inf.append(tab_inf.min())
    min_bn_compact.append(tab_bn_compact.min())
    min_inf_compact.append(tab_inf_compact.min())
    min_clique.append(tab_clique.min())
    min_csg.append(tab_csg.min())

    errorValues_ped.append(tab_ped.std())
    errorValues_bn.append(tab_bn.std())
    errorValues_inf.append(tab_inf.std())
    errorValues_bn_compact.append(tab_bn_compact.std())
    errorValues_inf_compact.append(tab_inf_compact.std())
    errorValues_clique.append(tab_clique.std())
    errorValues_csg.append(tab_csg.std())

    mean_gen_ped.append(tab_ped.mean())
    mean_gen_bn.append(tab_bn.mean())
    mean_gen_inf.append(tab_inf.mean())
    mean_gen_bn_compact.append(tab_bn_compact.mean())
    mean_gen_inf_compact.append(tab_inf_compact.mean())
    mean_clique.append(tab_clique.mean())
    mean_csg.append(tab_csg.mean())

file.close()
# f1 = plt.figure(1)
# plt.errorbar(nb_people, mean_gen_ped, yerr = errorValues_ped, ecolor='red')
# plt.title('Temps d\'execution en fonction de la taille du pedigree')
# plt.xlabel('Taille du pedigree')
# plt.ylabel('Temps en sec')
# plt.savefig('../cplex/figure/Temps d\'execution en fonction de la taille du pedigree avec ecart-type')
# f1.show()
#
# f2 = plt.figure(2)
# plt.plot(nb_people, np.log(mean_gen_ped))
# plt.title('Log du temps d\'execution en fonction de la taille du pedigree')
# plt.xlabel('Taille du pedigree')
# plt.ylabel('log du temps en sec')
# plt.savefig('../cplex/figure/Log du temps d\'execution en fonction de la taille du pedigree')
# f2.show()
#
# f3 = plt.figure(3)
# plt.plot(nb_people, mean_gen_ped, label='mean')
# plt.plot(nb_people, max_ped, label='max')
# plt.plot(nb_people, min_ped, label='min')
# plt.legend(['mean','max','min'])
# plt.title('Temps d\'execution en fonction de la taille du pedigree')
# plt.xlabel('Taille du pedigree')
# plt.ylabel('Temps en sec')
# plt.savefig('../cplex/figure/Temps d\'execution moyen, min et max en fonction de la taille du pedigree')
# f3.show()
#
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
plt.plot(len_sen,time_sen_no_compact,'xr')
plt.title('Temps de calcul de l\'inférence en fonction de la taille du pedigree')
plt.xlabel('Taille du pedigree')
plt.ylabel('Temps en sec')
plt.savefig('../cplex/figure/Temps de calcul de l\'inférence en fonction de la taille du pedigree avec ecart-type')
f6.show()

f7 = plt.figure(7)
plt.plot(nb_people, mean_gen_inf, label='mean')
plt.plot(nb_people, max_inf, label='max')
plt.plot(nb_people, min_inf, label='min')
plt.plot(len_sen,time_sen_no_compact,'xr')
plt.legend(['mean','max','min'])
plt.title('Temps de calcul de l\'inférence en fonction de la taille du pedigree')
plt.xlabel('Taille du pedigree')
plt.ylabel('Temps en sec')
plt.savefig('../cplex/figure/Temps de calcul de l\'inférence moyenne, min et max en fonction de la taille du pedigree')
f7.show()


# f8 = plt.figure(8)
# plt.errorbar(nb_people, mean_gen_bn_compact, yerr = errorValues_bn_compact, ecolor='red')
# plt.plot(len_sen,time_sen_compact,'xr')
# plt.title('Temps de génération d\'un BN compact en fonction de la taille du pedigree')
# plt.xlabel('Taille du pedigree')
# plt.ylabel('Temps en sec')
# plt.savefig('../cplex/figure/Temps de génération d\'un BN compact en fonction de la taille du pedigree avec ecart-type')
# f8.show()
#
# f9 = plt.figure(9)
# plt.plot(nb_people, mean_gen_bn_compact, label='mean')
# plt.plot(nb_people, max_bn_compact, label='max')
# plt.plot(nb_people, min_bn_compact, label='min')
# plt.plot(len_sen,time_sen_compact,'xr')
# plt.legend(['mean','max','min'])
# plt.title('Temps de génération d\'un BN compact en fonction de la taille du pedigree')
# plt.xlabel('Taille du pedigree')
# plt.ylabel('Temps en sec')
# plt.savefig('../cplex/figure/Temps de génération d\'un BN compact moyen, min et max en fonction de la taille du pedigree')
# f9.show()
#
# f10 = plt.figure(10)
# plt.errorbar(nb_people, mean_gen_inf_compact, yerr = errorValues_inf_compact, ecolor='red')
# plt.plot(len_sen,time_sen_compact,'xr')
# plt.title('Temps de calcul de l\'inférence d\'un BNC en fonction du pedigree')
# plt.xlabel('Taille du pedigree')
# plt.ylabel('Temps en sec')
# plt.savefig('../cplex/figure/Temps de calcul de l\'inférence d\'un BN compact en fonction de la taille du pedigree avec ecart-type')
# f10.show()
#
# f11 = plt.figure(11)
# plt.plot(nb_people, mean_gen_inf_compact, label='mean')
# plt.plot(nb_people, max_inf_compact, label='max')
# plt.plot(nb_people, min_inf_compact, label='min')
# plt.plot(len_sen,time_sen_compact,'xr')
# plt.legend(['mean','max','min','sen'])
# plt.title('Temps de calcul de l\'inférence avec un BNC')
# plt.xlabel('Taille du pedigree')
# plt.ylabel('Temps en sec')
# plt.savefig('../cplex/figure/Temps de calcul de l\'inférence moyenne d\'un BN compact , min et max en fonction de la taille du pedigree')
# f11.show()

# f12 = plt.figure(12)
# plt.plot(nb_people, mean_clique, label='mean')
# plt.plot(nb_people, max_clique, label='max')
# plt.plot(nb_people, min_clique, label='min')
# plt.legend(['mean','max','min'])
# plt.title('Taille de la clique en fonction de la taille du pedigree')
# plt.xlabel('Taille du pedigree')
# plt.ylabel('Taille de la clique')
# plt.savefig('../cplex/figure/Taille de la clique moyenne, min et max en fonction de la taille du pedigree pour bn compact')
# f12.show()
#
# f13 = plt.figure(13)
# plt.plot(nb_people, mean_csg, label='mean')
# plt.plot(nb_people, max_csg, label='max')
# plt.plot(nb_people, min_csg, label='min')
# plt.legend(['mean','max','min'])
# plt.title('Nombre de consanguins en fonction du pedigree')
# plt.xlabel('Taille du pedigree')
# plt.ylabel('Nombre de consanguins')
# plt.savefig('../cplex/figure/Proportion de consanguins moyen, min et max en fonction de la taille du pedigree pour bn compact')
#f13.show()

plt.show()
