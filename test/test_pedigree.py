import unittest
import os

from bped2.pedigree import *

class TestPedigree(unittest.TestCase):

    def test_pedigree(self):#OK
        ped = Pedigree()
        ped.load_old("../data/fam9.ped")
        self.assertEqual    (ped.get_people('2'),People('9','2','0','0',0))
        self.assertEqual    (ped.get_people('20'),People('9','20','9','10'))

    def test_equal(self):#OK
        p=People('9','2','0','9','0')
        self.assertEqual   (p,People('9','2','0','9','0'))
        self.assertNotEqual(p,People('9','3','0','9','0'))
        self.assertNotEqual(p,People('9','2','1','9','0'))
        self.assertNotEqual(p,People('9','2','0','5','0'))
        self.assertNotEqual(p,People('9','2','0','9','1'))
        self.assertNotEqual(p,People('1','2','0','9','0'))

    def test_insertion(self):#OK
        ped = Pedigree()
        with self.assertRaises(ValueError):
            ped.add_people(People('1','0','0','9','0'))
        ped.load("../data/fam9.ped")
        with self.assertRaises(ValueError):
            ped.add_people(People('9','2','0','0',0))
        ped.add_people(People('9','30','0','0',0))
        self.assertTrue(ped.get_people('30'))

    def test_remove(self):#OK
        ped = Pedigree()
        ped.load("../data/fam9.ped")
        ped.add_children_all()
        ped.remove_people('2')
        with self.assertRaises(ValueError):
            ped.get_people('2') # Le people 2 n'existe plus
        self.assertEqual(ped.get_people('4').fatID,'0') #Le père a bien disparu
        ped.remove_people('10')
        self.assertTrue(ped.get_people('1').child=={'8','6','4'}) # L'enfant a bien été supprimé de la liste child

    def test_sex(self):#OK
        ped = Pedigree()
        ped.load_old("../data/fam9.ped")
        ped.add_sex_all()
        print(ped)
        self.assertEqual(ped.get_people('1').sex,2)
        self.assertEqual(ped.get_people('2').sex,1)
        self.assertEqual(ped.get_people('21').sex,0)
        self.assertEqual(ped.get_people('3').sex,1)
        self.assertNotEqual(ped.get_people('3').sex,3)

    def test_children(self):#OK
        ped = Pedigree()
        ped.load_old("../data/fam9.ped")
        ped.add_children(ped.get_people('8'))
        self.assertTrue(ped.get_people('1').child=={'8'})
        self.assertTrue(ped.get_people('2').child == {'8'})
        ped.add_children_all()
        self.assertTrue(ped.get_people('1').child == {'4','6','8','10'})
        self.assertTrue(ped.get_people('2').child == {'4','6','8','10'})
        self.assertTrue(len(ped.get_people('21').child) == 0)

    def test_save(self):#OK
        ped = Pedigree()
        ped.load_old("../data/fam9.ped")
        ped.save("../data/tanto.ped")
        self.assertEqual(os.path.exists("../data/tanto.ped"),1)

    def test_family(self):
        ped = Pedigree()
        #ped.load("../data/test.ped") #Ne fonctionne pas, erreur inconnu
        ped.load("../data/fam9.ped")
        ped.add_people(People('9', '23', '0', '0',1,{'1'})) #Père de 1
        ped.add_people(People('9', '24', '0', '0',2,{'1'})) #Mère de 1
        ped.add_people(People('9', '25', '23', '24',2)) # Soeur de 1
        ped.add_people(People('9', '26', '2', '25',1)) # Cousin de 8
        ped.add_sex_all()
        ped.add_children_all()
        self.assertEqual(ped.get_people('1'),People('9','1','23','24',2,{'4','6','8','10'}))
        self.assertEqual(ped.bro_sis('8'),set(['6','10','4']))
        self.assertEqual(ped.grandparents('8'),[['0', '0'], ['23', '24']])
        self.assertEqual(ped.uncles_aunts('8'),{'25'})
        self.assertEqual(ped.cousins('8'),{'26'})
        self.assertEqual(ped.grandparents('8'),[['0', '0'], ['23','24']])

    def test_generation(self):
        ped = Pedigree()
        # ped.load("../data/test.ped") #Ne fonctionne pas, erreur inconnu
        ped.load("../data/fam9.ped")
        ped.add_people(People('9', '23', '0', '0', 1, {'1'}))  # Père de 1
        ped.add_people(People('9', '24', '0', '0', 2, {'1'}))  # Mère de 1
        ped.add_people(People('9', '25', '23', '24', 2))  # Soeur de 1
        ped.add_people(People('9', '26', '2', '25', 1))  # Cousin de 8
        ped.add_sex_all()
        ped.add_children_all()
        print('blabla',ped.old_generation('8', 2))

    def test_graph(self):
        ped = Pedigree()
        ped.load("../data/fam9.ped")
        ped.graph1()



