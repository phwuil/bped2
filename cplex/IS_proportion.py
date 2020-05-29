from bped2.pedigree import *
from time import *
import bped2.view as pview
import sandbox.doLazyProg as laz
import sandbox.doIS as imp
import numpy as np
import matplotlib.pyplot as plt
import math
import matplotlib.ticker as ticker

f = 0.05
nb_ped = 10
nb_people = [10,20,50,100,200,300,500,1000,1500,2000,2100,2200,2300,2400]
#nb_Gen_Max = [3,4,7,10,15,20,25,30,35,40,50,60,70,80]
nb_Gen_Max = [3,3,4,4,4,4,4,5,5,6,6,6,6,6]
nb_Gen_Min = [math.ceil(x/2) for x in nb_Gen_Max]
cl = 3

data = np.zeros((len(nb_people),7),dtype=float)

mean_gen_is = []
errorValues_is = []
max_is = []
min_is = []

mean_gen_diff = []
errorValues_diff = []
max_diff = []
min_diff = []
w = 0

sen = Pedigree()
sen.load('../data/ped/senegal2013.ped')
len_sen = len(sen)
bn_sen = pview.ped_to_bn_compact(sen,f)
ie = pview.gum.ImportanceSampling(bn_sen)
ie.setMaxTime(200)
ie.setEpsilon(5e-4)
t1 = process_time()
ie.makeInference()
t2 = process_time()
time_sen_compact = t2 - t1

for p,g_max,g_min in zip(nb_people,nb_Gen_Max,nb_Gen_Min):
    tab_lis = np.zeros(nb_ped)
    tab_diff = np.zeros(nb_ped)
    for nb in range(nb_ped):
        nbChild = random.randint(6,12)
        g = random.randint(g_min,g_max)
        ped = Pedigree()
        ped.gen_ped(nb, p, g, nbChild, cl, 0.03)
        bn_compact = pview.ped_to_bn_compact(ped, f)
        pview.save(ped, f'../cplex/samples/IS/pedigree_{p}_{g}_{nbChild}_{cl}_G{nb}')
        pview.save_bn(bn_compact, f'../cplex/bn/IS/bn_compact_{p}_{g}_{nbChild}_{cl}_G{nb}')

        t1 = process_time()
        ie1 = imp.lisPosterior(f'../cplex/bn/IS/bn_compact_{p}_{g}_{nbChild}_{cl}_G{nb}.bif')
        t2 = process_time()
        t2 = t2 - t1
        tab_lis[nb] = t2
        ie2 = laz.lazyPosterior(f'../cplex/bn/IS/bn_compact_{p}_{g}_{nbChild}_{cl}_G{nb}.bif')

        error_lbp_laz = []
        for i in ped.get_pedigree().keys():
            p1 = ie1.posterior(f'X{i}')
            p2 = ie2.posterior(f'X{i}')
            x = [abs(p1[0] - p2[0]),abs(p1[1] - p2[1]),abs(p1[2] - p2[2]),abs(p1[3] - p2[3])]
            v = max(x)
            if v < 10**-5:
                data[w][0] += 100/(nb_ped*p)
            elif v < 10**-4:
                data[w][1] += 100/(nb_ped*p)
            elif v < 10**-3:
                data[w][2] += 100/(nb_ped*p)
            elif v < 10**-2:
                data[w][3] += 100/(nb_ped*p)
            # else:
            elif v < 10 ** -1:
                data[w][4] += 100/(nb_ped*p)
            elif v < 0.3:
                data[w][5] += 100 / (nb_ped * p)
            elif v < 0.5:
                data[w][6] += 100 / (nb_ped * p)
            #error_lbp_laz.append(max(x))

        #error_lbp_laz = np.array(error_lbp_laz)
        # tab_diff[nb] = error_lbp_laz.max()
        #v = error_lbp_laz.max()

    max_is.append(tab_lis.max())
    min_is.append(tab_lis.min())
    errorValues_is.append(tab_lis.std())
    mean_gen_is.append(tab_lis.mean())
    # max_diff.append(tab_diff.max())
    # min_diff.append(tab_diff.min())
    # errorValues_diff.append(tab_diff.std())
    # mean_gen_diff.append(tab_diff.mean())

    w+=1

# les tailles des graphes
#columns = ('1000', '1500', '2000', '2500', '5000')

columns = nb_people
# les seuils testés
#values=[80,50,20,10,5]
#values=[50,40,5,1,0.1]
values = [50,30,10,1,10**-1,10**-2,10**-3]
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
plt.ylim(70)
plt.yscale('log')
plt.gca().get_yaxis().set_minor_formatter(ticker.FormatStrFormatter('%.2f'))
plt.gca().get_yaxis().set_major_formatter(ticker.FormatStrFormatter('%.2f'))
plt.xticks([])
plt.title('Distribution des erreurs (en %)');
plt.savefig('../cplex/figure/IS/proportion_20s_5e-4',bbox_inches='tight',dpi=300)
plt.show()

f2 = plt.figure(2)
plt.errorbar(nb_people, mean_gen_is, yerr = errorValues_is, ecolor='red')
plt.plot(len_sen,time_sen_compact,'xr')
plt.title('Temps de calcul de l\'inférence d\'un BNC avec IS')
plt.xlabel('Taille du pedigree')
plt.ylabel('Temps en sec')
plt.savefig('../cplex/figure/IS/Temps de calcul de l\'inférence d\'un BNC en fonction du pedigree avec ecart-type',bbox_inches='tight')
f2.show()


f3 = plt.figure(3)
plt.plot(nb_people, mean_gen_is, label='mean')
plt.plot(nb_people, max_is, label='max')
plt.plot(nb_people, min_is, label='min')
plt.plot(len_sen,time_sen_compact,'xr')
plt.legend(['mean','max','min','sen'])
plt.title('Temps de calcul de l\'inférence d\'un BNC avec IS')
plt.xlabel('Taille du pedigree')
plt.ylabel('Temps en sec')
plt.savefig('../cplex/figure/IS/Temps de calcul de l\'inférence moyenne d\'un BNC, min et max en fonction du pedigree',bbox_inches='tight')
f3.show()
