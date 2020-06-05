#!/usr/local/bin/python
import math

import pyAgrum as gum
import pyAgrum.lib.notebook as gnb
import pyAgrum.lib.bn2graph as bng
import pydotplus as pydot
import matplotlib.pyplot as plt
from pyAgrum.lib.notebook import showGraph
from pyAgrum.lib.dynamicBN import getTimeSlicesRange, noTimeCluster

mycmap=plt.get_cmap('Pastel1')

def nodevalue(n):
    cols={"X":0.5,
              "S":0.9,
              "m":0.7,
              "f":0.75}
    return cols[n[0]]

def save(ped, filename):
    """
    Save the current Pedigree in a file : filename.ped
    """
    with open(f'{filename}.ped', "w") as f:
        for i in ped._pedigree.values():
            f.write(f"{i._famID}\t{i._pID}\t{i._fatID}\t{i._matID}\n")



def graph(ped, name, bool):
    """
    DoubleCircle = Roots
    Box = leaves
    Diamond = Nodes
    """
    col_rac_fill = {ped.sex_undefined: "#C2F732", #Green
                    ped.sex_male: "#00ffff", #Cyan
                   ped.sex_female: "#ff009c", #Pink
                   ped.sex_malefemale: "#000000"} #Dark

    shape_nodes = {False:['circle','box','diamond'],True:['point','point','point']}

    roots = {i for i in ped.roots()}
    leaves = {i for i in ped.leaves()}
    graph = pydot.Dot(graph_type='digraph', graph_name=name, strict=True)
    for k, v in ped._pedigree.items():

        if v.pID in roots:
            graph.add_node(pydot.Node(k, shape=shape_nodes[bool][0], margin="0", width="0", height="0",
                                          style="filled", color=col_rac_fill[v.sex]))

        elif v.pID in leaves:
            graph.add_node(pydot.Node(k, shape=shape_nodes[bool][1], margin="0", width="0", height="0",
                                        style="filled", color=col_rac_fill[v.sex]))

        else:
            graph.add_node(pydot.Node(k, shape=shape_nodes[bool][2], margin="0", width="0", height="0",
                                        style="filled", color=col_rac_fill[v.sex]))

    node = -1
    for f,m in ped.get_couple():
        current_node = node
        graph.add_node(pydot.Node(current_node, shape='point'))
        graph.add_edge(pydot.Edge(f, current_node,color='blue'))
        graph.add_edge(pydot.Edge(m, current_node,color='pink'))
        node -= 1
        for c in ped.get_people(f).child.intersection(ped.get_people(m).child):
            edge = pydot.Edge(current_node, c)
            graph.add_edge(edge)

    graph.write_pdf(name + '.pdf')


def load_evidence(file,famID):
    tab = dict()
    with open(file,'r') as f:
        for (line,i) in enumerate(f.readlines()):
            ev = i.split()
            idfam = ev[0].split(':')[0]
            if ev[0] == famID:
                # del ev[0],ev[1]
                ev = [float(i) for i in ev[2:]]
                tab[f'X{line+1}'] = ev
    return tab

def load_evidence_out(file,famID):
    tab = dict()
    with open(file,'r') as f:
        for (line,i) in enumerate(f.readlines()):
            ev = i.split()
            f_id = ev[0].split(':')[0]
            if f_id == f'X_{famID}':
                key = ev[0].split(':')[1]
                ev = [float(i) for i in ev[1:]]
                tab[f'X{key}'] = ev
    return tab

def create_holders(ped, bn, p, f):

    bn.add(gum.LabelizedVariable(f"matX{p.pID}", f"mother of {p.pID}", ["0", "1"]))
    bn.add(gum.LabelizedVariable(f"fatX{p.pID}", f"father of {p.pID}", ["0", "1"]))
    bn.add(gum.LabelizedVariable(f"X{p.pID}", f"{p.pID}", ["00", "01", "10", "11"]))
    bn.addArc(f"fatX{p.pID}", f"X{p.pID}")
    bn.addArc(f"matX{p.pID}", f"X{p.pID}")
    bn.cpt(f"X{p.pID}").fillWith([1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1])

def create_holders_multi(ped, bn, p, f,id_gen):

    bn.add(gum.LabelizedVariable(f"matX{p.pID}_{id_gen}", f"mother of {p.pID}", ["0", "1"]))
    bn.add(gum.LabelizedVariable(f"fatX{p.pID}_{id_gen}", f"father of {p.pID}", ["0", "1"]))
    bn.add(gum.LabelizedVariable(f"X{p.pID}_{id_gen}", f"{p.pID}", ["00", "01", "10", "11"]))
    bn.addArc(f"fatX{p.pID}_{id_gen}", f"X{p.pID}_{id_gen}")
    bn.addArc(f"matX{p.pID}_{id_gen}", f"X{p.pID}_{id_gen}")
    bn.cpt(f"X{p.pID}_{id_gen}").fillWith([1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1])

