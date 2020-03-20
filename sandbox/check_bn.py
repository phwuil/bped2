from bped2.pedigree import *

ped = Pedigree()
ped.gen_ped('f',20,4,4,4)
ped.save('../data/check_bn.ped')
ped.graph('check_bn',False)
print(ped)
ped.ped_to_bn(0.05)