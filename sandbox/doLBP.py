#!/usr/local/bin/python
import bped2.view as pview
from time import *

def doLBP(bn_name):
    bn = pview.gum.BayesNet()
    bn.loadBIF(bn_name)
    try:
        t1 = process_time()
        ie = pview.gum.LoopyBeliefPropagation(bn)
        ie.setMaxTime(600)
        ie.makeInference()
        t2 = process_time()
        return t2 - t1
    except RuntimeError:
        print('too long')


def lbpPosterior(bn_name,evidence=None):
    bn = pview.gum.BayesNet()
    bn.loadBIF(bn_name)
    ie = pview.gum.LoopyBeliefPropagation(bn)
    if evidence:
        ie.setEvidence(evidence)
    ie.makeInference()
    return ie