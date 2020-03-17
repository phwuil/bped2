#!/usr/local/bin/python
from typing import Set
import pydotplus as pydot
import matplotlib.pyplot as plt
import random
import pyAgrum as gum
import pyAgrum.lib.notebook as gnb

class People:
    def __init__(self, famID: str, pID: str, fatID: str, matID: str):
        self._famID = famID
        self._pID = pID
        self._fatID = fatID
        self._matID = matID
        self._sex = 0
        self._child = set()

    def __eq__(self, other):
        return (self.famID == other.famID) and (self.pID == other.pID) and (self.fatID == other.fatID) \
               and (self.matID == other.matID) and (self.sex == other.sex) and (self.child == other.child)

    def _set(self, famID, fatID, matID):
        self._famID = famID
        self._fatID = fatID
        self._matID = matID

    @property
    def famID(self) -> str:
        # def get_famID(self):
        return self._famID

    @famID.setter
    def famID(self, famID) -> str:
        # self._famID=famID
        raise NameError("Cannot change FamID")

    @property
    def pID(self) -> str:
        return self._pID

    @pID.setter
    def pID(self, pid) -> str:
        raise NameError("Cannot change pid")

    @property
    def fatID(self) -> str:
        return self._fatID

    @fatID.setter
    def fatID(self, fatID) -> str:
        raise NameError("Cannot change FatID")

    @property
    def matID(self) -> str:
        return self._matID

    @matID.setter
    def matID(self, matID):
        raise NameError("Cannot change matID")

    @property
    def sex(self) -> int:
        return self._sex

    @sex.setter
    def sex(self, sex):
        self._sex = sex

    @property
    def child(self):
        return self._child.copy()

    def nbrChild(self):
        return len(self._child)

    @child.setter
    def child(self):
        raise NameError("Cannot change child")

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
    sex_undefined = 0
    sex_male = 1
    sex_female = 2
    sex_malefemale = 3

    people_unknown = "?"
    no_people = "0"

    def __init__(self):
        self._pedigree = dict()
        self._people2line = dict()

    def __str__(self):
        return ", ".join([str(v) for k, v in self._pedigree.items()])

    def __len__(self):
        """
        Return the People's number in the pedigree
        """
        return len(self.get_pedigree())

    def __eq__(self, other):
        if len(self._pedigree) != len(other._pedigree):
            return False

        for i, j in zip(self._pedigree.values(), other._pedigree.values()):
            if i != j:
                return False
        return True

    def get_pedigree(self):
        """
        Return the Pedigree
        """
        return self._pedigree.copy()

    def get_people(self, idp: str) -> People:
        """
        Return the People with the key = idp
        """
        if idp not in self._pedigree.keys():
            raise ValueError(f"ID: {idp} is not in the pedigree")
        return self._pedigree[idp]

    def get_line(self, idPeople):
        """
        return the line of the file where the people has been defined
        """
        return self._people2line[idPeople]

    def load(self, fichier):
        """
        Read a .ped file and
        Return a dictionary where the keys are the people's IDs and the values are the People
        """
        with open(fichier, "r") as file:
            for (line, i) in enumerate(file.readlines()):
                p = People(*i.strip().split())
                self.add_people(*i.strip().split())
                self._people2line[p.pID] = line

    def save(self, filename):
        """
        Save the current Pedigree in a file : filename.ped
        """
        with open(filename, "w") as f:
            for i in self._pedigree.values():
                f.write(f"{i._famID}\t{i._pID}\t{i._fatID}\t{i._matID}\n")

    def add_sex(self, pID: str, sex: int):
        """
        Modify the "sex value" for people 'pId'
        sex_undefined = unidentify / 0
        sex_male = Male / 1
        sex_female = Female /  2
        sex_malefemale = Male AND Female (why not) / 3
        """
        # check if sex already filled
        p = self.get_people(pID)
        if p.sex == self.sex_undefined:
            p.sex = sex
        elif p.sex != sex:
            p.sex = self.sex_malefemale

    def add_sex_all(self):
        """
        Modify the "sex value" for all people if possible, due to fatID and MatID knowlege's
        """
        for k, v in self._pedigree.items():
            if v.fatID != self.no_people:
                self.add_sex(v.fatID, self.sex_male)
            if v.matID != self.no_people:
                self.add_sex(v.matID, self.sex_female)

    def update_children(self, pID):
        """
        Fill the child parameter, due to fatID and MatID knowlege's
        """
        father = self.get_people(pID).fatID
        mother = self.get_people(pID).matID
        if father in self._pedigree:
            self._pedigree[father].add_children(pID)
        if mother in self._pedigree:
            self._pedigree[mother].add_children(pID)

    def update_children_all(self):
        """
        Complete the child attribute for all the pedigree's people
        """
        for k in self._pedigree.keys():
            self.update_children(k)

    def update_parents(self, pID):
        """
        Fill the fatID and matID if possible due to param child of the people
        """
        people = self.get_people(pID)
        if people.nbrChild() != 0 and people.sex != 0:  # S'il a au moins un enfant et un sexe connu
            for i in people.child:
                # print(self.get_people(i).fatID)
                if self.get_people(i).fatID == self.no_people and people.sex == 1:
                    self.get_people(i)._fatID = people.pID
                if self.get_people(i).matID == self.no_people and people.sex == 2:
                    self.get_people(i)._matID = people.pID

    def update_parents_all(self):
        """
        Complete the fat/fam attribute for all the pedigree's people
        """
        for k, v in self._pedigree.items():
            self.update_parents(k)

    def add_people(self, famID, pID, fatID, matID):

        if pID == self.no_people:
            raise ValueError(f'id {self.no_people} is not allowed for people')

        if famID == self.people_unknown:
            raise ValueError(f'Cannot add a people with famID = {self.people_unknow}')

        if pID in self._pedigree.keys():
            if self.get_people(pID).famID != self.people_unknown:
                raise ValueError(f'{pID} already use for another people')
            self.get_people(pID)._set(famID, fatID, matID)

        else:
            people = People(famID, pID, fatID, matID)
            self._pedigree[pID] = people
            self.update_children(pID)

    def remove_people(self, idp: str):
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
            ch = self.get_people(chid)
            if ch.fatID == idp:
                ch._fatID = self.no_people
            if ch.matID == idp:
                ch._matID = self.no_people

        del self._pedigree[idp]

    def remove_singleton(self):
        """
        If a people doesn't have any parents and childrens, remove him from the pedigree
        """
        for f, v in list(self._pedigree.items()):
            if v.fatID == self.no_people and v.matID == self.no_people and v.nbrChild() == 0:
                self.remove_people(v.pID)

    def roots(self):
        """
        Return the olders, people without knowned parents
        """
        for k, v in self._pedigree.items():
            if v.fatID == self.no_people and v.matID == self.no_people:  # Si l'individu n'a pas de parents -> Racine
                yield v.pID

    def leaves(self):
        """
        People without childrens are leaves
        """
        for k, v in self._pedigree.items():
            if v.nbrChild() == 0:  # Si l'individu n'a pas d'enfants -> Feuille
                yield v.pID

    def get_domain(self):
        """
        Return all the different family present in the pedigree
        """
        dom = set()
        for k, v in self._pedigree.items():
            dom.add(v.famID)
        return dom

    def get_bro_sis(self, pID):
        """
        Return brothers and sister of a People, without step family
        """
        father = self.get_people(pID).fatID
        mother = self.get_people(pID).matID
        if father != self.no_people or mother != self.no_people:  # Au moins 1 des parents est connu
            bros = self.get_people(father).child.intersection(self.get_people(mother).child)
            bros.remove(pID)
        else:
            bros = set()
        return bros

    def get_male(self):
        """
        Return knowed people with male sex
        """
        male = set()
        for v in self._pedigree.values():
            if v.sex == 1:
                male.add(v.pID)
        return male

    def get_female(self):
        """
        Return knowed people with female sex
        """
        female = set()
        for v in self._pedigree.values():
            if v.sex == 2:
                female.add(v.pID)
        return female

    def get_step_bro_sis(self, pID):
        """
        Do the symmetric difference (new set with elements in either father's child or mother's child but not both)

        """
        father = self.get_people(pID).fatID
        mother = self.get_people(pID).matID
        step_bros = self.get_people(father).child.symmetric_difference(self.get_people(mother).child)
        step_bros.remove(pID)
        return step_bros

    def get_uncles_aunts(self, pID) -> set:
        """
        Return the uncles and aunts of a individu
        """
        father, mother = self.get_parents(pID)
        return self.get_bro_sis(father).union(self.get_bro_sis(mother))

    def get_cousins(self, pID):
        """
        Return the cousins of an individu
        """
        people = set()
        uncles_aunts = self.get_uncles_aunts(pID)
        for i in uncles_aunts:
            for j in self.get_people(i).child:  #  Pas opti mais je vois pas comment faire autrement
                people.add(j)
        return people

    def get_parents(self, pID):
        """
        Return a set of the parents
        """
        s = set()
        if self.get_people(pID).matID != self.no_people:
            s.add(self.get_people(pID).matID)

        if self.get_people(pID).fatID != self.no_people:
            s.add(self.get_people(pID).fatID)

        return s

    def get_grand_parents(self, pID):  # Probablement inutile
        """
        return a set of paternal and mather grandparents
        """
        grand_parents = set()
        parents = self.get_parents(pID)
        for i in parents:
            grand_parents.update(self.get_parents(i))
        return grand_parents

    def get_couple(self):
        couple = set()
        for k,v in self._pedigree.items():
            if len(self.get_parents(v.pID))>1:
                couple.add((v.fatID,v.matID))
        return couple

    def remove_family(self, famID):
        """
        Remove an entire family in the Pedigree
        """
        for k, v in list(self._pedigree.items()):
            if v.famID == famID:
                # Pas besoin de faire attention aux liens avec les autres puisqu'on supprime toute la famille
                del self._pedigree[k]
                # self.remove_people(k)

    def gen_family_pedigree(self, famID):
        """
        Return a new Pedigree with only the family famID
        """
        ped = Pedigree()
        for k, v in list(self._pedigree.items()):
            if v.famID == famID:
                ped.add_people(v.famID, v.pID, v.fatID, v.matID)
        return ped

    def gen_all_pedigree(self):
        """
        Return a dictionary where the key is a famID and the value is a new Pedigree with only the family famID
        """
        ped = dict()
        dom = self.get_domain()
        for i in dom:
            ped[i] = self.gen_family_pedigree(i)
        return ped

    def get_stat_family(self) -> dict():
        """
        return a dictionary where keys = famID and values = Number of family members
        """
        dom = self.get_domain()
        fam_nb = dict()
        for d in dom:
            fam_nb[d] = 0
        for k, v in self._pedigree.items():
            fam_nb[v.famID] += 1
        return fam_nb

    def old_gen(self, pID, nbG) -> set:
        """
        Return a list of list that contains each previous generation of pID, from parents (1st gen) to nbG gen
        """
        if nbG == 1:
            return self.get_parents(pID)
        else:
            cpt = 1
            gen = set()
            while cpt <= nbG:
                if len(gen) == 0:
                    gen.update(self.get_parents(pID))
                else:
                    tmp = set()
                    for i in gen:
                        tmp.update(self.get_parents(i))
                    gen.update(tmp)
                cpt += 1
            return gen

    def next_gen(self, pID, nbG) -> set:
        """
        Return a list of list that contains each next generation of pID, from children (1st gen) to nbG gen
        """
        if nbG == 1:
            return self.get_people(pID).child
        else:
            cpt = 1
            children = set()
            while cpt <= nbG:
                tmp = set()
                if len(children) == 0:
                    children.update(self.get_people(pID).child)
                else:
                    for i in children:
                        tmp.update(self.get_people(i).child)
                    children.update(tmp)
                cpt += 1
            return children

    def check_one_people_family(self):
        """
        Return the family's number with just one people
        """
        dico = self.get_stat_family()
        cpt = 0
        for v in self._pedigree.values():
            if dico[v.famID] == 1:
                cpt += 1
        return cpt

    def check_mother_and_father(self):
        """
        Check for all people in the pedigree, if someone is a mother and also a father
        """
        father = set()
        mother = set()
        for v in self._pedigree.values():
            father.add(v.fatID)
            mother.add(v.matID)
        return father.intersection(mother)

    def check_consanguinity(self, pID, nbG):  # Peut etre le faire sur une famille entiere et non sur un unique individu
        """
        Check if a people has consanguinous origin by checking in the nbG older generation
        """
        parents = self.get_parents(pID)
        if len(parents) == 2:
            parent1, parent2 = self.get_parents(pID)
        elif len(parents) == 1:
            parent1 = parents
            parents = self.no_people
        else:
            return {}

        holders1 = set()
        holders2 = set()
        if parent1 != self.no_people and parent2 != self.no_people:
            holders1 = self.old_gen(parent1, nbG)
            holders2 = self.old_gen(parent2, nbG)
        elif parent1 != 0 and parent2 == self.no_people:
            holders1 = self.old_gen(parent1, nbG)
        else:
            holders2 = self.old_gen(parent2, nbG)
        return holders1.intersection(holders2)

    def check_consanguinity_family(self, famID):
        fam = self.gen_family_pedigree(famID)
        res = set()
        for v in fam._pedigree.values():
            res.update(self.check_consanguinity(v.pID, 10))
        return res

    def check_consanguinity_pedigree(self):
        dom = self.get_domain()
        res = set()
        for i in dom:
            res.update(self.check_consanguinity_family(i))
        return res

    def is_consanguineous(self, p1, p2, nbG):
        """
        In the case where p1 and p2 are supposed to have children, we check their olders
        Return True if p1 and p2 had common olders, else return False
        """
        holders_p1 = set(self.old_gen(p1, nbG))
        holders_p2 = set(self.old_gen(p2, nbG))
        x = holders_p1.intersection(holders_p2)
        return len(x) != 0

    def check_famID(self, pID):
        """
        Check if people link to the people pID have a different famID
        """
        ref = self.get_people(pID).famID
        errors = set()
        for k, v in self._pedigree.items():
            if v.famID != ref:
                errors.add(k)
        return errors

    def pedigree_overview_file(self, filename):

        with open("../data/ped/" + filename, "w") as f:
            for k, v in self._people2line.items():
                f.write(f"People {k} is defined at line {v}\n")
            stats = self.get_stat_family()
            f.write("---------------------------------------------------\n")
            for k, v in stats.items():
                f.write(f"The Family {k} is composed by {v} members \n")
            f.write("---------------------------------------------------\n")
            f.write(f"Out of  {len(stats)} families, there are {self.check_one_people_family()} composed by one people\n")
            f.write(
                f"In the pedigree, this people appear as mother and also as father : {self.check_mother_and_father()}\n")
            f.write(
                f"In the pedigree, this people had consangineous origins : {self.check_consanguinity_pedigree()}\n")

    def graph(self, name, bool):
        """
        DoubleCircle = Roots
        Box = leaves
        Diamond = Nodes
        """
        col_rac_fill = {self.sex_undefined: "#C2F732", #Green
                       self.sex_male: "#00ffff", #Cyan
                       self.sex_female: "#ff009c", #Pink
                       self.sex_malefemale: "#000000"} #Dark

        shape_nodes = {False:['circle','box','diamond'],True:['point','point','point']}

        roots = {i for i in self.roots()}
        leaves = {i for i in self.leaves()}
        graph = pydot.Dot(graph_type='digraph', graph_name=name, strict=True)
        for k, v in self._pedigree.items():

            if v.pID in roots:
                graph.add_node(pydot.Node(k, shape=shape_nodes[bool][0], style="filled", color=col_rac_fill[v.sex]))

            elif v.pID in leaves:
                graph.add_node(pydot.Node(k, shape=shape_nodes[bool][1], style="filled", color=col_rac_fill[v.sex]))

            else:
                graph.add_node(pydot.Node(k, shape=shape_nodes[bool][2], style="filled", color=col_rac_fill[v.sex]))

        node = -1
        for f,m in self.get_couple():
            current_node = node
            graph.add_node(pydot.Node(current_node, shape='point'))
            graph.add_edge(pydot.Edge(f, current_node,color='blue'))
            graph.add_edge(pydot.Edge(m, current_node,color='pink'))
            node -= 1
            for c in self.get_people(f).child.intersection(self.get_people(m).child):
                edge = pydot.Edge(current_node, c)
                graph.add_edge(edge)
        graph.write_png("../data/graph/" + name + '.pdf')

    def generation_ped(self, famID, nbDepart, nbGeneration):
        """
        Return a new pedigree, start with a number nbDepart of people and create nbGeneration
        """
        nbChildMax = 4  # Nombres d'enfants max que l'on peut avoir
        pMariage = 0.8  # Probabilité d'effectuer un mariage entre deux peoples
        pConsanguinity = 0.5  # Probabilité d'effectuer un mariage entre people d'une même lignée
        global currentID
        currentID = 1

        def first_generation(currentID):
            for p in range(nbDepart):
                self.add_people(famID, str(currentID), self.no_people, self.no_people)
                currentID += 1

            mariage = {i for i in self.leaves()}

            while len(mariage) > 1:
                p1, p2 = random.sample(mariage, 2)  # On choisi 2 personnes au hasard
                mariage.remove(p1)
                mariage.remove(p2)
                child = random.randint(1, nbChildMax)
                # Ajout des enfants
                for c in range(child):
                    self.add_people(famID, str(currentID), p1, p2)
                    self.update_children(str(currentID))
                    currentID += 1
                self.add_sex(p1, 1)
                self.add_sex(p2, 2)
            return currentID

        def mariage_2p_exist(currentID,mariage):
            if len(mariage) > 1:
                p1, p2 = random.sample(mariage, 2)
                bool = self.is_consanguineous(p1, p2, n)
                if bool:
                    if random.random() < pConsanguinity:
                        child = random.randint(1, nbChildMax)
                        # Ajout des enfants
                        for c in range(child):
                            self.add_people(famID, str(currentID), p1, p2)
                            self.update_children(str(currentID))
                            currentID += 1
                        self.add_sex(p1, 1)
                        self.add_sex(p2, 2)
                        mariage.remove(p1)
                        mariage.remove(p2)
                    else:
                        pass
                else:  # Mariage normal entre deux personnes déja présente dans le pedigree
                    child = random.randint(1, nbChildMax)
                    # Ajout des enfants
                    for c in range(child):
                        self.add_people(famID, str(currentID), p1, p2)
                        self.update_children(str(currentID))
                        currentID += 1
                    self.add_sex(p1, 1)
                    self.add_sex(p2, 2)
                    mariage.remove(p1)
                    mariage.remove(p2)
            return currentID

        def mariage_1p_exist(currentID,mariage):
            if len(mariage) > 0:
                p1 = random.sample(mariage, 1)[0]
                sex = random.random()
                child = random.randint(1, nbChildMax)
                p2 = str(currentID)
                self.add_people(famID, p2, self.no_people, self.no_people)
                mariage.add(p2)
                currentID += 1
                if sex < 0.5:  # On crée un homme
                    for i in range(child):
                        self.add_people(famID, str(currentID), p2, p1)
                        self.update_children(str(currentID))
                        currentID += 1
                    self.add_sex(p2, 1)
                    self.add_sex(p1, 2)
                    mariage.remove(p1)
                    mariage.remove(p2)
                else:  # On crée une femme
                    for i in range(child):
                        self.add_people(famID, str(currentID), p1, p2)
                        self.update_children(str(currentID))
                        currentID += 1
                    self.add_sex(str(p1), 1)
                    self.add_sex(str(p2), 2)
                    mariage.remove(p1)
                    mariage.remove(p2)
            return currentID

        currentID = first_generation(currentID)
        for n in range(1,nbGeneration):
            mariage = {i for i in self.leaves()}
            while random.random() < pMariage:
                if random.random() < 0.5:
                    currentID = mariage_2p_exist(currentID,mariage)
                else:
                    currentID = mariage_1p_exist(currentID,mariage)

    def new_gen_ped(self,famID, nbP, nbDepart, nbG , nbChildMax = 4, consanguinity = 4):
        """
        Return a new pedigree, start with a number nbDepart of people and create nbGeneration
        """
        pMariage = 0.8  # Probabilité d'effectuer un mariage entre deux peoples
        pConsanguinity = 0.5  # Probabilité d'effectuer un mariage entre people d'une même lignée
        currentID = 1
        for p in range(nbDepart):
            self.add_people(famID, str(currentID), self.no_people, self.no_people)
            currentID += 1

        mariage = {i for i in self.leaves()}

        while len(mariage) > 1:
            p1, p2 = random.sample(mariage, 2)  # On choisi 2 personnes au hasard
            mariage.remove(p1)
            mariage.remove(p2)
            child = random.randint(1, nbChildMax)
            # Ajout des enfants
            for c in range(child):
                if currentID > nbP:
                    return
                self.add_people(famID, str(currentID), p1, p2)
                self.update_children(str(currentID))
                currentID += 1
            self.add_sex(p1, 1)
            self.add_sex(p2, 2)
            if currentID > nbP:
                return

    ## Fin 1ere generation

        for i in range(2,nbG):
            mariage = {i for i in self.leaves()}
            alea = random.random()
            if alea < 0.5:
                if len(mariage) > 1:
                    p1, p2 = random.sample(mariage, 2)
                    bool = self.is_consanguineous(p1, p2, consanguinity)
                    if bool:
                        if random.random() < pConsanguinity:
                            child = random.randint(1, nbChildMax)
                            # Ajout des enfants
                            for c in range(child):
                                if currentID > nbP :
                                    return
                                else:
                                    self.add_people(famID, str(currentID), p1, p2)
                                    self.update_children(str(currentID))
                                    currentID += 1

                            self.add_sex(p1, 1)
                            self.add_sex(p2, 2)
                            if currentID > nbP:
                                return
                            mariage.remove(p1)
                            mariage.remove(p2)
                        else:
                            pass
                    else:  # Mariage normal entre deux personnes déja présente dans le pedigree
                        child = random.randint(1, nbChildMax)
                        # Ajout des enfants
                        for c in range(child):
                            if currentID > nbP:
                                return
                            else:
                                self.add_people(famID, str(currentID), p1, p2)
                                self.update_children(str(currentID))
                                currentID += 1

                        self.add_sex(p1, 1)
                        self.add_sex(p2, 2)
                        if currentID > nbP:
                            return
                        mariage.remove(p1)
                        mariage.remove(p2)

            else:
                if len(mariage) > 0:
                    p1 = random.sample(mariage, 1)[0]
                    sex = random.random()
                    child = random.randint(1, nbChildMax)
                    p2 = str(currentID)
                    if currentID > nbP:
                        return
                    else:
                        self.add_people(famID, p2, self.no_people, self.no_people)
                        mariage.add(p2)
                        currentID += 1
                        if currentID > nbP:
                            return
                        if sex < 0.5:  # On crée un homme
                            for c in range(child):
                                if currentID > nbP :
                                    return
                                else:
                                    self.add_people(famID, str(currentID), p2, p1)
                                    self.update_children(str(currentID))
                                    currentID += 1

                            self.add_sex(p2, 1)
                            self.add_sex(p1, 2)
                            if currentID > nbP:
                                return
                            mariage.remove(p1)
                            mariage.remove(p2)
                        else:  # On crée une femme
                            for c in range(child):
                                if currentID > nbP :
                                    return
                                else:
                                    self.add_people(famID, str(currentID), p1, p2)
                                    self.update_children(str(currentID))
                                    currentID += 1

                            self.add_sex(str(p1), 1)
                            self.add_sex(str(p2), 2)
                            if currentID > nbP:
                                return
                            mariage.remove(p1)
                            mariage.remove(p2)

    def gen_ped(self, famID, nb, g_max, c_max, cl):
        """

        """

        def waiting_wedding(famID, mea, people, sex):
            self.add_people(famID, people, self.no_people, self.no_people)
            profondeur[people] = profondeur[mea[0]]
            if self.get_people(people).sex == self.sex_male:
                if families.get((people,mea[0])) == None:
                    families[(people, mea[0])] = []
                    families[(people, mea[0])].append(mea[1])
                    self.get_people(mea[1])._set(famID, people, mea[0])
                else:
                    families[(people, mea[   0])].append(mea[1])
                    self.get_people(mea[1])._set(famID, people, mea[0])
            else:
                if families.get((mea[0],people)) == None:
                    families[(mea[0],people)] = []
                    families[(mea[0],people)].append(mea[1])
                    self.get_people(mea[1])._set(famID, mea[0], people)
                else:
                    families[(mea[0],people)].append(mea[1])
                    self.get_people(mea[1])._set(famID, mea[0], people)

            self.add_sex(people, sex)
            self.get_people(people).add_children(mea[1])
            #self.update_parents(mea[1])
            mea.clear()

        def create_wedding(famID, people1, people2, child, sex):
            self.add_people(famID, people1, self.no_people, self.no_people)
            profondeur[people1] = profondeur[child] - 1
            self.get_people(people1).add_children(child)
            self.get_people(people2).add_children(child)
            self.add_sex(people1, sex)
            #self.update_parents(child)
            if sex == self.sex_male:
                families[(people1,people2)].append(child)
                self.get_people(child)._set(famID, people1, people2)
            else:
                families[(people2,people1)].append(child)
                self.get_people(child)._set(famID, people2, people1)

        gamma = 0.6
        mea = []
        profondeur = dict()
        families = dict()

        for i in range(1,nb+1):
            profondeur[str(i)] = -1
            #families[str(i)] = dict() #Structure pas encore determiner

        self.add_people(famID, '1', self.no_people, self.no_people)
        profondeur['1'] = 0

        for p in range(2,nb+1):
            new_p = str(p)
            if len(mea) > 0:
                if self.get_people(mea[0]).sex == self.sex_male:
                    #Ajout de la mere
                    waiting_wedding(famID, mea, new_p, 2)
                    continue
                else:
                    #Ajout du pere
                    waiting_wedding(famID, mea, new_p, 1)
                    continue


            child_pot = [i for i in self.roots() if profondeur[i] > 0 ]
            parents_pot = []
            for k,v in self._pedigree.items():
                if v.nbrChild() < c_max and profondeur[k] < g_max and profondeur[k] > -1:
                    parents_pot.append(k)

            k1 = len(child_pot)
            k2 = len(parents_pot)
            choice = random.random()
            parent = random.sample(parents_pot, 1)[0]
            if choice > k1/(k1+k2):
                #Nouvel enfant

                sex = self.get_people(parent).sex
                couple = []
                for p1,p2 in families.keys():
                    if p1 == parent or p2 == parent:
                        couple.append((p1,p2))

                if couple == []:
                    if random.random() < 0.5:
                        self.add_people(famID, new_p, parent, self.no_people)
                        profondeur[new_p] = profondeur[parent] + 1
                        self.get_people(parent).add_children(new_p)
                        #self.update_parents(new_p)
                        self.add_sex(parent,1)
                        mea.extend([parent, new_p])

                    else:
                        self.add_people(famID, new_p, self.no_people, parent)
                        profondeur[new_p] = profondeur[parent] + 1
                        self.get_people(parent).add_children(new_p)
                        #self.update_parents(new_p)
                        self.add_sex(parent, 2)
                        mea.extend([parent, new_p])

                else:
                    tmp = []
                    keys = []
                    for k,v in families.items():
                        if k in couple :
                            tmp.append(gamma*len(v))
                            keys.append(k)
                    index = tmp.index(min(tmp))
                    families[keys[index]].append(new_p)
                    self.add_people(famID, new_p, keys[index][0], keys[index][1])
                    self.get_people(keys[index][0]).add_children(new_p)
                    self.get_people(keys[index][1]).add_children(new_p)
                    self.get_people(new_p)._set(famID, keys[index][0], keys[index][1])


            else:
                #Nouveau Parent
                child = random.sample(child_pot,1)[0]
                conjoint = [k for k in self._pedigree.keys() if profondeur[k] == profondeur[new_p] -1 ]
                alea = random.randint(0,len(conjoint))
                if alea == 0:
                    if random.random() < 0.5:
                        self.add_people(famID, new_p, self.no_people, self.no_people)
                        profondeur[new_p] = profondeur[child] - 1
                        self.get_people(new_p).add_children(child)
                        #self.update_parents(child)
                        self.add_sex(new_p,1)
                        mea.extend([new_p, child])
                    else:
                        self.add_people(famID, new_p, self.no_people, self.no_people)
                        profondeur[new_p] = profondeur[child] - 1
                        self.get_people(new_p).add_children(child)
                        #self.update_parents(child)
                        self.add_sex(new_p, 2)
                        mea.extend([new_p, child])
                else:
                    other_p = random.sample(conjoint,1)[0]
                    while child == other_p and self.is_consanguineous(new_p,other_p,cl) is True:
                        other_p = random.sample(conjoint, 1)[0]
                    if self.get_people(other_p).sex == self.no_people:
                        self.add_people(famID, new_p, self.no_people, self.no_people)
                        profondeur[new_p] = profondeur[child] - 1
                        self.get_people(new_p).add_children(child)
                        self.get_people(other_p).add_children(child)
                        self.add_sex(new_p,1)
                        self.add_sex(other_p,2)
                        #self.update_parents(child)
                        self.get_people(child)._set(famID, new_p, other_p)
                        families[(new_p,other_p)].append(child)


                    elif self.get_people(other_p).sex == self.sex_male:
                        create_wedding(famID, new_p, other_p, child, 2)

                    else:
                        create_wedding(famID, new_p, other_p, child, 1)




