import unittest
import os

from bped2.pedigree import *

class TestPedigree(unittest.TestCase):

    def test_gen_bn(self):
        ped = Pedigree()
        ped.load("../data/ped/fam9.ped")
        bn = ped.ped_to_bn(0.05)
