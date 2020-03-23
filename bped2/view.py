#!/usr/local/bin/python
import pyAgrum as gum
import pyAgrum.lib.notebook as gnb
import pydotplus as pydot


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


def load_evidence(file, famID):
    tab = dict()
    with open(file, 'r') as f:
        for (line, i) in enumerate(f.readlines()):
            ev = i.split()
            idfam = ev[0].split(':')[0]
            if ev[0] == famID:
                del ev[0], ev[1]
                ev = [float(i) for i in ev]
                tab[f'X{line + 1}'] = ev
    return tab

def load_evidence_out(file, famID):
    tab = dict()
    with open(file, 'r') as f:
        for (line, i) in enumerate(f.readlines()):
            ev = i.split()
            f_id = ev[0].split(':')[0]
            if f_id == f'X_{famID}':
                key = ev[0].split(':')[1]
                del ev[0], ev[1]
                ev = [float(i) for i in ev]
                tab[f'X{key}'] = ev
    return tab

def create_holders(ped, bn, p, f):

    bn.add(gum.LabelizedVariable(f"matX{p.pID}", f"mother of {p.pID}", ["0", "1"]))
    bn.add(gum.LabelizedVariable(f"fatX{p.pID}", f"father of {p.pID}", ["0", "1"]))
    bn.add(gum.LabelizedVariable(f"X{p.pID}", f"{p.pID}", ["00", "01", "10", "11"]))
    bn.addArc(f"fatX{p.pID}", f"X{p.pID}")
    bn.addArc(f"matX{p.pID}", f"X{p.pID}")
    bn.cpt(f"X{p.pID}").fillWith([1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1])

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

def save_bn(bn,name):
    bn.saveBIF(name+'.bif')


