from bped2.pedigree import *

ped = Pedigree()
ped.gen_ped('f',20,4,4,4)
print(ped)
ped.ped_to_bn(0.05)