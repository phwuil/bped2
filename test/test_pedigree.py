import unittest
import os
import math
from bped2.pedigree import *
import bped2.view as pview
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
        ped.load("../data/ped/fam9.ped")
        with self.assertRaises(ValueError):
            ped.add_people('9', '2', '0', '0')
        ped.add_people('9', '30', '0', '0')
        self.assertTrue(ped.get_people('30'))

    def test_remove(self):#OK
        ped = Pedigree()
        ped.load("../data/ped/fam9.ped")
        ped.update_children_all()
        ped.remove_people('2')
        with self.assertRaises(ValueError):
            ped.get_people('2') # People 2 has been removed
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
        pview.save(ped,"../data/ped/tanto.ped")
        self.assertEqual(os.path.exists("../data/ped/tanto.ped"),1)

    def test_family(self):#OK
        ped = Pedigree()
        ped.load("../data/ped/fam9.ped")
        self.assertEqual(ped.get_couple(),{('2','1'),('3','4'),('6','5'),('8','7'),('9','10')})
        ped.add_people('9', '23', '0', '0') # Father of 1
        ped.add_people('9', '24', '0', '0') # Mother of 1
        ped.get_people('1')._set('9','23','24')
        ped.add_people('9', '25', '23', '24') # Sister of 1
        ped.add_people('9', '26', '2', '25') # Cousin of 8
        ped.add_sex_all()
        ped.update_children_all()
        self.assertEqual(ped.get_people('1').fatID,'23')
        self.assertEqual(ped.get_people('1').matID,'24')
        self.assertEqual(ped.get_bro_sis('8'),set(['6','10','4']))
        self.assertEqual(ped.get_grand_parents('8'),set(['23', '24']))
        self.assertEqual(ped.get_uncles_aunts('8'),{'25'})
        self.assertEqual(ped.get_cousins('8'),{'26'})


    def test_generation(self):#OK
        ped = Pedigree()
        ped.load("../data/ped/fam9.ped")
        ped.add_people('9', '23', '0', '0') # Father of 1
        ped.add_people('9', '24', '0', '0') # Mother of 1
        ped.get_people('1')._set('9','23','24')
        ped.add_people('9', '25', '23', '24') # Sister of 1
        ped.add_people('9', '26', '2', '25') # Cousin of 8
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

    def test_check(self): #OK
        ped = Pedigree()
        ped1 = Pedigree()
        ped.load("../data/ped/senegal2013.ped")
        ped1.load("../data/ped/fam9.ped")
        print(len(ped.get_domain()),ped.check_one_people_family()) # 161 people alone
        self.assertEqual(ped.check_one_people_family(),198-37)
        print(ped.check_mother_and_father()) # no sex change
        print(ped.check_consanguinity('N501426',5))
        print("N1 consanguin",ped.check_consanguinity_family('N1'))
        print(len(ped.check_famID('N501426')),ped.check_famID('N501426'))


    def test_generation_pedigree(self): #OK
        ped = Pedigree()
        ped.load("../data/ped/senegal2013.ped")
        N1 = ped.gen_family_pedigree('N1')
        new = ped.gen_all_pedigree()
        self.assertEqual(new['N1'],N1)

    def test_graph(self): #OK
        ped3 = Pedigree()
        ped3.load("../data/ped/senegal2013.ped")
        N8 = ped3.gen_family_pedigree('N8')
        N8.add_sex_all()
        N8.update_children_all()
        N8.update_parents_all()
        pview.graph(N8,"N8", False)

        fam9 = Pedigree()
        fam9.load("../data/ped/fam9.ped")
        fam9.add_sex_all()
        fam9.update_children_all()
        fam9.update_parents_all()
        pview.graph(fam9,"fam9", False)

        N1 = ped3.gen_family_pedigree('N1')
        N1.add_sex_all()
        N1.update_children_all()
        N1.update_parents_all()
        pview.graph(N1,"N1", True)

    def test_pedigree_file(self): #OK
        fam9 = Pedigree()
        fam9.load("../data/ped/fam9.ped")
        fam9.add_sex_all()
        fam9.update_children_all()
        fam9.update_parents_all()
        fam9.pedigree_overview_file("fam9_overview",True)

        senegal = Pedigree()
        senegal.load("../data/ped/senegal2013.ped")
        senegal.add_sex_all()
        senegal.update_children_all()
        senegal.update_parents_all()
        senegal.pedigree_overview_file("senegal_overview",False)


    def test_new_gen(self): #OK
        nb_ped = 1
        nb_people = [50]
        nb_Gen_Max = [4]
        nb_Gen_Min = [math.ceil(x/2) for x in nb_Gen_Max]
        cl = 3
        ped1 = Pedigree()
        ped1.load("../data/ped/senegal2013.ped")
        bn_sen = pview.ped_to_bn_compact(ped1,0.05)
        print('clique sen',pview.max_clique_size(bn_sen))
        print('uho', ped1.all_consanguineous_ped(cl))
        for p, g_max, g_min in zip(nb_people, nb_Gen_Max, nb_Gen_Min):
            for nb in range(nb_ped):
                nbChild = random.randint(4, 8)
                g = random.randint(g_min, g_max)
                ped = Pedigree()
                ped.gen_ped(nb, p, g, nbChild, cl)
                # print('-------------------------')
                # print(ped)
                print('-------------------------')
                print('Consanguin',ped.all_consanguineous_ped(cl))
                bn = pview.ped_to_bn_compact(ped,0.05)
                print('clique',pview.max_clique_size(bn))
                print('-------------------------')
                pview.save(ped, f'../pedigree_{p}_{g}_{nbChild}_{cl-1}_G{nb}')
                pview.graph(ped, f'../generate_graph_{p}_{g}_{nbChild}_{cl-1}_G{nb}', False)

    def test_depth(self): #OK
        ped = Pedigree()
        ped.load("../data/ped/fam9.ped")
        ped1 = Pedigree()
        ped1.load("../data/ped/senegal2013.ped")
        print(ped1.mean_weeding())
        print(len(ped1.all_consanguineous_ped(5)))
        ped2 = Pedigree()
        ped2.gen_ped('test',1900,5,10,3,0.4)
        print(ped2.mean_weeding())
        print('ocho',len(ped2.all_consanguineous_ped(5)))

    def xxxtest_random_ped(self):
        ped = Pedigree()
        #ped.load('../cplex/pedigree_50_3_6_4_G1.ped')
        ped.load('../cplex/pedigree_50_3_10_1_G1.ped')
        print(ped.check_consanguinity_pedigree())
        print(ped.is_consanguineous('2','10',1))
        print(ped.old_gen('2',1))
        print(ped.old_gen('10', 1))
        print(ped.check_consanguinity('9',4))
        print(ped.all_consanguineous_ped(4))

    def xxxtest_check_consanguinity(self):
        ped = Pedigree()
        ped.load('../cplex/pedigree_50_4_8_2_G3.ped')
        print(ped.all_consanguineous_ped(3))
        print(ped.is_consanguineous('1','7',2))
        print(ped.old_gen('1',4).intersection(ped.old_gen('7',4)))
        print(ped.old_gen('7', 4))
        print('---------------------------')
        nb_ped = 50
        nb_people = [10,20,50,100,200,300,500,1000,1500,2000,2200,2400]
        nb_Gen_Max = [3,3,4,4,4,4,4,5,5,6,6,6]
        # nb_people = [50]
        # nb_Gen_Max = [4]
        nb_Gen_Min = [math.ceil(x/2) for x in nb_Gen_Max]
        cl = 3
        cpt = 0
        for p, g_max, g_min in zip(nb_people, nb_Gen_Max, nb_Gen_Min):
            for nb in range(nb_ped):
                nbChild = random.randint(4, 8)
                g = random.randint(g_min, g_max)
                ped = Pedigree()
                ped.gen_ped(nb, p, g, nbChild, cl)

                if len(ped.all_consanguineous_ped(cl)) != 0:
                    cpt+=1
                    print('ICI IL Y A UN PB',ped.all_consanguineous_ped(3))
                    print('le pedigree en question',ped)
                    pview.save(ped, f'../pedigree_{p}_{g}_{nbChild}_{cl - 1}_G{nb}')
                    pview.graph(ped, f'../generate_graph_{p}_{g}_{nbChild}_{cl - 1}_G{nb}', False)
            print(cpt)
            self.assertEqual(cpt,0)

    def test_check_pedigree(self): #OK
        ped = Pedigree()
        ped.gen_ped('f', 2000, 10, 6, 3)
        pview.graph(ped, f'../jpp', True)
        print(ped)

    def blabla(self):
        ped = Pedigree()
        ped.load('../cplex/samples/IS/pedigree_10_3_7_3_G2.ped')
        pview.graph(ped,generate,True)
