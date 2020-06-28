import math
import random
import matplotlib.pyplot as plt
import numpy as np

nb_people = [10,20,50,100,200,300,500,1000,1500,2000]
#nb_people = [10,20,50,100,200,300,500,1000,1500,2000,2100,2200,2300,2400]
g = 2
gene_depart = 2
def file_to_data(file,g):
    res = dict()
    max_res = dict()
    min_res = dict()
    mean_res = dict()
    errorValues_res = dict()

    for i in range(gene_depart, g + 1):
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
        last_line = data[-1]
        for line in data:
            if line == '-\n' or line==last_line:
                if len(tab_2) != 0 :
                    array_2 = np.array(tab_2)
                    mean_res[2].append(array_2.mean())
                    max_res[2].append(array_2.max())
                    min_res[2].append(array_2.min())
                    errorValues_res[2].append(array_2.std())
                    tab_2 = []

                if len(tab_3) != 0 :
                    array_3 = np.array(tab_3)
                    mean_res[3].append(array_3.mean())
                    max_res[3].append(array_3.max())
                    min_res[3].append(array_3.min())
                    errorValues_res[3].append(array_3.std())
                    tab_3 = []

                if len(tab_4) != 0 :
                    array_4 = np.array(tab_4)
                    mean_res[4].append(array_4.mean())
                    max_res[4].append(array_4.max())
                    min_res[4].append(array_4.min())
                    errorValues_res[4].append(array_4.std())
                    tab_4 = []

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

#mean_res,max_res,min_res,errorValues_res = file_to_data('./data_bn', 4)
#mean_res,max_res,min_res,errorValues_res = file_to_data('/home/valentin/Documents/Stage/backup/multi/Nouveau dossier/data_bn', 4)
# f1 = plt.figure(1)
# legende = []
#
# for i in range(2,g+1):
#     c = (random.random(), random.random(), random.random())
#     ec = (random.random(),random.random(),random.random())
#     plt.errorbar(nb_people, mean_res[i], yerr = errorValues_res[i], ecolor=ec,color=c)
#     legende.append(f'{i}gène(s)')
# plt.legend(legende)
# plt.title('Temps de génération du BN en fonction de la taille du pedigree')
# plt.xlabel('Taille du pedigree')
# plt.ylabel('Temps en sec')
# plt.savefig('./Temps de génération du BN en fonction de la taille du pedigree avec ecart-type')
# #plt.savefig('/home/valentin/Documents/Stage/backup/multi/Nouveau dossier/Temps de génération du BN en fonction de la taille du pedigree avec ecart-type')
# f1.show()
#
# mean_res,max_res,min_res,errorValues_res = file_to_data('./data_inf', 4)
# #mean_res,max_res,min_res,errorValues_res = file_to_data('/home/valentin/Documents/Stage/backup/multi/Nouveau dossier/data_inf', 4)
# f2 = plt.figure(1)
# legende = []
# for i in range(2,g+1):
#     c = (random.random(), random.random(), random.random())
#     ec = (random.random(),random.random(),random.random())
#     plt.errorbar(nb_people, mean_res[i], yerr = errorValues_res[i], ecolor=ec,color=c)
#     legende.append(f'{i}gène(s)')
# plt.legend(legende)
# plt.title('Calcul d\'inférence multi-allélique en fonction du pedigree avec Lazy')
# plt.xlabel('Taille du pedigree')
# plt.ylabel('Temps en sec')
# plt.savefig('./Calcul d\'inférence multi-allélique avec Lazy')
# #plt.savefig('/home/valentin/Documents/Stage/backup/multi/Nouveau dossier/Calcul d\'inférence multi-allélique avec Lazy')
# f2.show()


mean_res,max_res,min_res,errorValues_res = file_to_data('./data_bn_2G_30', 4)
#mean_res,max_res,min_res,errorValues_res = file_to_data('/home/valentin/Documents/Stage/backup/multi/Nouveau dossier/data_bn', 4)
for i in range(gene_depart,g+1):
    plt.figure()
    plt.plot(nb_people, mean_res[i], label='mean')
    plt.plot(nb_people, max_res[i], label='max')
    plt.plot(nb_people, min_res[i], label='min')
    plt.legend(['mean', 'max', 'min'])
    plt.title(f'Temps de génération du BN en fonction du pedigree avec {i} gènes')
    plt.xlabel('Taille du pedigree')
    plt.ylabel('Temps en sec')
    plt.savefig(f'./Gen {i} Genes 30 samples')
    #plt.savefig(f'/home/valentin/Documents/Stage/backup/multi/Nouveau dossier/Temps de génération du BN multi-allélique en fonction du pedigree avec {i} gènes')
    plt.show()

mean_res,max_res,min_res,errorValues_res = file_to_data('./data_inf_2G_30', 4)
#mean_res,max_res,min_res,errorValues_res = file_to_data('/home/valentin/Documents/Stage/backup/multi/Nouveau dossier/data_inf', 4)
for i in range(gene_depart,g+1):
    plt.figure()
    plt.plot(nb_people, mean_res[i], label='mean')
    plt.plot(nb_people, max_res[i], label='max')
    plt.plot(nb_people, min_res[i], label='min')
    plt.legend(['mean', 'max', 'min'])
    plt.title(f'Calcul d\'inférence multi-allélique en fonction du pedigree avec {i} gènes')
    plt.xlabel('Taille du pedigree')
    plt.ylabel('Temps en sec')
    plt.savefig(f'./Inf {i} genes 30 samples')
    #plt.savefig(f'/home/valentin/Documents/Stage/backup/multi/Nouveau dossier/Calcul d\'inférence multi-allélique avec {i} gènes')
    plt.show()