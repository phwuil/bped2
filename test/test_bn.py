import unittest
import os
import sys
import psutil
from bped2.pedigree import *
import bped2.view as pview
import sandbox.doLazyProg as lazy

class TestPedigree(unittest.TestCase):

    def test_gen_bn(self):
        ped = Pedigree()
        ped.load("../cplex/samples/pedigree_1000_50_4_4_G49.ped")
        bn = pview.ped_to_bn(ped,0.05)
        #pview.save_bn(bn,'toto')
        print(lazy.doLazyProg("../cplex/bn/bn_2500_44_4_4_G2.bif"))

    def test_bn_compact(self):
        ped = Pedigree()
        ped.load('../cplex/samples/pedigree_50_7_4_4_G8.ped')
        bn_no = pview.ped_to_bn(ped,0.05)
        bn_compact = pview.ped_to_bn_compact()
        ie_no = pview.gum.LazyPropagation(bn_no)
        ie_compact = pview.gum.LazyPropagation(bn_compact)

    def test_clique_csg(self):
        nb_ped = 50
        nb_people = [1900]
        nb_Gen_Max = [5]
        nb_Gen_Min = [5] #[math.ceil(x/2) for x in nb_Gen_Max]
        cl = 3
        min_clique = 100
        max_clique = 0
        mean_clique = 0

        min_csg = 100
        max_csg = 0
        mean_csg = 0
        ped1 = Pedigree()
        ped1.load("../data/ped/senegal2013.ped")
        bn_sen = pview.ped_to_bn_compact(ped1,0.05)
        print('clique sen',pview.max_clique_size(bn_sen))
        print('csg', len(ped1.all_consanguineous_ped(5)))
        for p, g_max, g_min in zip(nb_people, nb_Gen_Max, nb_Gen_Min):
            for nb in range(nb_ped):
                nbChild = random.randint(6, 12)
                g = random.randint(g_min, g_max)
                ped = Pedigree()
                ped.gen_ped(nb, p, g, nbChild, cl, 0.03)
                bn = pview.ped_to_bn_compact(ped,0.05)
                clique = pview.max_clique_size(bn)
                csg = len(ped.all_consanguineous_ped(g))

                if clique > max_clique:
                    max_clique = clique
                if clique < min_clique:
                    min_clique = clique
                mean_clique+=clique

                if csg > max_csg:
                    max_csg = csg
                if csg < min_csg:
                    min_csg = csg
                mean_csg+=csg
            print(max_clique,min_clique,mean_clique/nb_ped)
            print(max_csg,min_csg,mean_csg/nb_ped)

