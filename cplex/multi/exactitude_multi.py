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
nb_ped = 30
nb_people = [10,20,50,100,200,300,500,1000,1500,2000,2100,2200,2300,2400]
nb_Gen_Max = [3,3,4,4,4,4,4,5,5,6,6,6,6,7]
# nb_people = [10,20]
# nb_Gen_Max = [3,3]
data = np.zeros((len(nb_people),7),dtype=float)

nb_Gen_Min = [math.ceil(x/2) for x in nb_Gen_Max]
cl = 3
gene_depart = 5
gene = 5
distance = [0.8,0.7,0.5]
centimorgans = [0.295797287184, 0.296353882133, 0.299343592142, 0.59]
w = 0

#{'X1_1':[1,0,0,0],'X5_1':[1,1,1,0],'X8_1':[1,1,1,0],'X1_2':[0,1,1,0],'X6_2':[0,0,0,1],'X2_3':[1,1,1,0],'X3_3':[0,1,1,0],'X7_3':[1,0,0,0],'X4_4':[0,1,1,1],'X5_4':[0,1,0,0]}
#evidence = {'X1_1':[1,0,0,0],'X5_1':[1,1,1,0],'X8_1':[1,1,1,0],'X2_2':[0,1,1,0],'X6_2':[0,0,0,1],'X3_3':[1,1,1,0],'X7_3':[0,1,1,0]}
evidence = {'X1_1':[1,0,0,0],'X5_1':[1,1,1,0],'X8_1':[1,1,1,0],'X3_3':[1,1,1,0],'X7_3':[0,1,1,0],'X1_4':[1,1,1,0],'X2_4':[0,1,1,0],'X6_5':[0,1,1,1],'X9_5':[1,1,1,0]}
#evidence = None
file = open('../data/multi/lbp/last_test3', 'w')
#file = open('../data/multi/lbp/test', 'w')


for p,g_max,g_min in zip(nb_people,nb_Gen_Max,nb_Gen_Min):

    for nb in range(nb_ped):

        nbChild = random.randint(6,12)

        g = random.randint(g_min,g_max)
        ped = Pedigree()
        ped.gen_ped(nb, p, g, nbChild, cl, 0.03)

        for i in range(gene_depart,gene+1):

            #bn = pview.bn_multi_pb(ped, f, i, distance[:i-1])
            bn = pview.bn_multi_morgans(ped, f, i, centimorgans[:i])
            pview.save(ped,f'./samples/pedigree_{p}_{g}_{nbChild}_{cl}_G{nb}')
            pview.save_bn(bn,f'./bn/bn_{p}_{g}_{nbChild}_{cl}_G{nb}')


            ie1 = laz.lazyPosterior(f"./bn/bn_{p}_{g}_{nbChild}_{cl}_G{nb}.bif",evidence)
            ie2 = lbp.lbpPosterior(f"./bn/bn_{p}_{g}_{nbChild}_{cl}_G{nb}.bif",evidence)

            for j in ped.get_pedigree().keys():
                for g in range(1, 3):
                #for g in range(1,gene+1):
                    p1 = ie1.posterior(f'X{j}_{g}')
                    p2 = ie2.posterior(f'X{j}_{g}')
                    x = [abs(p1[0] - p2[0]), abs(p1[1] - p2[1]), abs(p1[2] - p2[2]), abs(p1[3] - p2[3])]
                    v = max(x)
                    file.write(f'{v}\t{100 / (nb_ped * p * gene)}\n')
                    file.flush()
                    if v < 10 ** -5:
                        data[w][0] += 100 / (nb_ped * p * gene)
                    elif v < 10 ** -4:
                        data[w][1] += 100 / (nb_ped * p * gene)
                    elif v < 10 ** -3:
                        data[w][2] += 100 / (nb_ped * p * gene)
                    elif v < 10 ** -2:
                        data[w][3] += 100 / (nb_ped * p * gene)
                    elif v < 10 ** -1:
                        data[w][4] += 100 / (nb_ped * p * gene)
                    elif v < 0.4:
                        data[w][5] += 100 / (nb_ped * p * gene)
                    elif v < 0.5:
                        data[w][6] += 100 / (nb_ped * p * gene)

    w+=1
    file.write(f'changement\n')
    file.flush()
file.close()

#
# # les tailles des graphes
# #columns = ('1000', '1500', '2000', '2500', '5000')
#
# columns = nb_people
# # les seuils testés
# #values=[80,50,20,10,5]
# #values=[50,40,5,1,0.1]
# values = [50,40,10,1,10**-1,10**-2,10**-3]
# # data = données à produire
# # en supposant qu'il y a
# # dans le cas N=1000 :
# #   - 80% des X ont une erreur err<0.05,
# #   - 20% des X ont une erreur 0.05<err<0.1,
# # dans le cas N=5O00 :
# #   -  8% <0.05
# #   - 32% entre 0.05 et 0.1
# #   - 36% entre 0.1 et 0.2
# #   - 20% entre 0.2 et 0.5
# #   -  4% >0.5
# # data = np.array([[ 80, 20,  0,  0, 0],
# #                  [ 60, 30, 10,  0, 0],
# #                  [ 40, 32, 20,  8, 0],
# #                  [ 25, 36, 24, 10, 5],
# #                  [  8, 32, 36, 20, 4]])
# data=data.transpose()
# rows = ['<=%3.4f' % (x/100) for x in values]
#
# colors = plt.cm.BuPu(np.linspace(0.2, 0.8, len(rows)))
# n_rows = len(data)
#
# index = np.arange(len(columns)) + 0.3
# bar_width = 0.4
#
# # Initialize the vertical-offset for the stacked bar chart.
# y_offset = np.zeros(len(columns))
#
# # Plot bars and create text labels for the table
# cell_text = []
# for row in range(n_rows):
#     plt.bar(index, data[row], bar_width, bottom=y_offset, color=colors[row])
#     y_offset = y_offset + data[row]
#     cell_text.append(['%1.4f' % x if x!=0 else "" for x in data[row]])
# # Reverse colors and text labels to display the last value at the top.
# colors = colors[::-1]
# cell_text.reverse()
#
# # Add a table at the bottom of the axes
# the_table = plt.table(cellText=cell_text,
#                       rowLabels=rows,
#                       rowColours=colors,
#                       colLabels=columns,
#                       loc='bottom')
# # Adjust layout to make room for the table:
# plt.subplots_adjust(left=0.2, bottom=0.2)
#
# plt.ylabel("Proportion % (logarithmic)")
# plt.ylim(80)
# plt.yscale('log')
# plt.gca().get_yaxis().set_minor_formatter(ticker.FormatStrFormatter('%.2f'))
# plt.gca().get_yaxis().set_major_formatter(ticker.FormatStrFormatter('%.2f'))
# plt.xticks([])
# plt.title('Distribution des erreurs (en %)');
# plt.savefig('./figure/proportion',bbox_inches='tight')
# plt.show()


