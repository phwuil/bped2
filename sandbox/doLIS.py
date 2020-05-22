#!/usr/local/bin/python
import bped2.view as pview
from time import *

def doLIS(bn_name):
    bn = pview.gum.BayesNet()
    bn.loadBIF(bn_name)
    try:
        t1 = process_time()
        ie = pview.gum.LoopyImportanceSampling(bn)
        ie.setMaxTime(200)
        ie.setEpsilon(5e-4)
        ie.makeInference()
        print(ie.messageApproximationScheme())
        t2 = process_time()
        return t2 - t1
    except RuntimeError:
        print('too long')


def lisPosterior(bn_name):
    bn = pview.gum.BayesNet()
    bn.loadBIF(bn_name)
    ie = pview.gum.LoopyImportanceSampling(bn)
    ie.setMaxTime(200)
    ie.setEpsilon(5e-4)
    ie.makeInference()
    print(ie.messageApproximationScheme())
    return ie