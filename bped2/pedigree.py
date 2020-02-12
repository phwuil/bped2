#!/usr/local/bin/python
import pickle as pkl


class Pedigree:
    def __init__(self):
        self._pedigree = dict()
        self._nb = 0

    def getPedigree(self):
        """
        Return the Pedigree
        """
        return self._pedigree

    def getNB(self):
        """
        Return the People's number in the pedigree
        """
        return self._nb

    def getPeople(self,idp):
        """
        Return the People with the key = idp
        """
        return self._pedigree[idp]

    def load(self, fichier):
        """
        Read a .ped file and
        Return a dictionary where the keys are the people's IDs and the values are the People
        """
        for i in open(fichier).readlines():
            tmp = i.strip().split()
            p = People(tmp[0],tmp[1],tmp[2],tmp[3])
            #print(p)
            self._pedigree[tmp[1]] = p
        self._nb = len(self._pedigree)

    def sex(self):
        """
        Modify the "sex value" if possible, due to fatID and MatID knowlege's
        0 = unidentify
        1 = Male
        2 = Female
        """
        father = set()
        mother = set()
        for k,v in self._pedigree.items():
            if v._fatID != '0':
                father.add(v._fatID)
            if v._matID != '0':
                mother.add(v._matID)
        for f,m in zip(father,mother):
            self._pedigree[str(f)]._sex = 1
            self._pedigree[str(m)]._sex = 2

    def add_children_all(self):
        """
        Complete the child attribute for all the pedigree's people
        """
        for k, v in self._pedigree.items():
            father = v._fatID #v[2] fatID
            mother = v._matID #v[3] matID
            if father != '0' and self._pedigree[father] is not None:
                self._pedigree[father].child.add(k)
            if mother != '0' and self._pedigree[mother] is not None:
                self._pedigree[mother].child.add(k)

    def add_children(self,people):
        """
        Fill the child parameter, due to fatID and MatID knowlege's
        """
        father = people._fatID
        mother = people._matID
        if father != '0' and self._pedigree[father] is not None:
            self._pedigree[father][4].add(people._pID) # 4 pour le parametre child
        if mother != '0' and self._pedigree[mother] is not None:
            self._pedigree[mother][4].add(people._pID) # 4 pour le parametre child


    def pedigreeToFile(self):
        return

    def addPeople(self,people):
        self._pedigree[people._pID] = people
        #self.add_children(people)
        self._nb = len(self._pedigree)

    def removePeople(self,idp):
        #Cas où le People n'a ni enfants, ni parents
        if len(self._pedigree[idp]._child) == '0' and self._pedigree[idp]._fatID == '0' and self._pedigree[idp]._matID == '0':
            del self._pedigree[idp] #Suppression direct

        #Cas où le People n'a pas d'enfants mais ses parents sont connus
        elif len(self._pedigree[idp]._child) == '0' and self._pedigree[idp]._fatID != '0' and self._pedigree[idp]._matID != '0':
            father = self._pedigree[idp]._fatID
            mother = self._pedigree[idp]._matID
            if father != 0 and self._pedigree[father] is not None:
                self._pedigree[father][4].remove(idp)  # 4 pour le parametre child
            if mother != 0 and self._pedigree[mother] is not None:
                self._pedigree[mother][4].remove(idp)  # 4 pour le parametre child

        # Cas où le People n'a pas de parents connus mais a des enfants
        elif len(self._pedigree[idp]._child) != '0' and self._pedigree[idp]._fatID == '0' and self._pedigree[idp]._matID == '0':
            for id in self._pedigree[idp]._child:
                if self._pedigree[idp]._sex == '1':
                    self._pedigree[id]._sex = 0
                if self._pedigree[idp]._sex == '2':
                    self._pedigree[id]._sex = 0
        #Cas où le People a des parents ET des enfants
        else:
            father = self._pedigree[idp]._fatID
            mother = self._pedigree[idp]._matID
            if father != 0 and self._pedigree[father] is not None:
                self._pedigree[father][4].remove(idp)  # 4 pour le parametre child
            if mother != 0 and self._pedigree[mother] is not None:
                self._pedigree[mother][4].remove(idp)  # 4 pour le parametre child

            for id in self._pedigree[idp]._child:
                if self._pedigree[idp]._sex == '1':
                    self._pedigree[id]._sex = 0
                if self._pedigree[idp]._sex == '2':
                    self._pedigree[id]._sex = 0

    def roots(self):
        roots = {}
        for k,v in self._pedigree.keys():
            if v[2] == '0' and v[3] == '0': # Si l'individu n'a pas de parents -> Racine
                roots.add(v[1])
        return roots

    def leaves(self):
        leaves = {}
        for k,v in self._pedigree.keys():
            if len(v[4]) == 0: # Si l'individu n'a pas d'enfants -> Feuille
                leaves.add(v[1])
        return leaves

    def domain(self):
        dom = set()
        for k,v in self._pedigree.keys():
            dom.add(v[0])
        return dom



    def __str__(self):
        return ", ".join([str(v) for k,v in self._pedigree.items()])

class People:
    def __init__(self,famID,pID,fatID,matID,sex=0):
        self._famID = famID
        self._pID = pID
        self._fatID = fatID
        self._matID = matID
        self._sex = sex
        self._child = set()

    @property
    def famID(self):
    #def get_famID(self):
        return self._famID
    @famID.setter
    def famID(self,famID):
        #self._famID=famID
        raise NameError("Cannot change FamID")

    @property
    def pID(self):
        return self._pID

    @pID.setter
    def pID(self,pid):
        raise NameError("Cannot change pid")

    @property
    def fatID(self):
        return self._fatID

    @fatID.setter
    def fatID(self,fatID):
        raise NameError("Cannot change FatID")

    @property
    def matID(self):
        return self._matID

    @matID.setter
    def matID(self,matID):
        raise NameError("Cannot change matID")

    @property
    def sex(self):
        return self._sex

    @sex.setter
    def sex(self,sex):
        self.sex = sex

    @property
    def child(self):
        return self._child


    def __str__(self):
        #return "[%s %s %s %s %s]"%(self._famID,self.pID,self.famID,self.famID,self.sex)
        return f"[{self._famID} {self._pID} {self._fatID} {self._famID} {self._sex} {self._child}]"

    # pid = property(get_pID,set_pID)
    # fatID = property(get_fatID,set_fatID)
    # famID = property(get_famID,set_famID)
    # sex = property(get_sex,set_sex)