from matplotlib import ticker

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


nb_people = [10,20,50,100,200,300,500,1000,1500,2000,2100,2200,2300,2400]
data = np.zeros((len(nb_people),7),dtype=float)
gene = 2

def data_to_plot(file):
    with open(file) as f:
        tab = f.readlines()
        w = 0
        for line in tab:
            if data[w].sum() >= 99.9999999999:
                print('oui')
                w+=1
                if w == len(nb_people):
                    return data

            v,x = line.split()
            v = float(v)
            x = float(x)
            if v < 10**-5:
                data[w][0] += x
            elif v < 10**-4:
                data[w][1] += x
            elif v < 10**-3:
                data[w][2] += x
            elif v < 10**-2:
                data[w][3] += x
            # else:
            elif v < 10 ** -1:
                data[w][4] += x
            elif v < 0.4:
                data[w][5] += x
            elif v < 0.5:
                data[w][6] += x


    return data



data = data_to_plot('./data/multi/lbp/proportion_2G_obs')

columns = nb_people
# les seuils testés
#values=[80,50,20,10,5]
#values=[50,40,5,1,0.1]
values = [50,40,10,1,10**-1,10**-2,10**-3]
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
rows = ['<=%3.4f' % (x/100) for x in values]

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
plt.ylim(80)
plt.yscale('log')
plt.gca().get_yaxis().set_minor_formatter(ticker.FormatStrFormatter('%.2f'))
plt.gca().get_yaxis().set_major_formatter(ticker.FormatStrFormatter('%.2f'))
plt.xticks([])
plt.title('Distribution des erreurs (en %)');
#plt.savefig('../cplex/figure/LBP/proportion',bbox_inches='tight')
plt.savefig('../cplex/multi/figure/proportion_2G_obs',bbox_inches='tight',dpi=300)
plt.show()
