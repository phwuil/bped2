#!/usr/local/bin/python
import bped2.view as pview
from time import *
import TenGeRine as ttgum

def doTTBN(bn_name):
    bn = pview.gum.BayesNet()
    bn.loadBIF(bn_name)
    try:
        t1 = process_time()
        ie = ttgum.ShaferShenoyTensorTrain(bn, precision=1e-4, info=False)
        marginalesSSTT, tempsSSTT, nb_param_SSTT = ie.makeInference()
        t2 = process_time()
        return t2 - t1
    except RuntimeError:
        print('too long')

def ttbn_posterior(bn_name):
    bn = pview.gum.BayesNet()
    bn.loadBIF(bn_name)
    ie = ttgum.ShaferShenoyTensorTrain(bn, precision=1e-4, info=False)
    marginalesSSTT, tempsSSTT, nb_param_SSTT = ie.makeInference()
    return marginalesSSTT, tempsSSTT, nb_param_SSTT

