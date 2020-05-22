import pyAgrum as gum
from matplotlib import ticker

from bped2.pedigree import *
import bped2.view as pview
import sandbox.doLazyProg as laz
from time import *
import numpy as np
import matplotlib.pyplot as plt
import os, psutil
import math

f = 0.05
nb_ped = 5
nb_people = [10,20,50,100,200,300,500,1000,1500,2000,2100,2200,2300,2400]
#nb_Gen_Max = [3,4,7,10,15,20,25,30,35,40,50,60,70,80]
nb_Gen_Max = [3,3,4,4,4,4,4,5,5,6,6,6,6,7]
nb_Gen_Min = [math.ceil(x/2) for x in nb_Gen_Max]
cl = 3

data = np.zeros((len(nb_people),6),dtype=float)
w = 0
for p,g_max,g_min in zip(nb_people,nb_Gen_Max,nb_Gen_Min):
    tab_clique = np.zeros(nb_ped)
    for nb in range(nb_ped):

        nbChild = random.randint(6,12)

        g = random.randint(g_min,g_max)
        ped = Pedigree()
        ped.gen_ped(nb, p, g, nbChild, cl, 0.03)
        bn = pview.ped_to_bn_compact(ped,f)
        pview.save(ped,f'../cplex/samples/compact/pedigree_{p}_{g}_{nbChild}_{cl}_G{nb}')
        pview.save_bn(bn,f'../cplex/bn/bn_compact_{p}_{g}_{nbChild}_{cl}_G{nb}')
        jte = gum.JunctionTreeGenerator()
        jt = jte.junctionTree(bn)
        for cl in jt.nodes():
            v = len(jt.clique(cl))
            if v < 3:
                data[w][0] += 100/(nb_ped*p)
            elif v < 6:
                data[w][1] += 100/(nb_ped*p)
            elif v < 10:
                data[w][2] += 100/(nb_ped*p)
            elif v < 20:
                data[w][3] += 100/(nb_ped*p)
            elif v < 30:
                data[w][4] =+ 100/(nb_ped*p)
            elif v < 40:
                data[w][5] =+ 100/(nb_ped*p)
            # elif v < 10 ** -1:
            #     data[w][4] += 100/(nb_ped*p)
            # elif v < 0.4:
            #     data[w][5] += 100 / (nb_ped * p)
            # elif v < 0.5:
            #     data[w][6] += 100 / (nb_ped * p)

    w+=1

# les tailles des graphes
#columns = ('1000', '1500', '2000', '2500', '5000')

columns = nb_people
# les seuils testés
#values=[80,50,20,10,5]
#values=[50,40,5,1,0.1]
values = [40,30,20,10,6,3]
# data = données à produire
# en supposant qu'il y a
# dans le cas N=1000 :
#   - 80% des X ont une erreur err<0.05,
#   - 20% des X ont une erreur 0.05<err<0.1,
# dans le cas N=5O00 :
#   -  8% <0.05
#   - 32% entre 0.05 et 0.1
#   - 36% entre 0.1 et 0.2
#   - 20% entre 0.2 et 0.5
#   -  4% >0.5
# data = np.array([[ 80, 20,  0,  0, 0],
#                  [ 60, 30, 10,  0, 0],
#                  [ 40, 32, 20,  8, 0],
#                  [ 25, 36, 24, 10, 5],
#                  [  8, 32, 36, 20, 4]])
data=data.transpose()
rows = ['<=%3.4f' % (x) for x in values]

colors = plt.cm.BuPu(np.linspace(0.2, 0.8, len(rows)))
n_rows = len(data)

index = np.arange(len(columns)) + 0.3
bar_width = 0.4

# Initialize the vertical-offset for the stacked bar chart.
y_offset = np.zeros(len(columns))

# Plot bars and create text labels for the table
cell_text = []
for row in range(n_rows):
    plt.bar(index, data[row], bar_width, bottom=y_offset, color=colors[row])
    y_offset = y_offset + data[row]
    cell_text.append(['%1.4f' % x if x!=0 else "" for x in data[row]])
# Reverse colors and text labels to display the last value at the top.
colors = colors[::-1]
cell_text.reverse()

# Add a table at the bottom of the axes
the_table = plt.table(cellText=cell_text,
                      rowLabels=rows,
                      rowColours=colors,
                      colLabels=columns,
                      loc='bottom')
# Adjust layout to make room for the table:
plt.subplots_adjust(left=0.2, bottom=0.2)

plt.ylabel("Proportion % (logarithmic)")
plt.ylim(50)
plt.yscale('log')
plt.gca().get_yaxis().set_minor_formatter(ticker.FormatStrFormatter('%.2f'))
plt.gca().get_yaxis().set_major_formatter(ticker.FormatStrFormatter('%.2f'))
plt.xticks([])
plt.title('Distribution des cliques (en %)');
plt.savefig('../cplex/figure/proportion_clique',bbox_inches='tight',dpi=300)
plt.show()

