import unittest

from bped2.pedigree import *

class TestPedigree(unittest.TestCase):

    def test_pedigree(self):
        ped = Pedigree()
        ped.load("../data/fam9.ped")
        p = ped.getPeople('2')
        self.assertEqual   (p,People('9','2','0','9','0'))

    def test_equal(self):
        p=People('9','2','0','9','0')
        self.assertEqual   (p,People('9','2','0','9','0'))
        self.assertNotEqual(p,People('9','3','0','9','0'))
        self.assertNotEqual(p,People('9','2','1','9','0'))
        self.assertNotEqual(p,People('9','2','0','5','0'))
        self.assertNotEqual(p,People('9','2','0','9','1'))
        self.assertNotEqual(p,People('1','2','0','9','0'))

    def test_insertion(self):
        ped = Pedigree()
        with self.assertRaises(self,ValueError):
            ped.add_people(self,People('1','0','0','9','0'))

    # def test_main(self):
    #     ped = Pedigree()
    #     ped.load("../data/fam9.ped")
    #     #print(p.getPeople(3))
    #     print("affichage de ped \n",ped)
    #     p = People(4,4,4,4,4)
    #     print("affichage d'un People\n",p)
    #     ped.addPeople(p)
    #     print("affichage de ped après ajout \n",ped)
    #     ped.removePeople(4)
    #     print("affichage de ped après remove \n",ped)
    #     ped.sex()
    #     print("affichage de ped avec le sexe\n",ped)
    #     ped.add_children_all()
    #     print("ajout des enfants \n",ped)

