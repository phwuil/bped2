from bped2.pedigree import *
import bped2.view as pview
import sandbox.doLazyProg as laz
from time import *
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mat
mat.use('Agg')
import math

f = 0.05
nb_ped = 30
nb_people = [10,20,50,100,200,300,500,1000,1500,2000,2100,2200,2300,2400]
nb_Gen_Max = [3,3,4,4,4,4,4,5,5,6,6,6,6,7]
# nb_people = [10,20,50]
# nb_Gen_Max = [3,3,3]

nb_Gen_Min = [math.ceil(x/2) for x in nb_Gen_Max]
cl = 3
gene = 4
distance = [0.8,0.7,0.5]
centimorgans = [0.295797287184, 0.296353882133, 0.299343592142, 0.59]

file_bn = open('../data/multi/data_bn', 'w')
file_inf = open('../data/multi/data_inf', 'w')
sen = Pedigree()
sen.load('../../data/ped/senegal2013.ped')
len_sen = len(sen)
time_sen = []

res_bn = dict()
res_inf = dict()
res_clique = dict()

max_bn = dict()
min_bn = dict()
mean_bn = dict()
errorValues_bn = dict()

max_inf = dict()
min_inf = dict()
mean_inf = dict()
errorValues_inf = dict()

max_clique = dict()
min_clique = dict()
mean_clique = dict()
errorValues_clique = dict()

for i in range(2,gene+1):

    max_clique[i] = []
    max_inf[i] = []
    max_bn[i] = []

    min_clique[i] = []
    min_inf[i] = []
    min_bn[i] = []

    mean_clique[i] = []
    mean_bn[i] = []
    mean_inf[i] = []

    errorValues_clique[i] = []
    errorValues_inf[i] = []
    errorValues_bn[i] = []

    # bn_sen = pview.ped_to_bn_multi(sen, f, i, distance[:i-1])
    # ie = pview.gum.LazyPropagation(bn_sen)
    # t1 = process_time()
    # ie.makeInference()
    # t2 = process_time()
    # time_sen.append(t2 - t1)
    time_sen.append(0)

for p,g_max,g_min in zip(nb_people,nb_Gen_Max,nb_Gen_Min):
    for i in range(2, gene + 1):
        res_bn[i] = np.zeros(nb_ped)
        res_inf[i] = np.zeros(nb_ped)
        res_clique[i] = np.zeros(nb_ped)

    for nb in range(nb_ped):

        nbChild = random.randint(6,12)

        g = random.randint(g_min,g_max)
        ped = Pedigree()
        ped.gen_ped(nb, p, g, nbChild, cl, 0.03)

        for i in range(2,gene+1):

            t3 = process_time()
            #bn = pview.bn_multi_pb(ped, f, i, distance[:i-1])
            bn = pview.bn_multi_morgans(ped, f, i, centimorgans[:i])
            t4 = process_time()

            pview.save(ped,f'./samples/pedigree_{p}_{g}_{nbChild}_{cl}_G{nb}')
            pview.save_bn(bn,f'./bn/bn_{p}_{g}_{nbChild}_{cl}_G{nb}')

            t5 = process_time()
            laz.doLazyProg(f"./bn/bn_{p}_{g}_{nbChild}_{cl}_G{nb}.bif")
            t6 = process_time()

            t4 = t4 - t3
            res_bn[i][nb] = t4
            t6 = t6 - t5
            res_inf[i][nb] = t6
            res_clique[i][nb] = pview.max_clique_size(bn)

            file_bn.write(f'{nb}\t{t4}\t{i}\n')
            file_inf.write(f'{nb}\t{t6}\t{i}\n')

    file_bn.write('-\n')
    file_inf.write('-\n')

    for i in range(2,gene+1):
        max_bn[i].append(res_bn[i].max)
        max_inf[i].append(res_inf[i].max())
        max_clique[i].append(res_clique[i].max())

        min_bn[i].append(res_bn[i].min())
        min_inf[i].append(res_inf[i].min())
        min_clique[i].append(res_clique[i].min())

        errorValues_bn[i].append(res_bn[i].std())
        errorValues_inf[i].append(res_inf[i].std())
        errorValues_clique[i].append(res_clique[i].std())

        mean_bn[i].append(res_bn[i].mean())
        mean_inf[i].append(res_inf[i].mean())
        mean_clique[i].append(res_clique[i].mean())

file_bn.close()
file_inf.close()

f1 = plt.figure(1)
legende = []

for i in range(2,gene+1):
    c = (random.random(), random.random(), random.random())
    ec = (random.random(),random.random(),random.random())
    plt.errorbar(nb_people, mean_bn[i], yerr = errorValues_bn[i], ecolor=ec,color=c)
    legende.append(f'{i}gène(s)')
plt.legend(legende)
plt.title('Temps de génération du BN en fonction de la taille du pedigree')
plt.xlabel('Taille du pedigree')
plt.ylabel('Temps en sec')
plt.savefig('./figure/Temps de génération du BN en fonction de la taille du pedigree avec ecart-type')
#f1.show()

f2 = plt.figure(1)
legende = []
for i in range(2,gene+1):
    c = (random.random(), random.random(), random.random())
    ec = (random.random(),random.random(),random.random())
    plt.errorbar(nb_people, mean_inf[i], yerr = errorValues_inf[i], ecolor=ec,color=c)
    legende.append(f'{i}gène(s)')
plt.legend(legende)
plt.title('Calcul d\'inférence multi-allélique en fonction du pedigree avec LBP')
plt.xlabel('Taille du pedigree')
plt.ylabel('Temps en sec')
plt.savefig('./figure/Calcul d\'inférence multi-allélique avec LBP')
#f2.show()
