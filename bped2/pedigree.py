#!/usr/local/bin/python
import pickle as pkl
import pandas as pd
import numpy as np

class Pedigree:
    def __init__(self):
        self.pedigree = {}
        self.nb = 0
    
    def getPedigree(self):
        return self.pedigree

    def getNB(self):
        return self.nb

    def getPeople(self,idp):
        return self.pedigree[idp]

    def load(self, fichier):
        cpt = 0
        for i in open(fichier).readlines():
            tmp = i.strip().split()
            p = People(tmp[0],tmp[1],tmp[2],tmp[3])
            #print(p)
            self.pedigree[cpt] = p
            cpt+=1
        self.nb = cpt
        #tab = [i.strip().split() for i in open(fichier).readlines()]
        #self.pedigree[nb] = People()
        #self.nb = len(self.p)
    
    def sex(self):
        return

    def pedigreeToFile(self):
        return

    def addPeople(self,people):
        cpt = self.nb
        self.pedigree[cpt] = people

    def removePeople(self,idp):
        del self.pedigree[idp]

    def __str__(self):
        res = ""
        for i in (self.pedigree.keys()):
            res+=(self.pedigree[i].__str__()) + "\n"
        return res

class People:
    def __init__(self,famID,pID,fatID,matID,sex=None):
        self.famID = famID
        self.pID = pID
        self.fatID = fatID
        self.matID = matID
        self.sex = 0
    
    def get_famID(self):
        return self.famID

    def get_pID(self):
        return self.pID

    def get_fatID(self):
        return self.fatID

    def get_matID(self):
        return self.matID

    def get_sex(self):
        return self.sex

    def set_famID(self,famID):
        raise NameError("Cannot change FamID")

    def set_pID(self,pid):
        raise NameError("Cannot change pid")

    def set_fatID(self,fatID):
        raise NameError("Cannot change FatID")   

    def set_matID(self,matID):
        raise NameError("Cannot change matID")

    def set_sex(self,sex):
        self.sex = sex  

    def __str__(self):
        return "[%s %s %s %s %s]"%(self.famID,self.pID,self.famID,self.famID,self.sex)

    # famID = property(get_famID,set_famID)
    # pid = property(get_pID,set_pID)
    # fatID = property(get_fatID,set_fatID)
    # famID = property(get_famID,set_famID)
    # sex = property(get_sex,set_sex)