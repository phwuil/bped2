#!/usr/local/bin/python
import pickle as pkl
import pandas as pd
import numpy as np
def main():
    p = Pedigree()
    p.load("../data/fam9.ped")

main()