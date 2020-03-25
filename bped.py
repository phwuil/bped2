#!/usr/local/bin/python
import sys
from optparse import OptionParser
import bped2.pedigree as ped
import bped2.view as pview


def main(args=None):
    """
    --ped pedfile: format famid, id, patid (0 for founder), matid (0 for founder), gender (1 male, 2 female)
  [--ev evidencefile]: format famid, id, ev00, ev10 (1 paternal), ev01 (1 maternal), ev11
  [--freq minorallelefreq (default: freq=0.01)]
  [--targets list_of_ind (default: all)]
  [--bndot dotfile] export the BN into a dot file
  [--peddot dotfile] export the pedigree into a dot file
  [--audit textfile] introspect pedigree into a text file
  [--verbose] display error/warning messages in stderr
    """
    parser = OptionParser(version="%prog 0.1", usage="usage: %prog [options] pedfile")
    parser.add_option("", "--ev", dest="evfile",
                      help="Specification of the profile", metavar="FILE")
    parser.add_option("", "--freq", dest="f",
                      help="minor allel freq (gamma)", type="float", default=0.01)
    parser.add_option("", "--targets", dest="targets",
                      help="Specification of a list of targets (comma separated)")
    parser.add_option("", "--bndot", dest="bndotfile",
                      help="Export the BN into a dot file", metavar="FILE")
    parser.add_option("", "--peddot", dest="peddotfile",
                      help="Export the pedigree into a dot file", metavar="FILE")
    parser.add_option("", "--audit", dest="auditfile",
                      help="Export some stats on pedigree in a text file", metavar="FILE")
    parser.add_option("", "--verbose", dest="verbose", help="messages while processing", default=False,
                      action="store_true")
    parser.add_option("", "--bn", dest="bnfile", help="Export the BN into a BIF file", metavar="FILE")

    if args is None:
        (options, arguments) = parser.parse_args()
    else:
        (options, arguments) = parser.parse_args(args)

    if len(arguments) != 2:  # si on n'a pas mis de pedfile ou on en a mis trop
        parser.parse_args(["--help"])
    else:
        # on retrouve toutes les valeurs dans options (principalement)
        # options.peddotfile contient le nom du fichier
        # options.verbose contient True or False
        # etc.
        print("=" * 40)
        print(f"arguments: {arguments}")
        print("=" * 40)
        print(f"options: {options}")
        print("=" * 40)
        print("\n\n")

        pedfile = arguments[1]
        print(f"working on file : {pedfile}")
        current_ped = ped.Pedigree()
        current_ped.load(str(pedfile))
        print(current_ped)
        famID = current_ped.get_domain()
        bn = pview.ped_to_bn(current_ped,options.f)

        if options.evfile:
            pview.load_evidence(options.evfile,famID)
            print(f"{options.evfile} loaded")


        if options.peddotfile:
            pview.save(current_ped,options.peddotfile)
            print('ped saved')

        if options.bndotfile:
            pview.gum.saveBN(bn, options.bndotfile)
            print('bn_dot_file saved')

        if options.verbose:
            pass

        if options.bnfile:
            pview.save_bn(options.bndotfile)
            print('bn saved')

        if options.auditfile:
            ped.Pedigree.pedigree_overview_file(options.auditfile)

        if options.targets:
            ie = pview.gum.LazyPropagation(bn)
            ie.makeInference()
            for i in current_ped.get_pedigree().keys():
                if i in options.targets:
                    pview.gnb.showProba(ie.posterior(f"X{i}"))
        else:
            ie = pview.gum.LazyPropagation(bn)
            ie.makeInference()
            for i in current_ped.get_pedigree().keys():
                pview.gnb.showProba(ie.posterior(f"X{i}"))


if __name__ == "__main__":
    main(sys.argv)
