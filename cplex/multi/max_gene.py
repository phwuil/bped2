from matplotlib import ticker

from bped2.pedigree import *
import bped2.view as pview
import sandbox.doLazyProg as laz
import sandbox.doLBP as lbp
from time import *
import numpy as np
#import matplotlib.pyplot as plt
# import matplotlib as mat
# mat.use('Agg')
import math

f = 0.05
nb_ped = 1
#nb_people = [10,50,100,200,300,500,1000,1500,2000,2400]
#nb_Gen_Max = [3,4,4,4,4,4,5,5,6,7]
nb_people = [2400]
nb_Gen_Max = [7]
data = np.zeros((len(nb_people),7),dtype=float)

nb_Gen_Min = [math.ceil(x/2) for x in nb_Gen_Max]
cl = 3
gene_depart = 4
gene = 4

centimorgans = [0.295797287184]


file = open('../data/multi/lbp/jpp', 'a+')
file.write(f'{nb_people[0]}\n')
for p,g_max,g_min in zip(nb_people,nb_Gen_Max,nb_Gen_Min):
    i=5
    for nb in range(nb_ped):

        nbChild = random.randint(6,12)

        g = random.randint(g_min,g_max)
        ped = Pedigree()
        ped.gen_ped(nb, p, g, nbChild, cl, 0.03)

        while True:

            bn = pview.bn_multi_morgans(ped, f, i, centimorgans*i)
            pview.save(ped,f'./samples/pedigree_{p}_{g}_{nbChild}_{cl}_G{nb}')
            pview.save_bn(bn,f'./bn/bn_{p}_{g}_{nbChild}_{cl}_G{nb}')

            t1 = process_time()
            lbp.doLBP(f"./bn/bn_{p}_{g}_{nbChild}_{cl}_G{nb}.bif")
            t2 = process_time()
            t2 = t2 - t1
            print(t2) 
            file.write(f'{i}\t{t2}\n')
            file.flush()
            i+=1
            if t2 > 600:
            	exit()
file.close()