def create_offsprings(ped, bn, p, parent):
    # parent = fat ou mat
    if parent == 'fat':
        parentID = p.fatID
    else:
        parentID = p.matID

    # Creating Selector
    bn.add(gum.LabelizedVariable(f"S{parent}{p.pID}", f"Selector of {parent}ID", ["fat", "mat"]))
    bn.cpt(f"S{parent}{p.pID}").fillWith([0.5, 0.5])

    bn.addArc(f"fatX{parentID}", f"{parent}X{p.pID}")
    bn.addArc(f"matX{parentID}", f"{parent}X{p.pID}")
    bn.addArc(f"S{parent}{p.pID}", f"{parent}X{p.pID}")  # Selector to fat/mat

    bn.cpt(f"{parent}X{p.pID}").fillWith([1, 0, 1, 0, 0, 1, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1])

def create_offsprings_compact(ped, bn, p, parent):
    # parent = fat ou mat
    if parent == 'fat':
        parentID = p.fatID
    else:
        parentID = p.matID

    bn.addArc(f"fatX{parentID}", f"{parent}X{p.pID}")
    bn.addArc(f"matX{parentID}", f"{parent}X{p.pID}")

    bn.cpt(f"{parent}X{p.pID}").fillWith([1,0,0.5,0.5,0.5,0.5,0,1])

def create_offsprings_multi(ped, bn, p, parent,id_gen):
    # parent = fat ou mat
    if parent == 'fat':
        parentID = p.fatID
    else:
        parentID = p.matID

    # Creating Selector
    bn.add(gum.LabelizedVariable(f"S{parent}{p.pID}_{id_gen}", f"Selector of {parent}ID", ["fat", "mat"]))
    bn.cpt(f"S{parent}{p.pID}_{id_gen}").fillWith([0.5, 0.5])

    bn.addArc(f"fatX{parentID}_{id_gen}", f"{parent}X{p.pID}_{id_gen}")
    bn.addArc(f"matX{parentID}_{id_gen}", f"{parent}X{p.pID}_{id_gen}")
    bn.addArc(f"S{parent}{p.pID}_{id_gen}", f"{parent}X{p.pID}_{id_gen}")  # Selector to fat/mat

    bn.cpt(f"{parent}X{p.pID}_{id_gen}").fillWith([1, 0, 1, 0, 0, 1, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1])

def ped_to_bn(ped, f):
    bn = gum.BayesNet()
    for p in ped.get_pedigree().values():
        create_holders(ped,bn, p, f)

    for p in ped.get_pedigree().values():
        if p.fatID == '0':  # Cas parents inconnu
            bn.cpt(f"fatX{p.pID}").fillWith([1 - f, f])
        else:
            create_offsprings(ped,bn, p, 'fat' )

        if p.matID == '0':  # Cas parents inconnu
            bn.cpt(f"matX{p.pID}").fillWith([1 - f, f])
        else:
            create_offsprings(ped,bn, p, 'mat')

    #gnb.showBN(bn, size=100)

    return bn

def ped_to_bn_compact(ped,f):
    bn = gum.BayesNet()
    for p in ped.get_pedigree().values():
        create_holders(ped,bn, p, f)

    for p in ped.get_pedigree().values():
        if p.fatID == '0':  # Cas parents inconnu
            bn.cpt(f"fatX{p.pID}").fillWith([1 - f, f])
        else:
            create_offsprings_compact(ped,bn, p, 'fat')

        if p.matID == '0':  # Cas parents inconnu
            bn.cpt(f"matX{p.pID}").fillWith([1 - f, f])
        else:
            create_offsprings_compact(ped,bn, p, 'mat')

    #gnb.showBN(bn, size=100)

    return bn

def bn_multi_pb(ped, f, nb_gen, proba):

    if len(proba) != nb_gen-1:
        return "Difference of size between gene's number and distance's number"
    bn = gum.BayesNet()

    for i in range(1,nb_gen+1):
        for p in ped.get_pedigree().values():
            create_holders_multi(ped,bn, p, f, i) # Creation de tous les noeuds

        for p in ped.get_pedigree().values():
            if p.fatID == '0':  # Cas parents inconnu
                bn.cpt(f"fatX{p.pID}_{i}").fillWith([1 - f, f])
            else:
                create_offsprings_multi(ped, bn, p, 'fat', i)

            if p.matID == '0':  # Cas parents inconnu
                bn.cpt(f"matX{p.pID}_{i}").fillWith([1 - f, f])
            else:
                create_offsprings_multi(ped, bn, p, 'mat', i)

    for i in range(1,nb_gen):
        j = i + 1
        for p in ped.get_pedigree().values():
            if p.fatID != '0' and p.matID != '0':
                bn.addArc(f"Sfat{p.pID}_{i}", f"Sfat{p.pID}_{j}")
                bn.addArc(f"Smat{p.pID}_{i}", f"Smat{p.pID}_{j}")
                bn.cpt(f"Sfat{p.pID}_{j}").fillWith([1- proba[i - 1], proba[i - 1], proba[i - 1], 1 - proba[i - 1]])
                bn.cpt(f"Sfat{p.pID}_{j}").fillWith([1- proba[i - 1], proba[i - 1], proba[i - 1], 1 - proba[i - 1]])

    return bn

