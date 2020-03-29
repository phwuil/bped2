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


