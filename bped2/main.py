import pickle as pkl
import pandas as pd
import numpy as np
from pedigree import *
def main():
    ped = Pedigree()
    ped.load("../data/fam9.ped")
    #print(p.getPeople(3))
    print(ped)
    p = People(4,4,4,4)
    print(p,"\n")
    ped.addPeople(p)
    print(ped)
    ped.removePeople(22)
    print(ped)

main()