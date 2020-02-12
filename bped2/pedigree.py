#!/usr/local/bin/python
import pickle as pkl
import pandas as pd
import numpy as np

class Pedigree:
    def __init__(self):
        self._pedigree = dict()
        self._nb = 0

    def getPedigree(self):
        return self._pedigree

    def getNB(self):
        return self._nb

    def getPeople(self,idp):
        return self._pedigree[idp]

    def load(self, fichier):
        for i in open(fichier).readlines():
            tmp = i.strip().split()
            p = People(tmp[0],tmp[1],tmp[2],tmp[3])
            #print(p)
            self._pedigree[tmp[1]] = p
        self._nb = len(self._pedigree)
        #tab = [i.strip().split() for i in open(fichier).readlines()]
        #self.pedigree[nb] = People()
        #self.nb = len(self.p)

    def sex(self):
        return

    def pedigreeToFile(self):
        return

    def addPeople(self,people):
        self._pedigree[people.pID] = people
        self._nb = len(self._pedigree)

    def removePeople(self,idp):
        del self._pedigree[idp]

    def __str__(self):
        return ", ".join([str(v) for k,v in self._pedigree.items()])

class People:
    def __init__(self,famID,pID,fatID,matID,sex=None):
        self._famID = famID
        self._pID = pID
        self._fatID = fatID
        self._matID = matID
        self._sex = 0

    @property
    def get_famID(self):
        return self._famID

    def famID(self,famID):
        #self._famID=famID
        raise NameError("Cannot change FamID")

    def get_pID(self):
        return self.pID

    def get_fatID(self):
        return self.fatID

    def get_matID(self):
        return self.matID

    def get_sex(self):
        return self.sex

    def set_pID(self,pid):
        raise NameError("Cannot change pid")

    def set_fatID(self,fatID):
        raise NameError("Cannot change FatID")

    def set_matID(self,matID):
        raise NameError("Cannot change matID")

    def set_sex(self,sex):
        self.sex = sex

    def __str__(self):
        #return "[%s %s %s %s %s]"%(self._famID,self.pID,self.famID,self.famID,self.sex)
        return f"{self._famID}"

    # pid = property(get_pID,set_pID)
    # fatID = property(get_fatID,set_fatID)
    # famID = property(get_famID,set_famID)
    # sex = property(get_sex,set_sex)