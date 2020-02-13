import unittest

from bped2.pedigree import *

class TestPedigree(unittest.TestCase):

    def test_pedigree(self):
        ped = Pedigree()
        ped.load_old("../data/fam9.ped")
        self.assertEqual    (ped.get_people('2'),People('9','2','0','0',0))
        self.assertEqual    (ped.get_people('20'),People('9','20','9','10'))

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
        ped.load("../data/fam9.ped")
        with self.assertRaises(self, ValueError):
            ped.add_people(People('9','2','0','0',0))
        ped.add_people(People('9','30','0','0',0))
        self.assertTrue(ped.get_people('30'))

    def test_remove(self):
        ped = Pedigree()
        ped.load("../data/fam9.ped")
        ped.add_children_all()
        ped.remove_people('2')
        self.assertFalse(ped.get_people('2')) # Le people 2 n'existe plus
        self.assertTrue(ped.get_people('4')==People('9','4','0','1')) #Le père a bien disparu
        ped.remove_people('10')
        self.assertTrue(ped.get_people('1').child=={'8','6','4'}) # L'enfant a bien été supprimé de la liste child

    def test_sex(self):
        ped = Pedigree
        ped.load_old("../data/fam9.ped")
        ped.add_sex_all()
        print(ped)
        self.assertEqual(ped.get_people('1').sex,2)
        self.assertEqual(ped.get_people('2').sex,1)
        self.assertEqual(ped.get_people('21').sex,0)
        self.assertEqual(ped.get_people('3').sex,1)
        self.assertNotEqual(ped.get_people('3').sex,3)

    def test_children(self):
        ped = Pedigree
        ped.load_old("../data/fam9.ped")
        ped.add_children('8')
        self.assertTrue(ped.get_people('1').child=={'8'})
        self.assertTrue(ped.get_people('2').child == {'8'})
        ped.add_children_all()
        self.assertTrue(ped.get_people('1').child == {'4','6','8','10'})
        self.assertTrue(ped.get_people('2').child == {'4','6','8','10'})
        self.assertTrue(ped.get_people('21').child == {})

    # def test_save(self):
    #     ped = Pedigree()
    #     ped.load_old("../data/fam9.ped")
    #     ped.save("../data/tanto.ped")
    #     self.assertTrue(open("../data/tanto.ped"))

