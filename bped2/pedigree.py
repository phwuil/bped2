#!/usr/local/bin/python
import pickle as pkl
from typing import Set
import pickle as pkl
import pygraphviz as pgv
from graphviz import *

class People:
    def __init__(self, famID: str, pID: str, fatID: str, matID: str, sex: int = 0,child = None):
        self._famID = famID
        self._pID = pID
        self._fatID = fatID
        self._matID = matID
        self._sex = sex
        if child is None:
            self._child = set()
        else:
            self._child = child

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
        self._sex = sex

    @property
    def child(self):
        return self._child

    def add_children(self, cID):
        """
        Add the children to his parent's set
        """
        self._child.add(cID)

    def remove_children(self, cID):
        """
        Remove the children from the child set of his parent
        """
        self._child.remove(cID)

    def __str__(self):
        # return "[%s %s %s %s %s]"%(self._famID,self.pID,self.matID,self.famID,self.sex)
        return f"[{self._famID} {self._pID} {self._fatID} {self._matID} {self._sex} {self._child}]"

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
        if idp not in self._pedigree.keys():
            raise ValueError(f"ID: {idp} is not in the pedigree")
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
        file = open(fichier)
        for i in file.readlines():
            self.add_people(People(*i.strip().split()))
        file.close()

    def save(self,filename):
        """
        Save the current Pedigree in a file : filename.ped
        """
        f = open(filename,"w")
        for i in self._pedigree.values():
            f.write(f"{i._famID}\t{i._pID}\t{i._fatID}\t{i._matID}\t{i._sex}\t{i._child} \n")
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
        father = people.fatID
        mother = people.matID
        if father in self._pedigree:
            self._pedigree[father].child.add(people.pID)
            #self.get_people(father).child.add(people.pID)
            #self._pedigree[father].add_children(people._pID)
        if mother in self._pedigree:
            self._pedigree[mother].child.add(people.pID)
            #self.get_people(mother).child.add(people.pID)
            #self._pedigree[mother].add_children(people._pID)


    def add_children_all(self):
        """
        Complete the child attribute for all the pedigree's people
        """
        for v in self._pedigree.values():
            self.add_children(v)

    def add_parents(self, people):
        """
        Fill the fatID and matID if possible due to param child of the people
        """
        if len(people.child) != 0 and people.sex != 0: #S'il a au moins un enfant et un sexe connu
            for i in people.child:
                #print(self.get_people(i).fatID)
                if self.get_people(i).fatID == '0' and people.sex == 1:
                    self.get_people(i)._fatID = people.pID
                if self.get_people(i).matID == '0' and people.sex == 2:
                    self.get_people(i)._matID = people.pID
    def add_parents_all(self):
        """
        Complete the fat/fam attribute for all the pedigree's people
        """
        for k,v in self._pedigree.items():
            self.add_parents(v)


    def add_people(self,people:People):
        """
        warning
        -------
        add_people tries hard to update childrens of father and mother but it is not reliable (parents may not already exist)
        """
        if people.pID=='0':
            raise ValueError('id "0" is not allowed for people')
        #if self._pedigree[people.pID] in self._pedigree.keys():
        if people.pID in self._pedigree.keys():
            raise ValueError('id already use for another people')
        else:
            self._pedigree[people.pID] = people
            self.add_children(people)
            self.add_parents(people)

    def remove_people(self,idp:str):
        """
        Remove the people 'idp' from the pedigree and from child, matID, and fatID if necessary
        """
        p = self.get_people(idp)

        # deal with parents
        father = p.fatID
        mother = p.matID
        if father in self._pedigree:
            self.get_people(father).remove_children(idp)
        if mother in self._pedigree:
            self.get_people(mother).remove_children(idp)

        # deal with children
        for chid in p.child:
            ch=self.get_people(chid)
            if ch.fatID==idp:
                ch._fatID="0"
            if ch.matID==idp:
                ch._matID="0"

        del self._pedigree[idp]

    def clear_pedigree(self):
        """
        If a people doesn't have any parents and childrens, remove him from the pedigree
        """
        for f,v in list(self._pedigree.items()):
            if v.fatID == '0' and v.matID == '0' and len(v.child)== 0:
                self.remove_people(v.pID)

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

    def bro_sis(self,pID):
        """
        Return brothers and sister of a People, without step family
        """
        father = self.get_people(pID).fatID
        mother = self.get_people(pID).matID
        if father != '0' or mother != '0': # Au moins 1 des parents est connu
            bros = self.get_people(father).child.intersection(self.get_people(mother).child)
            bros.remove(pID)
        else:
            bros = set()
        return bros


    def step_bro_sis(self,pID):
        """
        Do the symmetric difference (new set with elements in either father's child or mother's child but not both)

        """
        father = self.get_people(pID).fatID
        mother = self.get_people(pID).matID
        step_bros = self.get_people(father).child.symmetric_difference(self.get_people(mother).child)
        step_bros.remove(pID)
        return step_bros

    def uncles_aunts(self,pID)->set:
        """
        Return the uncles and aunts of a individu
        """
        father, mother = self.parents(pID)
        return self.bro_sis(father).union(self.bro_sis(mother))

    def cousins(self,pID):
        """
        Return the cousins of an individu
        """
        people = set()
        uncles_aunts = self.uncles_aunts(pID)
        for i in uncles_aunts:
            for j in self.get_people(i).child: # Pas opti mais je vois pas comment faire autrement
                people.add(j)
        return people

    def parents(self,pID):
        """
        Return a tuple of the parents
        """
        return [self.get_people(pID).fatID,self.get_people(pID).matID]

    def grandparents(self,pID): #Probablement inutile
        """
        return a tuple of paternal and mather grandparents ((),())
        """
        father,mother = self.parents(pID)
        return [self.parents(father),self.parents(mother)]

    def remove_family(self,famID):
        """
        Remove an entire family in the Pedigree
        """
        for k,v in list(self._pedigree.items()):
            if v.famID == famID:
                del self._pedigree[k] # Pas besoin de faire attention aux liens avec les autres puisqu'on supprime toute la famille
                #self.remove_people(k)

    def keep_one_family(self,famID):
        """
        Remove all the families in the Pedigree except famID
        """
        for k,v in list(self._pedigree.items()):
            if v.famID != famID:
                del self._pedigree[k] # Pas besoin de faire attention aux liens avec les autres puisqu'on supprime toute la famille
                #self.remove_people(k)

    def family_number_members(self)->dict():
        """
        return a dictionary where keys = famID and values = Number of family members
        """
        dom = self.domain()
        fam_nb = dict()
        for d in dom:
            fam_nb[d] = 0
        for k, v in self._pedigree.items():
            fam_nb[v.famID]+=1
        return fam_nb

    def old_generation(self,pID,nbG):
        """
        Return a list of list that contains each previous generation of pID, from parents (1st gen) to nbG gen
        """
        if nbG == 1:
            parents = self.parents(pID)
            return [parents[0],parents[1]]
        else:
            parents = self.parents(pID)
            return [self.old_generation(i,nbG-1) for i in parents]
            # father,mother = self.parents(pID)
            # print("pere",father,"mere",mother)
            # return [father,mother] + self.old_generation(str(father),nbG-1)
            # return [father,mother] + self.old_generation(str(mother),nbG-1)

    def next_generation(self,pID,nbG):
        """
        Return a list of list that contains each next generation of pID, from children (1st gen) to nbG gen
        """
        if nbG == 1:
            return  list(self.get_people(pID).child)
        else:
            children = self.get_people(pID).child
            return [list(children) + self.next_generation(i,nbG-1) for i in children]

    #Pas du tout sur du fonctionnement de ces deux fonctions generation
    #Plus complexe en pratique qu'il n'y parait, pas sur de l'utilité de ces fonctions 

    def __str__(self):
        return ", ".join([str(v) for k,v in self._pedigree.items()])

    def graph(self,name):
        """
        Return a graph showing the Pedigree
        """
        graph = Graph(name='Pedigree',strict=True,comment=name)
        graph.attr(label=r'\n\n'+name+' pedigree')
        for k,v in self._pedigree.items():
            if v.fatID != '0':
                graph.edge(v.pID,v.fatID)
            if v.matID != '0':
                graph.edge(v.pID,v.matID)
            if len(v.child) > 0:
                for i in v.child:
                    graph.edge(v.pID,i)
        graph.save(filename=name,directory="../data")
        graph.view()