### ---------------------------------------------------------------------------
    def create_holders(self,bn, p):
        """
        Create 3 nodes, fatXi, matXi and Xi and link fatXi and matXi to Xi
        """
        bn.add(gum.LabelizedVariable(f"matX{p.pID}", f"mother of {p.pID}", ["0", "1"]))
        bn.add(gum.LabelizedVariable(f"fatX{p.pID}", f"father of {p.pID}", ["0", "1"]))
        bn.add(gum.LabelizedVariable(f"X{p.pID}", f"{p.pID}", ["00", "01", "10", "11"]))
        bn.addArc(f"fatX{p.pID}", f"X{p.pID}")
        bn.addArc(f"matX{p.pID}", f"X{p.pID}")
        bn.cpt(f"X{p.pID}").fillWith([1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1])

    def create_offsprings(self, bn, p, parent):
        """
        Create link between a parent and his children
        """

        # parent = fat ou mat
        if parent == 'fat':
            parentID = p.fatID
        else:
            parentID = p.matID

        # Creating Selector
        bn.add(gum.LabelizedVariable(f"S{parent}{p.pID}", f"Selector of {parent}ID", ["mat", "fat"]))
        bn.cpt(f"S{parent}{p.pID}").fillWith([0.5, 0.5])

        bn.addArc(f"fatX{parentID}", f"{parent}X{p.pID}") # fatXi to Child
        bn.addArc(f"matX{parentID}", f"{parent}X{p.pID}") # matXi to Child
        bn.addArc(f"S{parent}{p.pID}", f"{parent}X{p.pID}")  # Selector to fat/mat


        bn.cpt(f"{parent}X{p.pID}").fillWith([1, 0, 1, 0, 0, 1, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1])

    def ped_to_bn(self, f):
        bn = gum.BayesNet()
        for p in self.get_pedigree().values():
            self.create_holders(bn, p)

            if p.fatID == '0':  # Cas parents inconnu
                bn.cpt(f"fatX{p.pID}").fillWith([1 - f, f])
            else:
                self.create_offsprings(bn, p, 'fat' )

            if p.matID == '0':  # Cas parents inconnu
                bn.cpt(f"matX{p.pID}").fillWith([1 - f, f])
            else:
                self.create_offsprings(bn, p, 'mat')

        gnb.showPotential(bn.cpt("matX4"))
        gnb.showBN(bn, size=100)

        return bn

    def load_evidence(self,file, famID):
        tab = dict()
        with open(file, 'r') as f:
            for (line, i) in enumerate(f.readlines()):
                ev = i.split()
                idfam = ev[0].split(':')[0]
                if ev[0] == famID:
                    del ev[0], ev[1]
                    ev = [float(i) for i in ev]
                    tab[f'X{line + 1}'] = ev
        return tab

    def load_evidence_out(self, file, famID):
        tab = dict()
        with open(file, 'r') as f:
            for (line, i) in enumerate(f.readlines()):
                ev = i.split()
                f_id = ev[0].split(':')[0]
                if f_id == f'X_{famID}':
                    key = ev[0].split(':')[1]
                    del ev[0], ev[1]
                    ev = [float(i) for i in ev]
                    tab[f'X{key}'] = ev
        return tab