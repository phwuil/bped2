#!/usr/local/bin/python

import random


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
        return self._famID

    @famID.setter
    def famID(self, famID) -> str:
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
    cl = 3

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
        """
        :param other: Instance of pedigree
        :return: True if the two pedigree are equals, False if not
        """
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
            if v.fatID == self.no_people and v.matID == self.no_people:  # If people doesn't have parents, it's a root
                yield v.pID

    def leaves(self):
        """
        People without childrens are leaves
        """
        for k, v in self._pedigree.items():
            if v.nbrChild() == 0:  # If people doesn't have childrens, it's a leave
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
        if father != self.no_people or mother != self.no_people:
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
            for j in self.get_people(i).child:
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

    def get_grand_parents(self, pID):
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
        for k, v in self._pedigree.items():
            if len(self.get_parents(v.pID)) > 1:
                couple.add((v.fatID, v.matID))
        return couple

    def remove_family(self, famID):
        """
        Remove an entire family in the Pedigree
        """
        for k, v in list(self._pedigree.items()):
            if v.famID == famID:
                del self._pedigree[k]


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
        Return a set that contains each previous generation of pID, from parents (1st gen) to nbG gen
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
                    for i in list(gen):
                        self.get_parents(i)
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
                    for i in list(children):
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

    def check_consanguinity(self, pID, nbG):
        """
        Check if a people has consanguinous origin by checking in the nbG older generation
        """
        parents = self.get_parents(pID)
        if len(parents) == 2:
            parent1, parent2 = self.get_parents(pID)
        elif len(parents) == 1:
            parent1 = list(parents)[0]
            parent2 = self.no_people
        else:
            return set()

        holders1 = set()
        holders2 = set()
        if parent1 != self.no_people and parent2 != self.no_people:
            holders1 = self.old_gen(parent1, nbG)
            holders2 = self.old_gen(parent2, nbG)
        elif parent1 != 0 and parent2 == self.no_people:
            holders1 = self.old_gen(parent1, nbG)
        elif parent2 != 0 and parent1 == self.no_people:
            holders2 = self.old_gen(parent2, nbG)
        return holders1.intersection(holders2)

    def check_consanguinity_family(self, famID):
        """

        :param famID: ID of a family in the pedigree
        :return: a set of people who have consanguinous origin in the family
        """
        fam = self.gen_family_pedigree(famID)
        res = set()
        for v in fam._pedigree.values():
            res.update(self.check_consanguinity(v.pID, self.cl))
        return res

    def check_consanguinity_pedigree(self):
        """
        :return: All people who have consanguinous origin in the pedigree
        """
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
        parent_p1 = self.get_parents(p1)
        parent_p2 = self.get_parents(p1)

        children_p1 = self.get_people(p1).child
        children_p2 = self.get_people(p2).child

        if p1 in parent_p2 or p2 in parent_p1 or p1 in children_p2 or p2 in children_p1:
            return True

        holders_p1 = set(self.old_gen(p1, nbG))
        holders_p2 = set(self.old_gen(p2, nbG))

        if p1 in holders_p2 or p2 in holders_p1:
            return True

        x = holders_p1.intersection(holders_p2)
        return len(x) != 0

    def all_consanguineous_ped(self,nbG):
        """
        :return: All people who have consanguinous origin in the pedigree
        """
        dom = self.get_domain()
        res = set()
        for d in dom:
            fam = self.gen_family_pedigree(d)
            csg = set()
            for k in fam._pedigree.keys():
                p1 = fam.get_people(k).fatID
                p2 = fam.get_people(k).matID
                if p1 != '0' and p2 != '0':
                    holders_p1 = set(fam.old_gen(p1, nbG-1))
                    holders_p2 = set(fam.old_gen(p2, nbG-1))
                    x = holders_p1.intersection(holders_p2)
                    if len(x) != 0 or p1 in holders_p2 or p2 in holders_p1:
                        csg.add(k)
            res.update(csg)
        return res

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

    def pedigree_overview_file(self, filename, complete):
        """

        :return: a file which contains informations about the pedigree
        """

        with open(filename, "w") as f:
            stats = self.get_stat_family()
            if complete is True :
                for k, v in self._people2line.items():
                    f.write(f"People {k} is defined at line {v}\n")
                f.write("---------------------------------------------------\n")
                for k, v in stats.items():
                    f.write(f"The Family {k} is composed by {v} members \n")
                f.write("---------------------------------------------------\n")

            f.write(f'There is {len(self._pedigree)} people in this pedigree\n')
            f.write(f'There is {self.depth()} generation in this pedigree\n')
            nb_sex = self.nb_sexe_ped()
            f.write(f'There is {nb_sex[0]} men and {nb_sex[1]} women identify in this pedigree\n')
            f.write(f'There is {len(self._pedigree) / self.depth()} people by generation in average\n')
            f.write(f'There is {len([i for i in self.roots()])} people without parents in this pedigree\n')
            f.write(f'There is {len([i for i in self.leaves()])} people without childrens in this pedigree \n')
            f.write(f'The brotherhood\'s mean size is {self.mean_child()} in this pedigree \n')
            f.write(f'The biggest brotherhood is composed by {self.max_child()[1]} people \n')
            f.write(f'There is {self.mean_weeding()} weeding by people in average\n')
            f.write(
                f"Out of {len(stats)} families, there are {self.check_one_people_family()} composed by one people\n")
            f.write(
                f"In the pedigree, this people appear as mother and also as father : {self.check_mother_and_father()}\n")
            f.write(
                f"In the pedigree, this people had consangineous origins : {self.all_consanguineous_ped(self.cl)}\n")

    def depth(self):
        """
        Count the depth of the pedigree, ie largest path between roots and leaves
        :return: int
        """
        holders = [i for i in self.roots()]
        children = set()
        for i in holders:
            for j in list(self.get_people(i).child):
                children.add(j)
        if len(children) != 0:
            gen = 2
        else:
            return 1
        while True:
            tmp = set()
            for i in children:
                for j in list(self.get_people(i).child):
                    tmp.add(j)
            children = list(tmp)
            if len(tmp) == 0:
                return gen
            else:
                gen += 1

    def mean_child(self):
        """

        :return: The mean of child per person
        """
        mean = 0
        for k, v in self._pedigree.items():
            mean += self.get_people(k).nbrChild()
        return mean / len(self._pedigree)

    def max_child(self):
        """
        Return the people who got the largest brotherhood and it number
        :return: (str,int)
        """
        nb = 0
        people = '0'
        for k, v in self._pedigree.items():
            if self.get_people(k).nbrChild() > nb:
                nb = self.get_people(k).nbrChild()
                people = k
        return people, nb

    def nb_sexe_ped(self):
        """
        Calculte the nombers of men and women in the pedigree
        :return: (int,int)
        """
        father = set()
        mother = set()
        for v in self._pedigree.values():
            if v.fatID != self.no_people :
                father.add(v.fatID)
            if v.matID != self.no_people:
                mother.add(v.matID)
        return (len(father), len(mother))

    def mean_weeding(self):
        """
        :param: pedigree
        :return: mean of number of weeding by people
        """
        parents = set()
        people = set()
        for v in self._pedigree.values():
            if v.fatID != '0' and v.matID != '0':
                parents.add(v.fatID)
                parents.add(v.matID)
                people.add((v.fatID,v.matID))
        return len(people)/len(parents)


    def gen_ped(self, famID, nb, g_max, c_max, cl, pb_remariage=0.1):
        """
        generate a pedigree with nb people

        :param
        nb : nombre de people
        g_max: nbr de génération max
        c_max: nbr d'enfants max par famille
        cl: niveau de consanguinité accepté
        pb_remariage: Probablité d'effectuer un re mariage
        """

        def waiting_wedding(famID, mea, people, sex):
            """

            :param famID: ID of the family
            :param mea:
            :param people:
            :param sex:
            :return:
            """
            self.add_people(famID, people, self.no_people, self.no_people)
            profondeur[people] = profondeur[mea[1]] - 1
            self.add_sex(people, sex)
            self.get_people(people).add_children(mea[1])
            if sex == self.sex_male:
                if families.get((people, mea[0])) is None:
                    families[(people, mea[0])] = []
                    families[(people, mea[0])].append(mea[1])
                else:
                    families[(people, mea[0])].append(mea[1])
                self.get_people(mea[1])._set(famID, people, mea[0])
            else:
                if families.get((mea[0], people)) is None:
                    families[(mea[0], people)] = []
                    families[(mea[0], people)].append(mea[1])
                else:
                    families[(mea[0], people)].append(mea[1])
                self.get_people(mea[1])._set(famID, mea[0], people)

            mea.clear()

        def create_wedding(famID, people1, people2, child, sex):
            self.add_people(famID, people1, self.no_people, self.no_people)
            profondeur[people1] = profondeur[child] - 1
            self.get_people(people1).add_children(child)
            self.get_people(people2).add_children(child)
            self.add_sex(people1, sex)
            if sex == self.sex_male:
                if families.get((people1, people2)) == None:
                    families[(people1, people2)] = []
                    families[(people1, people2)].append(child)
                else:
                    families[(people1, people2)].append(child)
                self.get_people(child)._set(famID, people1, people2)
            else:
                if families.get((people2, people1)) == None:
                    families[(people2, people1)] = []
                    families[(people2, people1)].append(child)
                else:
                    families[(people2, people1)].append(child)
                self.get_people(child)._set(famID, people2, people1)

        prof_mariage_max = 2  # Wedding with 2 generations gap are available
        gamma = 0.8  # discount factor pour controle de la taille de famille
        mea = []  # Waiting wedding
        profondeur = dict()  # Node depth
        families = dict()  # [(Dad,Mom)] -> list(children)

        for i in range(1, nb + 1):
            profondeur[str(i)] = -1  # Profondeur pour tous initiale = -1

        # Création of the first individu
        self.add_people(famID, '1', self.no_people, self.no_people)
        profondeur['1'] = 0

        for p in range(2, nb + 1):
            new_p = str(p)

            if len(mea) > 0:  # Si nous avons un mariage en attendre
                #print('finir le mea',new_p,mea[0])
                if self.get_people(mea[0]).sex == self.sex_male:
                    # Ajout de la mere
                    waiting_wedding(famID, mea, new_p, self.sex_female)
                    continue
                else:
                    # Ajout du pere
                    waiting_wedding(famID, mea, new_p, self.sex_male)
                    continue

            child_pot = [i for i in self.roots() if profondeur[i] > 0 and self.get_parents(i) != set()]  # Liste des enfants potentiels
            parents_pot = []  # Liste des parents potentiels
            for k, v in self._pedigree.items():
                if v.nbrChild() < c_max and g_max - 1 > profondeur[k] > -1:
                    parents_pot.append(k)
            k1 = len(child_pot)
            k2 = len(parents_pot)
            if k1 + k2 == 0:
                self.add_people(famID, new_p, self.no_people, self.no_people)
                profondeur[new_p] = random.randint(0, g_max - 1)
                continue

            choice = random.random()
            ratio = (k1 / (k1 + k2))
            if choice > ratio:
                parent = random.sample(parents_pot, 1)[0]
                # Nouvel enfant

                couple = []
                for p1, p2 in families.keys():  # Recherche de tous les mariages où parent est présent
                    if p1 == parent or p2 == parent:
                        couple.append((p1, p2))

                if couple == []:  # parent n'est dans aucun mariage ie pas d'enfant
                    if random.random() < 0.5:  # Random pour le choix du sexe
                        self.add_people(famID, new_p, parent, self.no_people)
                        self.add_sex(parent, self.sex_male)
                    else:
                        self.add_people(famID, new_p, self.no_people, parent)
                        self.add_sex(parent, self.sex_female)

                    # PH proba de créer un nouveau parent ou alors chercher un autre parent pour le mariage

                    if random.random() < pb_remariage:
                        #print('remariage',new_p)
                        # chercher un parent deja existant
                        # creer le nouveau mariage
                        new_parent = [k for k in parents_pot if
                                      abs(profondeur[k] - profondeur[parent]) <= prof_mariage_max
                                      and self.get_people(k).sex != self.get_people(parent).sex and k != parent and self.is_consanguineous(parent,k,cl) is False]

                        if len(new_parent) == 0:
                            #print('mea avec new_p fils',new_p)
                            profondeur[new_p] = profondeur[parent] + 1
                            self.get_people(parent).add_children(new_p)
                            mea.extend([parent, new_p])
                            continue

                        parent2 = random.sample(new_parent, 1)[0]
                        #print('avant',parent, parent2)
                        # while self.is_consanguineous(parent, parent2, cl) is True :
                        #     if len(new_parent) == 0:
                        #         profondeur[new_p] = profondeur[parent] + 1
                        #         self.get_people(parent).add_children(new_p)
                        #         mea.extend([parent, new_p])
                        #         continue
                        #     #print(self.get_people(parent).sex == self.get_people(parent2).sex,self.is_consanguineous(parent, parent2, cl))
                        #     new_parent.remove(parent2)
                        #     if len(new_parent) == 0:
                        #         profondeur[new_p] = profondeur[parent] + 1
                        #         self.get_people(parent).add_children(new_p)
                        #         mea.extend([parent, new_p])
                        #         continue
                        #     parent2 = random.sample(new_parent, 1)[0]
                        #     #print(parent2)
                        while True:
                            if self.is_consanguineous(parent, parent2, cl) is True:
                                new_parent.remove(parent2)
                                if len(new_parent) == 0:
                                    profondeur[new_p] = profondeur[parent] + 1
                                    self.get_people(parent).add_children(new_p)
                                    mea.extend([parent, new_p])
                                    break
                                parent2 = random.sample(new_parent, 1)[0]
                            else:
                                self.get_people(parent).add_children(new_p)
                                self.get_people(parent2).add_children(new_p)
                                profondeur[new_p] = max(profondeur[parent], profondeur[parent2]) + 1
                                #print('remariage SANS csg', parent, parent2, new_p)
                                break
                        #print(self.is_consanguineous(parent, parent2, cl))
                        # print(parent, parent2, self.get_people(parent).sex == self.get_people(parent2).sex,
                        #       self.get_people(parent2).sex, self.get_people(parent).sex, famID, nb)
                        # self.get_people(parent).add_children(new_p)remariage
                        # self.get_people(parent2).add_children(new_p)
                        # profondeur[new_p] = max(profondeur[parent], profondeur[parent2]) + 1
                        # print('remariage SANS csg',parent,parent2,new_p)

                        if self.get_people(parent).sex == self.sex_male:
                            self.get_people(parent2).sex = self.sex_female
                            if families.get((parent, parent2)) is None:
                                families[(parent, parent2)] = []
                                families[(parent, parent2)].append(new_p)
                                self.get_people(new_p)._set(famID, parent, parent2)
                            else:
                                families[(parent, parent2)].append(new_p)
                                self.get_people(new_p)._set(famID, parent, parent2)
                        else:
                            self.get_people(parent2).sex = self.sex_male
                            if families.get((parent2, parent)) is None:
                                families[(parent2, parent)] = []
                                families[(parent2, parent)].append(new_p)
                                self.get_people(new_p)._set(famID, parent2, parent)
                            else:
                                families[(parent2, parent)].append(new_p)
                                self.get_people(new_p)._set(famID, parent2, parent)
                    else:
                        #print('mea autre',new_p,parent)
                        profondeur[new_p] = profondeur[parent] + 1
                        self.get_people(parent).add_children(new_p)
                        mea.extend([parent, new_p])
                        continue
                else:  # On regarde où ajouté l'enfant parmis tous les mariages de parent
                    tmp = []
                    keys = []
                    for k, v in families.items():
                        if k in couple:
                            tmp.append(gamma ** len(v))
                            keys.append(k)
                    # index = tmp.index(min(tmp))
                    # PH calculer gamma^len(v) et faire un tirage aléatoire avec les poids tmp

                    index = random.choices(keys, weights=tmp, k=1)
                    #print('pour attraper les consanguins', keys, type(keys), index)
                    old_index = index
                    index = tuple(index[0])
                    while True:
                        if self.is_consanguineous(index[0], index[1], cl) is True:
                            ind = keys.index(index)
                            keys.remove(index)
                            del tmp[ind]
                            if len(keys) == 0 or len(tmp)==0:
                                if self.get_people(parent).sex == self.sex_male:
                                    self.add_people(famID, new_p, parent, self.no_people)
                                else:
                                    self.add_people(famID, new_p, self.no_people, parent)
                                profondeur[new_p] = profondeur[parent] + 1
                                self.get_people(parent).add_children(new_p)
                                mea.extend([parent, new_p])
                                break
                            index = random.choices(keys, weights=tmp, k=1)
                            index = tuple(index[0])
                        else:
                            #print('pour attraper les consanguins apres ', keys, type(keys), index)
                            families[index].append(new_p)
                            self.add_people(famID, new_p, index[0], index[1])
                            self.get_people(index[0]).add_children(new_p)
                            self.get_people(index[1]).add_children(new_p)
                            self.get_people(new_p)._set(famID, index[0], index[1])
                            profondeur[new_p] = max(profondeur[index[0]], profondeur[index[1]]) + 1
                            #print('pas de consanguins la normalement', index[0], index[1], new_p)
                            break
                    # print('pour attraper les consanguins apres ', keys, type(keys), index)
                    # families[index].append(new_p)
                    # self.add_people(famID, new_p, index[0], index[1])
                    # self.get_people(index[0]).add_children(new_p)
                    # self.get_people(index[1]).add_children(new_p)
                    # self.get_people(new_p)._set(famID, index[0], index[1])
                    # profondeur[new_p] = max(profondeur[index[0]], profondeur[index[1]]) + 1
                    # print('pas de consanguins la normalement',index[0],index[1],new_p)
                    # PH max(genepapa,genemaman)+1

            else:
                # Nouveau Parent ie Crée une nouvelle famille
                child = random.sample(child_pot, 1)[0]
                # conjoint = [k for k in self._pedigree.keys() if profondeur[k] == profondeur[new_p] -1]
                profnewparent = profondeur[child] - 1
                conjoint = [k for k in self._pedigree.keys() if profondeur[k] <= profnewparent
                            and abs(profondeur[k] - profnewparent) <= prof_mariage_max]
                # conjoint_bis = [conjoint[i].pop() for i in conjoint if profondeur[i] == profondeur[new_p] - 1]

                if len(conjoint) == 0:
                    conjoint_weight = [0]
                else:
                    conjoint_weight = [0] * len(conjoint) + [i for i in range(1, len(conjoint) + 1)]
                alea = random.choice(conjoint_weight)
                # alea = random.randint(0,len(conjoint))

                if alea == 0:
                    #print('mea avec new_p daron',new_p)
                    # On crée un MEA
                    self.add_people(famID, new_p, self.no_people, self.no_people)
                    profondeur[new_p] = profondeur[child] - 1
                    self.get_people(new_p).add_children(child)
                    if random.random() < 0.5:
                        self.add_sex(new_p, self.sex_male)
                        mea.extend([new_p, child])
                    else:
                        self.add_sex(new_p, self.sex_female)
                        mea.extend([new_p, child])
                else:
                    # On lui cherche un conjoint
                    other_p = random.sample(conjoint, 1)[0]
                    #while self.is_consanguineous(new_p, other_p, cl) is True:
                    if child == other_p:
                        conjoint.remove(other_p)
                        other_p = random.sample(conjoint, 1)[0]
                    #print('on cherche un conjoint',other_p,new_p,child)
                    if self.get_people(other_p).sex == self.no_people:
                        self.add_people(famID, new_p, self.no_people, self.no_people)
                        profondeur[new_p] = profondeur[child] - 1
                        self.add_sex(new_p, self.sex_male)
                        self.add_sex(other_p, self.sex_female)
                        self.get_people(new_p).add_children(child)
                        self.get_people(other_p).add_children(child)
                        self.get_people(child)._set(famID, new_p, other_p)

                        if families[(new_p, other_p)] is None:
                            families[(new_p, other_p)] = []
                            families[(new_p, other_p)].append(child)
                        else:
                            families[(new_p, other_p)].append(child)

                    elif self.get_people(other_p).sex == self.sex_male:
                        create_wedding(famID, new_p, other_p, child, self.sex_female)
                    else:
                        create_wedding(famID, new_p, other_p, child, self.sex_male)

        self.update_children_all()
        self.update_parents_all()

### ---------------------------------------------------------------------------

    def insert_name(self,dict_name):
        for i in dict_name.keys():
            if i in self.get_pedigree():
                self.add_people(self.get_people(i).famID, dict_name[i], self.get_people(i).fatID, self.get_people(i).matID)
                self.add_sex(dict_name[i], self.get_people(i).sex)
                for c in self.get_people(i).child:
                    self.get_people(dict_name[i]).add_children(c)
                self.remove_people(i)
                # self.get_people(i)._pID = dict_name[i]
                # self.get_pedigree()[dict_name[i]] = self.get_pedigree().pop(i)
            for p in self.get_pedigree().keys():
                if self.get_people(p).matID == i:
                    self.get_people(p)._matID = dict_name[i]
                if self.get_people(p).fatID == i:
                    self.get_people(p)._fatID = dict_name[i]
                if i in self.get_people(p).child :
                    self.get_people(p).remove_children(i)
                    self.get_people(p).add_children(dict_name[i])