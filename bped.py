#!/usr/local/bin/python
import sys
from optparse import OptionParser
import bped2.pedigree as ped
import bped2.view as pview


def main(args=None):
    """
    [--ped pedfile: format famid, id, patid (0 for founder), matid (0 for founder), gender (1 male, 2 female)
    [--ev evidencefile]: format famid, id, ev00, ev10 (1 paternal), ev01 (1 maternal), ev11
    [--freq minorallelefreq (default: freq=0.01)]
    [--targets list_of_ind (default: all)]
    [--size] size of the rendered graph
    [--bndot dotfile] export the BN into a dot file
    [--peddot dotfile] export the pedigree into a dot file
    [--audit textfile] introspect pedigree into a text file
    [--verbose] display error/warning messages in stderr
    [--mode] decide which version between normal, compact and multi version of a BN
    [--thetha] format [probability, probability, ...]
    [--centimorgans] format [distance, distance, ...]
    [--inference ] Decide which inference use, LazyPropagation or LoobyBeliefPropagation
    [--complete Bool] Decice which version between complete and compact for the audit file
    [--out outfile] export probabilities into a out file
    [--name_gen] format [str ,str ,str ...]
    [--name_people] format [number_name, number_name, ... ]
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
    # parser.add_option("","--compact",dest="compact",
    #                   help="Decided if the BN is conpacted or not")
    parser.add_option("","--mode",dest="mode",
                      help="Choose the type of the generate bn, compact, no compact or multi")
    parser.add_option("","--theta",dest="theta",type="string",
                      help="Input a probability's distribution, shape: float;float; ...")
    parser.add_option("", "--centimorgans", dest="centimorgans", type="string",
                      help="Input the distance between genes in centimorgans, shape: float;float; ...")
    parser.add_option("","--inference",dest="inference",
                      help="Choose between LP and LBP")
    parser.add_option("","--complete",dest="complete",
                      help="Decide if the audit is a complete version or a compact version")
    parser.add_option("","--out",dest="out",
                      help="Export the evidence into a out file",metavar="FILE")
    parser.add_option("", "--size", dest="size",
                      help="Choose the size of the rendered graph", type="int", default=100)
    parser.add_option("", "--name_gen", dest="name_gen", type="string",
                      help="Input the gene's name, shape: str;str; ...")
    parser.add_option("", "--name_people", dest="name_people", type="string",
                      help="Input the people's name, shape: nb_name;nb_name; ...")

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
        famID = current_ped.get_domain()

        if options.name_people:
            name = dict()
            tmp = options.name_people.split(';')
            for i in tmp:
                x,y = i.split('_')
                name[x] = y
            current_ped.insert_name(name)

        name_gen = None
        if options.name_gen:
            name_gen = options.name_gen.split(';')
            print(name_gen)
        if options.mode == 'compact':
            bn = pview.ped_to_bn_compact(current_ped, options.f)
            if options.verbose:
                pview.gnb.showBN(bn, options.size)
        elif options.mode == 'no_compact':
            bn = pview.ped_to_bn(current_ped, options.f)
            if options.verbose:
                pview.gnb.showBN(bn, options.size)
        elif options.mode == 'multi':
            if options.theta:
                distance = options.theta.split(';')
                nb_gen = len(distance)+1
                for i in range(len(distance)):
                    distance[i] = float(distance[i])
                bn = pview.bn_multi_pb(current_ped, options.f, nb_gen, distance, name_gen)
                if options.verbose:
                    pview.gnb.showBN(bn, options.size)
            elif options.centimorgans:
                centimorgans = options.centimorgans.split(';')
                nb_gen = len(centimorgans)
                for i in range(len(centimorgans)):
                    centimorgans[i] = float(centimorgans[i])
                bn = pview.bn_multi_morgans(current_ped, options.f, nb_gen, centimorgans, name_gen)
                if options.verbose:
                    pview.gnb.showBN(bn, options.size)
            else:
                return "missing theta or centimorgan argument, cannot use the multi mode"

        # if options.peddotfile:
        #     pview.save(current_ped,options.peddotfile)
        #     if options.verbose:
        #         print('ped saved in '+options.peddotfile)

        if options.bnfile:
            bn.saveBIF(options.bndotfile)
            pview.gum.availableBNExts()
            pview.gum.saveBN(bn, options.bndotfile)
            if options.verbose:
                print('bndotfile saved in '+options.bndotfile)

        if options.bndotfile:
            pview.save_dot(bn,options.bndotfile)
            if options.verbose:
                print('bn saved in '+options.bndotfile)

        if options.peddotfile:
            if (len(current_ped)) > 1000 :
                pview.graph(current_ped,options.graph,True)
            else:
                pview.graph(current_ped, options.graph, False)
            if options.verbose:
                print("graph save in "+ options.peddotfile)


        if options.auditfile:
            if options.complete == False:
                current_ped.pedigree_overview_file(options.auditfile)
            else:
                current_ped.pedigree_overview_file(options.auditfile,True)
            if options.verbose:
                print('audit file ' + options.auditfile + ' created')

        if options.targets:
            if options.evfile:
                if options.mode == 'multi':
                    evidence = pview.load_evidence_multi(options.evfile, famID)
                else:
                    evidence = pview.load_evidence(options.evfile, famID)
                if options.verbose:
                    print(f"{options.evfile} loaded")

                if options.inference == 'LBP':
                    ie = pview.gum.LoopyBeliefPropagation(bn)
                else:
                    ie = pview.gum.LazyPropagation(bn)
                ie.setEvidence(evidence)
                ie.makeInference()
                for i in current_ped.get_pedigree().keys():
                    if i in options.targets:
                        print(ie.posterior(f"X{i}"))
                pview.create_out(options.out, current_ped, ie)
            else:
                if options.inference == 'LBP':
                    ie = pview.gum.LoopyBeliefPropagation(bn)
                else:
                    ie = pview.gum.LazyPropagation(bn)
                ie.makeInference()
                for i in current_ped.get_pedigree().keys():
                    if i in options.targets:
                        print(ie.posterior(f"X{i}"))
                pview.create_out(options.out, current_ped, ie)
        else:
            if options.evfile:
                evidence = pview.load_evidence(options.evfile, famID)
                if options.verbose:
                    print(f"{options.evfile} loaded")

                if options.inference == 'LBP':
                    ie = pview.gum.LoopyBeliefPropagation(bn)
                else:
                    ie = pview.gum.LazyPropagation(bn)
                ie.setEvidence(evidence)
                ie.makeInference()
                if options.mode == 'multi':
                    pview.create_out_multi(options.out, current_ped, ie, nb_gen, name_gen)
                else:
                    pview.create_out(options.out,current_ped,ie)
            else:
                if options.inference == 'LBP':
                    ie = pview.gum.LoopyBeliefPropagation(bn)
                else:
                    ie = pview.gum.LazyPropagation(bn)
                ie.makeInference()
                if options.mode == 'multi':
                    pview.create_out_multi(options.out, current_ped, ie, nb_gen, name_gen)
                else:
                    pview.create_out(options.out, current_ped, ie)

if __name__ == "__main__":
    main(sys.argv)
