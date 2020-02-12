import unittest

from bped2.pedigree import *

class TestPedigree(unittest.TestCase):

    def test_pedigree(self):
        ped = Pedigree()
        ped.load("../data/fam9.ped")
        p1 = ped.getPeople('2')
        p = People(9,2,0,9,0)
        print(ped.getPedigree().get('2'))
        print(type(ped.getPeople('2')),ped.getPeople('2'))
        print(type(p),p)
        self.assertEqual(p1,p)
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

