import unittest
import os

from bped2.pedigree import *

class TestPedigree(unittest.TestCase):

    def test_pedigree(self):#OK
        ped = Pedigree()
        ped.load_old("../data/fam9.ped")
        print(ped._audit)
        self.assertEqual    (ped.get_people('2'),People('9','2','0','0'))
        self.assertEqual    (ped.get_people('20'),People('9','20','9','10'))

    def test_equal(self):#OK
        p=People('9','2','0','9')
        self.assertEqual   (p,People('9','2','0','9'))
        self.assertNotEqual(p,People('9','3','0','9'))
        self.assertNotEqual(p,People('9','2','1','9'))
        self.assertNotEqual(p,People('9','2','0','5'))
        self.assertNotEqual(p,People('1','2','0','9'))

    def test_insertion(self):#OK
        ped = Pedigree()
        with self.assertRaises(ValueError):
            ped.add_people('1', '0', '0', '9')
            # ped.add_people(People('1','0','0','9','0'))
        ped.load("../data/fam9.ped")
        with self.assertRaises(ValueError):
        #     ped.add_people(People('9','2','0','0',0))
        # ped.add_people(People('9','30','0','0',0))
            ped.add_people('9', '2', '0', '0')
        ped.add_people('9', '30', '0', '0')
        self.assertTrue(ped.get_people('30'))

    def test_remove(self):#OK
        ped = Pedigree()
        ped.load("../data/fam9.ped")
        ped.update_children_all()
        ped.remove_people('2')
        with self.assertRaises(ValueError):
            ped.get_people('2') # Le people 2 n'existe plus
        self.assertEqual(ped.get_people('4').fatID,'0') #Le père a bien disparu
        ped.remove_people('10')
        print(ped.get_people('1'))
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
        ped.update_children(ped.get_people('8'))
        self.assertTrue(ped.get_people('1').child=={'8'})
        self.assertTrue(ped.get_people('2').child == {'8'})
        ped.update_children_all()
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
        # ped.add_people(People('9', '23', '0', '0',1,{'1'})) #Père de 1
        # ped.add_people(People('9', '24', '0', '0',2,{'1'})) #Mère de 1
        ped.add_people('9', '23', '0', '0')
        ped.add_people('9', '24', '0', '0')
        ped.get_people('1')._set('9','23','24')
        ped.add_people('9', '25', '23', '24') # Soeur de 1
        ped.add_people('9', '26', '2', '25') # Cousin de 8
        ped.add_sex_all()
        ped.update_children_all()
        print(ped.get_people('1'))
        # self.assertEqual(ped.get_people('1'),People('9','1','23','24',2,{'4','6','8','10'}))
        # self.assertEqual(ped.bro_sis('8'),set(['6','10','4']))
        # self.assertEqual(ped.grandparents('8'),[['0', '0'], ['23', '24']])
        # self.assertEqual(ped.uncles_aunts('8'),{'25'})
        # self.assertEqual(ped.cousins('8'),{'26'})
        # self.assertEqual(ped.grandparents('8'),[['0', '0'], ['23','24']])

    def test_generation(self):
        ped = Pedigree()
        # ped.load("../data/test.ped") #Ne fonctionne pas, erreur inconnu
        ped.load("../data/fam9.ped")
        ped.add_people(People('9', '23', '0', '0', 1, {'1'}))  # Père de 1
        ped.add_people(People('9', '24', '0', '0', 2, {'1'}))  # Mère de 1
        ped.add_people(People('9', '25', '23', '24', 2))  # Soeur de 1
        ped.add_people(People('9', '26', '2', '25', 1))  # Cousin de 8
        ped.add_sex_all()
        ped.update_children_all()
        print(ped.old_generation('8', 2)) # Semble fonctionner
        print(ped.next_generation('23',2)) # Ne fonctionne pas

    def test_number(self):
        ped = Pedigree()
        ped.load("../data/fam9.ped")
        self.assertEqual(len(ped.family_number_members()),1)
        ped.add_people(People('A', '23', '0', '0', 1, {'1'}))
        self.assertEqual(len(ped.family_number_members()),2)
        ped.remove_family('A')
        self.assertEqual(len(ped.family_number_members()),1)

        ped1 = Pedigree()
        ped1.load("../data/senegal2013.ped")
        ped1.remove_family('D1')
        self.assertNotEqual(sorted(ped.get_domain())[0], 'D1')
        ped1.get_one_family('D10')
        self.assertEqual(len(ped.get_domain()), 1)

    def test_clean(self):
        ped = Pedigree()
        ped.load("../data/senegal2013.ped")
        print("avant netoyage", len(ped.get_domain())) #198 familles
        ped.clear_pedigree()
        print("apres nettoyage", len(ped.get_domain())) #37 familles
        dico = ped.family_number_members()
        print(dico)

    def test_graph(self):
        # ped1 = Pedigree()
        # ped1.load("../data/fam9.ped")
        # ped1.graph("fam9")
        #
        # ped2 = Pedigree()
        # ped2.load("../data/famRh.ped")
        # ped2.graph("famRh")

        ped3 = Pedigree()
        ped3.load("../data/senegal2013.ped")
        ped3.get_one_family('N8')
        ped3.graph("senegal2013")
        # Trop volumineux, meme avec une seul famille