def bn_multi_morgans(ped, f, nb_gen, centimorgans):
    if len(centimorgans) != nb_gen:
        return "Difference of size between gene's number and position's number"
    bn = gum.BayesNet()

    for i in range(1,nb_gen+1):
        for p in ped.get_pedigree().values():
            create_holders_multi(ped,bn, p, f, i) # Creation de tous les noeuds

        for p in ped.get_pedigree().values():
            if p.fatID == '0':  # Cas parents inconnu
                bn.cpt(f"fatX{p.pID}_{i}").fillWith([1 - f, f])
            else:
                create_offsprings_multi(ped, bn, p, 'fat', i)

            if p.matID == '0':  # Cas parents inconnu
                bn.cpt(f"matX{p.pID}_{i}").fillWith([1 - f, f])
            else:
                create_offsprings_multi(ped, bn, p, 'mat', i)

    for i in range(1,nb_gen):
        x = i - 1
        j = i + 1
        theta = (1 - math.exp(-2*(centimorgans[i]-centimorgans[x])/100.))/2.0
        for p in ped.get_pedigree().values():
            if p.fatID != '0' and p.matID != '0':
                bn.addArc(f"Sfat{p.pID}_{i}", f"Sfat{p.pID}_{j}")
                bn.addArc(f"Smat{p.pID}_{i}", f"Smat{p.pID}_{j}")
                bn.cpt(f"Sfat{p.pID}_{j}").fillWith([1 - theta, theta, theta, 1 - theta])
                bn.cpt(f"Sfat{p.pID}_{j}").fillWith([1 - theta, theta, theta, 1 - theta])

    return bn

def show_proba(bn):
    gnb.showInference(bn,size=15,nodeColor={n:nodevalue(n) for n in bn.names()},cmap=mycmap)

def save_bn(bn,name):
    bn.saveBIF(name+'.bif')

def save_dot(bn,name):
    bng.BN2dot(bn).write_pdf(name)

def max_clique_size(bn):
    jte = gum.JunctionTreeGenerator()
    jt = jte.junctionTree(bn)
    return max([len(jt.clique(cl)) for cl in jt.nodes()])

def create_out(filename, ped, inference):
    fam = list(ped.get_domain())[0]
    with open(filename+'.out', "w") as f:
        for i in ped.get_pedigree().keys():
            inf = inference.posterior(f'X{i}')
            f.write(f'{fam}:{i}\t{inf[0]}\t{inf[1]}\t{inf[2]}\t{inf[3]}\n')

def create_out_multi(filename, ped, inference, nb_gen):
    fam = list(ped.get_domain())[0]
    with open(filename+'.out', "w") as f:
        for n in range(1,nb_gen+1):
            for i in ped.get_pedigree().keys():
                inf = inference.posterior(f'X{i}_{n}')
                f.write(f'{fam}:{i}_{n}\t{inf[0]}\t{inf[1]}\t{inf[2]}\t{inf[3]}\n')

def audit(bn, ped, filename):
    with open(filename, "w") as f:
        ped.pedigree_overview_file(filename)
        f.write("---------------------------------------------------\n")
        f.write(f'The size of the bn is {bn.size()}\n')

def _TimeSlicesToDot(dbn):
    """
    Try to correctly represent dBN and 2TBN in dot format
    """
    timeslices = getTimeSlicesRange(dbn)
    g = pydot.Dot(graph_type='digraph')
    for k in sorted(timeslices.keys(), key=lambda x: -1 if x == noTimeCluster else 1e8 if x == 't' else int(x)):
        if k != noTimeCluster:
            cluster = pydot.Cluster(k, label="Gene {}".format(
                k), bgcolor="#DDDDDD")
            g.add_subgraph(cluster)
        else:
            cluster = g  # small trick to add in graph variable in no timeslice
        for (n, label) in sorted(timeslices[k]):
            cluster.add_node(pydot.Node('"' + n + '"', label='"' + label + '"', style='filled',
                                      color='#000000', fillcolor='white'))

    for tail, head in dbn.arcs():
        g.add_edge(pydot.Edge('"' + dbn.variable(tail).name() + '"',
                            '"' + dbn.variable(head).name() + '"',
                            constraint=False, color="blue"))

    for k in sorted(timeslices.keys(), key=lambda x: -1 if x == noTimeCluster else 1e8 if x == 't' else int(x)):
        if k != noTimeCluster:
            prec = None
            for (n, label) in sorted(timeslices[k]):
                if prec is not None:
                    g.add_edge(pydot.Edge('"' + prec + '"',
                                        '"' + n + '"',
                                        style="invis"))
                prec = n

    return g


def graph_multi(dbn, size=None):
    if size is None:
        size = gum.config["dynamicBN", "default_graph_size"]

    showGraph(_TimeSlicesToDot(dbn), size)
