import math
import random
import matplotlib.pyplot as plt
import numpy as np

nb_people = [10,20,50,100,200,300,500]
g = 4
def file_to_data(file,g):
    res = dict()
    max_res = dict()
    min_res = dict()
    mean_res = dict()
    errorValues_res = dict()

    for i in range(2, g + 1):
        res[i] = []
        max_res[i] = []
        min_res[i] = []
        mean_res[i] = []
        errorValues_res[i] = []

    with open(file) as f:
        data = f.readlines()
        tab_2 = []
        tab_3 = []
        tab_4 = []
        for line in data:
            if line == '-\n':
                array_2 = np.array(tab_2)
                array_3 = np.array(tab_3)
                array_4 = np.array(tab_4)

                mean_res[2].append(array_2.mean())
                mean_res[3].append(array_3.mean())
                mean_res[4].append(array_4.mean())

                max_res[2].append(array_2.max())
                max_res[3].append(array_3.max())
                max_res[4].append(array_4.max())

                min_res[2].append(array_2.min())
                min_res[3].append(array_3.min())
                min_res[4].append(array_4.min())

                errorValues_res[2].append(array_2.std())
                errorValues_res[3].append(array_3.std())
                errorValues_res[4].append(array_4.std())

                tab_2 = []
                tab_3 = []
                tab_4 = []

                print('ok je reconnais')
            else:
                occ,time,gene = line.split('\t')
                print(gene)
                gene = int(gene)
                if gene == 2:
                    print('uho')
                    tab_2.append(float(time))
                if gene == 3:
                    tab_3.append(float(time))
                if gene == 4:
                    tab_4.append(float(time))

    return mean_res,max_res,min_res,errorValues_res

mean_res,max_res,min_res,errorValues_res = file_to_data('./data_bn', 4)
f1 = plt.figure(1)
legende = []

for i in range(2,g+1):
    c = (random.random(), random.random(), random.random())
    ec = (random.random(),random.random(),random.random())
    plt.errorbar(nb_people, mean_res[i], yerr = errorValues_res[i], ecolor=ec,color=c)
    legende.append(f'{i}gène(s)')
plt.legend(legende)
plt.title('Temps de génération du BN en fonction de la taille du pedigree')
plt.xlabel('Taille du pedigree')
plt.ylabel('Temps en sec')
plt.savefig('./Temps de génération du BN en fonction de la taille du pedigree avec ecart-type')
f1.show()

mean_res,max_res,min_res,errorValues_res = file_to_data('./data_inf', 4)
f2 = plt.figure(1)
legende = []
for i in range(2,g+1):
    c = (random.random(), random.random(), random.random())
    ec = (random.random(),random.random(),random.random())
    plt.errorbar(nb_people, mean_res[i], yerr = errorValues_res[i], ecolor=ec,color=c)
    legende.append(f'{i}gène(s)')
plt.legend(legende)
plt.title('Calcul d\'inférence multi-allélique en fonction du pedigree avec LBP')
plt.xlabel('Taille du pedigree')
plt.ylabel('Temps en sec')
plt.savefig('./Calcul d\'inférence multi-allélique avec LBP')
f2.show()
