import unittest
import os

from bped2.pedigree import *
import bped2.view as pview
import sandbox.doLazyProg as lazy

class TestPedigree(unittest.TestCase):

    def test_gen_bn(self):
        ped = Pedigree()
        ped.load("../cplex/samples/pedigree_1000_50_4_4_G49.ped")
        bn = pview.ped_to_bn(ped,0.05)
        #pview.save_bn(bn,'toto')
        print(lazy.doLazyProg("../cplex/bn/bn_1000_50_4_4_G49.bif"))


