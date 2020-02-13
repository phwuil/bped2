#!/usr/local/bin/python
import pickle as pkl
from typing import Set
import pickle as pkl

class People:
    def __init__(self, famID: str, pID: str, fatID: str, matID: str, sex: int = 0):
        self._famID = famID
        self._pID = pID
        self._fatID = fatID
        self._matID = matID
        self._sex = sex
        self._child = set()

    def __eq__(self, other):
        return (self.famID == other.famID) and (self.pID == other.pID) and (self.fatID == other.fatID) \
               and (self.matID == other.matID)and (self.sex == other.sex) and (self.child == other.child)

    @property
    def famID(self)-> str:
        # def get_famID(self):
        return self._famID

    @famID.setter
    def famID(self, famID)-> str:
        # self._famID=famID
        raise NameError("Cannot change FamID")

    @property
    def pID(self)-> str:
        return self._pID

    @pID.setter
    def pID(self, pid)-> str:
        raise NameError("Cannot change pid")

    @property
    def fatID(self)-> str:
        return self._fatID

    @fatID.setter
    def fatID(self, fatID)-> str:
        raise NameError("Cannot change FatID")

    @property
    def matID(self) -> str:
        return self._matID

    @matID.setter
    def matID(self, matID) -> str:
        raise NameError("Cannot change matID")

    @property
    def sex(self)-> int:
        return self._sex

    @sex.setter
    def sex(self, sex):
        self.sex = sex

    @property
    #def child(self)->Set[People]:
    def child(self):
        return self._child

    def add_children(self, cID):
        self._child.add(cID)

    def remove_children(self, cID):
        self._child.remove(cID)

    def __str__(self):
        # return "[%s %s %s %s %s]"%(self._famID,self.pID,self.famID,self.famID,self.sex)
        return f"[{self._famID} {self._pID} {self._fatID} {self._famID} {self._sex} {self._child}]"

    def __repr__(self):
        return f"People({id(self)} :" + self.__str__()


class Pedigree:
    sex_undefined=0
    sex_male =1
    sex_female = 2
    sex_malefemale=3

    def __init__(self):
        self._pedigree = dict()

    def get_pedigree(self):
        """
        Return the Pedigree
        """
        return self._pedigree

    def __len__(self):
        """
        Return the People's number in the pedigree
        """
        return len(self.get_pedigree())

    def get_people(self,idp:str)->People:
        """
        Return the People with the key = idp
        """
        return self._pedigree[idp]

    def load_old(self, fichier):
        """
        Read a .ped file and
        Return a dictionary where the keys are the people's IDs and the values are the People
        """
        file = open(fichier)
        for i in file.readlines():
            p = People(*i.strip().split())
            self._pedigree[p.pID] = p
        file.close()
        # Version old n'ajoute pas directement les enfants

    def load(self, fichier):
        """
        Read a .ped file and
        Return a dictionary where the keys are the people's IDs and the values are the People
        """
        f = open(fichier)
        for i in f.readlines():
            #print(People(*i.strip().split()))
            self.add_people(People(*i.strip().split()))
        f.close()
    def add_sex(self,pID:str,sex:int):
        """
        Modify the "sex value" for people 'pId'
        sex_undefined = unidentify
        sex_male = Male
        sex_female = Female
        sex_malefemale = Male AND Female (why not)
        """
        # check if sex already filled
        p=self.get_people(pID)
        if p.sex==self.sex_undefined:
            p.sex=sex
        elif p.sex!=sex:
            p.sex=sex.malefemale

    def add_sex_all(self):
        """
        Modify the "sex value" for all people if possible, due to fatID and MatID knowlege's
        """
        for k,v in self._pedigree.items():
            if v._fatID != '0':
                self.add_sex(v._fatID,self.sex_male)
            if v._matID != '0':
                self.add_sex(v._matID,self.sex_female)

    def add_children(self,people):
        """
        Fill the child parameter, due to fatID and MatID knowlege's
        """
        father = people._fatID
        mother = people._matID
        if father in self._pedigree:
            self._pedigree[father].add_children(people._pID)
        if mother in self._pedigree:
            self._pedigree[mother].add_children(people._pID)


    def add_children_all(self):
        """
        Complete the child attribute for all the pedigree's people
        """
        for v in self._pedigree.values():
            self.add_children(v)


    def save(self,filename):
        f = open(filename,"w")
        f.write(str(self._pedigree.values()))
        f.close()

    def add_people(self,people:People):
        """
        warning
        -------
        add_people tries hard to update childrens of father and mother but it is not reliable (parents may not already exist)
        """
        if people._pID=="0":
            raise ValueError('id "0" is not allowed for people')
        if self._pedigree[people.pID] in self._pedigree.keys():
            raise ValueError('id already use for another people')
        self._pedigree[people._pID] = people
        self.add_children(people)

    def remove_people(self,idp:str):
        """
        Remove the people 'idp' from the pedigree and from child, famID, and fatID if necessary
        """
        p=self.get_people(idp)

        # deal with parents
        father=p.fatID
        mother=p.matID
        if father in self._pedigree:
            self.get_people(father).remove_children(father)
        if mother in self._pedigree:
            self.get_people(mother).remove_children(father)

        # deal with children
        for chid in p.children:
            ch=self.get_people(chid)
            if ch.fatID==idp:
                ch._fatID="0"
            if ch.matID==idp:
                ch._matID="0"

        del self._pedigree[idp]


    def roots(self):
        """
        Return the olders, people without knowned parents
        """
        for k,v in self._pedigree.items():
            if v.fatID == '0' and v.matID == '0': # Si l'individu n'a pas de parents -> Racine
                yield v.pID

    def leaves(self):
        """
        People without childrens are leave
        """
        for k,v in self._pedigree.items():
            if len(v.child) == 0: # Si l'individu n'a pas d'enfants -> Feuille
                yield v.pID

    def domain(self):
        """
        Return all the different family present in the pedigree
        """
        dom = set()
        for k,v in self._pedigree.items():
            dom.add(v.famID)
        return dom

    def step_bro_sis(self,pID):
        """
        Do the symmetric difference (new set with elements in either father's child or mother's child but not both)

        """
        father = self.get_people(pID).fatID
        mother = self.get_people(pID).famID
        return self.get_people(father).child.symmetric_difference(self.get_people(mother).child)

    def parents(self,pID):
        """
        Return a tuple of the parents
        """
        return [self.get_people(pID).fatID,self.get_people(pID).famID]

    def grandparents(self,pID): #Probablement inutile
        """
        return a tuple of paternal and mather grandparents ((),())
        """
        father,mother = self.parents(pID)
        return [self.parents(father),self.parents(mother)]

    def old_generation(self,pID,nbG):
        """
        """
        if nbG == 1:
            return self.parents(pID)
        else:
            parents = self.parents(pID)
            [self.old_generation(i,nbG-1) for i in parents]


    def __str__(self):
        return ", ".join([str(v) for k,v in self._pedigree.items()])

