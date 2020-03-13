import unittest
import os

from bped2.pedigree import *

class TestPedigree(unittest.TestCase):

    def xxtest_pedigree(self):#OK
        ped = Pedigree()
        ped.load("../data/ped/fam9.ped")
        print(ped._people2line)
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
        ped.load("../data/ped/fam9.ped")
        with self.assertRaises(ValueError):
        #     ped.add_people(People('9','2','0','0',0))
        # ped.add_people(People('9','30','0','0',0))
            ped.add_people('9', '2', '0', '0')
        ped.add_people('9', '30', '0', '0')
        self.assertTrue(ped.get_people('30'))

    def test_remove(self):#OK
        ped = Pedigree()
        ped.load("../data/ped/fam9.ped")
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
        ped.load("../data/ped/fam9.ped")
        ped.add_sex_all()
        print(ped)
        self.assertEqual(ped.get_people('1').sex,2)
        self.assertEqual(ped.get_people('2').sex,1)
        self.assertEqual(ped.get_people('21').sex,0)
        self.assertEqual(ped.get_people('3').sex,1)
        self.assertNotEqual(ped.get_people('3').sex,3)
        self.assertEqual(len(ped.get_male()),5)
        self.assertEqual(len(ped.get_female()),5)

    def test_children(self):#OK
        ped = Pedigree()
        ped.load("../data/ped/fam9.ped")
        ped.update_children('8')
        ped.update_children_all()
        self.assertTrue(ped.get_people('1').child == {'4','6','8','10'})
        self.assertTrue(ped.get_people('2').child == {'4','6','8','10'})
        self.assertTrue(len(ped.get_people('21').child) == 0)

    def test_save(self):#OK
        ped = Pedigree()
        ped.load("../data/ped/fam9.ped")
        ped.save("../data/ped/tanto.ped")
        self.assertEqual(os.path.exists("../data/ped/tanto.ped"),1)

    def test_family(self):
        ped = Pedigree()
        ped.load("../data/ped/fam9.ped")
        self.assertEqual(ped.get_couple(),{('2','1'),('3','4'),('6','5'),('8','7'),('9','10')})
        ped.add_people('9', '23', '0', '0') #Père de 1
        ped.add_people('9', '24', '0', '0') #Mère de 1
        ped.get_people('1')._set('9','23','24')
        ped.add_people('9', '25', '23', '24') # Soeur de 1
        ped.add_people('9', '26', '2', '25') # Cousin de 8
        ped.add_sex_all()
        ped.update_children_all()
        self.assertEqual(ped.get_people('1').fatID,'23')
        self.assertEqual(ped.get_people('1').matID,'24')
        self.assertEqual(ped.get_bro_sis('8'),set(['6','10','4']))
        self.assertEqual(ped.get_grand_parents('8'),set(['23', '24']))
        self.assertEqual(ped.get_uncles_aunts('8'),{'25'})
        self.assertEqual(ped.get_cousins('8'),{'26'})


    def test_generation(self):
        ped = Pedigree()
        # ped.load("../data/ped/test.ped") #Ne fonctionne pas, erreur inconnu
        ped.load("../data/ped/fam9.ped")
        ped.add_people('9', '23', '0', '0') #Père de 1
        ped.add_people('9', '24', '0', '0') #Mère de 1
        ped.get_people('1')._set('9','23','24')
        ped.add_people('9', '25', '23', '24') # Soeur de 1
        ped.add_people('9', '26', '2', '25') # Cousin de 8
        ped.add_sex_all()
        ped.update_children_all()
        print(ped.old_gen('8', 2))
        print(ped.next_gen('23', 2))


    def test_number(self): #OK
        ped = Pedigree()
        ped.load("../data/ped/fam9.ped")
        self.assertEqual(len(ped.get_stat_family()), 1)
        ped.add_people('A', '23', '0', '0')
        ped.add_sex('23',1)
        ped.get_people('23').add_children('1')
        self.assertEqual(len(ped.get_stat_family()), 2)
        ped.remove_family('A')
        self.assertEqual(len(ped.get_stat_family()), 1)

        ped1 = Pedigree()
        ped1.load("../data/ped/senegal2013.ped")
        ped1.remove_family('D1')
        self.assertNotEqual(sorted(ped.get_domain())[0], 'D1')
        ped1.gen_family_pedigree('D10')
        self.assertEqual(len(ped.get_domain()), 1)

    def test_clean(self): #OK
        ped = Pedigree()
        ped.load("../data/ped/senegal2013.ped")
        print("avant netoyage", len(ped.get_domain())) #198 familles
        ped.remove_singleton()
        print("apres nettoyage", len(ped.get_domain())) #37 familles
        dico = ped.get_stat_family()
        print(dico)

    def test_check(self):
        ped = Pedigree()
        ped1 = Pedigree()
        ped.load("../data/ped/senegal2013.ped")
        ped1.load("../data/ped/fam9.ped")
        print(len(ped.get_domain()),ped.check_one_people_family()) # 161 membres isolés
        self.assertEqual(ped.check_one_people_family(),198-37)
        print(ped.check_mother_and_father()) #Aucun changement de sexe
        print(ped.check_consanguinity('N501426',5))
        print("N1 consanguin",ped.check_consanguinity_family('N1'))
        print(len(ped.check_famID('N501426')),ped.check_famID('N501426')) #Probablement faux mais compliquer a verifier

    def test_consanguinity(self):
        ped = Pedigree()
        ped.load("../data/ped/famRh.ped")
        self.assertTrue(ped.is_consanguineous('5','6',3))
        self.assertFalse(ped.is_consanguineous('3','4',3))

    def test_generation_pedigree(self):
        ped = Pedigree()
        ped.load("../data/ped/senegal2013.ped")
        N1 = ped.gen_family_pedigree('N1')
        new = ped.gen_all_pedigree()
        self.assertEqual(new['N1'],N1)

    def test_graph(self):
        ped3 = Pedigree()
        ped3.load("../data/ped/senegal2013.ped")
        N8 = ped3.gen_family_pedigree('N8')
        N8.add_sex_all()
        N8.update_children_all()
        N8.update_parents_all()
        N8.graph("N8", False)

        fam9 = Pedigree()
        fam9.load("../data/ped/fam9.ped")
        fam9.add_sex_all()
        fam9.update_children_all()
        fam9.update_parents_all()
        fam9.graph("fam9", False)

        N1 = ped3.gen_family_pedigree('N1')
        N1.add_sex_all()
        N1.update_children_all()
        N1.update_parents_all()
        N1.graph("N1", True)

    def test_pedigree_file(self):
        fam9 = Pedigree()
        fam9.load("../data/ped/fam9.ped")
        fam9.add_sex_all()
        fam9.update_children_all()
        fam9.update_parents_all()
        fam9.pedigree_overview_file("fam9_overview")

        senegal = Pedigree()
        senegal.load("../data/ped/senegal2013.ped")
        senegal.add_sex_all()
        senegal.update_children_all()
        senegal.update_parents_all()
        senegal.pedigree_overview_file("senegal_overview")

    def test_test(self):
        ped = Pedigree()
        ped.generation_ped('3',4,10)
        print(ped)
        ped.graph('generate_graph', False)

    def test_new_gen(self):
        ped = Pedigree()
        ped.gen_ped('test',10,3,4,4)
        print(ped)
