#!/usr/bin/env python
# encoding: utf-8

import random

import numpy as np  # type: ignore
import networkx as nx  # type: ignore
from networkx.drawing.nx_agraph import graphviz_layout  # type: ignore
import matplotlib.pyplot as plt  # type: ignore
import matplotlib.patches as patches  # type: ignore
from typing import Sequence, List, Dict, Optional
from dotmap import DotMap  # type: ignore

from .HIVABM_Population import PopulationClass
from .agent import AgentSet


class NetworkClass(PopulationClass):
    def __init__(self, params: DotMap, popSeed: int = 0, netSeed: int = 0):
        """
        :Purpose:
            This is the base class used to generate the social network
            for the other agents, i.e. . The class inherits from the PopulationClass.

        :Input:
            N : int
              Number of agents. Default: 10000

            network_type: default is "scale_free", other options are "max_k_comp_size" and "binomial"
        """

        random.seed(netSeed)
        np.random.seed(netSeed)

        PopulationClass.__init__(self, popSeed, params)  # Create population

        # self.NetworkSize = N
        # happens for both scale_free and max_k_comp_size
        self.G = nx.Graph()
        for i in range(10):
            self.update_partner_assignments(self.G)

        if params.model.network.type == "max_k_comp_size":

            def trimComponent(component, maxComponentSize):
                for ag in component.nodes:
                    if random.random() < 0.1:
                        for rel in ag._relationships:
                            if len(ag._relationships) == 1:
                                break  # Make sure that agents stay part of the network by keeping one bond
                            rel.progress(forceKill=True)
                            self.Relationships.remove(rel)
                            component.remove_edge(rel.agent1, rel.agent2)
                            self.G.remove_edge(rel.agent1, rel.agent2)

                comps = list(
                    self.G.subgraph(c).copy() for c in nx.connected_components(self.G)
                )
                totNods = 0
                for component in comps:
                    cNodes = len(component)
                    if cNodes > params.maxComponentSize:
                        trimComponent(component, params.maxComponentSize)
                    elif cNodes < params.minComponentSize:
                        for a in component.nodes():
                            if a in self.G:
                                self.G.remove_node(a)

                    else:
                        totNods += cNodes

            components = sorted(self.connected_components(), key=len, reverse=True)
            for comp in components:
                if (
                    params.outputs.calc_component_stats
                    and comp.number_of_nodes() > params.model.network.component_size.max
                ):
                    print("TOO BIG", comp, comp.number_of_nodes())
                    trimComponent(comp, params.model.network.component_size.max)

            print("Total agents in graph: ", self.G.number_of_nodes())

    def connected_components(self):
        return (self.G.subgraph(c).copy() for c in nx.connected_components(self.G))

    def write_G_edgelist(self, path: str):
        G = self.get_Graph()
        nx.write_edgelist(G, path, data=["relationship"], delimiter="\t")

    def write_network_stats(
        self, t: int = 0, path: str = "results/network/networkStats.txt"
    ):
        subgraphs = (self.G.subgraph(c).copy() for c in nx.connected_components(self.G))
        components = sorted(subgraphs, key=len, reverse=True)
        bigG = components[0]
        outfile = open(path, "w")
        outfile.write(nx.info(self.G))

        centDict = nx.degree_centrality(self.G)

        outfile.write(
            "\nNumber of connected components: {}\n".format(
                nx.number_connected_components(self.G)
            )
        )
        conG = nx.connected_components(self.G)
        tot_nodes = 0
        for c in conG:
            thisComp = len(c)
            tot_nodes += thisComp
        outfile.write(
            "Average component size: {}\n".format(
                tot_nodes * 1.0 / nx.number_connected_components(self.G)
            )
        )
        outfile.write("Maximum component size: {}\n".format(nx.number_of_nodes(bigG)))
        outfile.write("Degree Histogram: {}\n".format(nx.degree_histogram(self.G)))
        outfile.write("Graph density: {}\n".format(nx.density(self.G)))
        outfile.write(
            "Average node degree centrality: {}\n".format(
                sum(centDict.values()) / len(list(centDict.values()))
            )
        )

        outfile.write(
            "Average node clustering: {}\n".format(nx.average_clustering(self.G))
        )
        outfile.close()

    def create_graph_from_agents(self, agents: AgentSet):
        G = self.get_Graph()
        numAdded = 0
        for tmpA in agents:
            numAdded += 1
            G.add_node(tmpA)
        print("\tAdded %d/%d agents" % (numAdded, G.number_of_nodes()))

    def get_Graph(self):
        """
        Return random assortative graph produced by ``set_assortative_graph``.
        """
        return self.G

    def get_network_color(self, coloring):
        G = self.G
        node_color = []
        if coloring == "SO":
            for v in G:
                tmp_sextype = v.so
                if tmp_sextype == "HM":
                    node_color.append("b")
                elif tmp_sextype == "HF":
                    node_color.append("g")
                elif tmp_sextype == "WSW":
                    node_color.append("c")
                elif tmp_sextype == "MSM":
                    node_color.append("r")
                elif tmp_sextype == "MTF":
                    node_color.append("y")
                else:
                    raise ValueError("Check agents %s sextype %s" % (v, tmp_sextype))
        elif coloring == "DU":
            for v in G:
                tmp_drugtype = v.drug_use
                if tmp_drugtype == "None":
                    node_color.append("g")
                elif tmp_drugtype == "NonInj":
                    node_color.append("b")
                elif tmp_drugtype == "Inj":
                    node_color.append("r")
                else:
                    raise ValueError("Check agents %s drug type %s" % (v, tmp_drugtype))
        elif coloring == "Tested":
            for v in G:
                if v.haart:
                    node_color.append("g")
                elif v.hiv_dx:  # tmp_hiv == 1:
                    node_color.append("y")
                elif v.hiv:  # tmp_aids == 1:
                    node_color.append("r")
                elif v.prep:
                    node_color.append("b")
                else:
                    node_color.append("purple")
        elif coloring == "Trtmt":
            for v in G:
                if v.hiv:  # tmp_aids == 1:
                    node_color.append("r")
                elif v.prep:
                    node_color.append("g")
                elif v.intervention_ever:
                    node_color.append("y")
                else:
                    node_color.append("gray")
        elif coloring == "HIV":
            for v in G:
                if v.aids:  # tmp_hiv == 1:
                    node_color.append("purple")
                elif v.hiv:  # tmpaids == 1:
                    node_color.append("r")
                else:
                    node_color.append("g")
        elif coloring == "HR":
            for v in G:
                if v.high_risk:  # tmp_hiv == 1:
                    node_color.append("r")
                elif v.high_risk_ever:  # tmp_aids == 1:
                    node_color.append("y")
                else:
                    node_color.append("g")
        elif coloring == "Race":
            for v in G:
                if v.race == "WHITE":
                    node_color.append("y")
                elif v.race == "BLACK":  # tmp_aids == 1:
                    node_color.append("g")
                else:
                    node_color.append("b")
        elif coloring == "MSW":
            for v in G:
                if v.race == "BLACK":
                    node_color.append("y")
                elif v.high_risk_ever:
                    node_color.append("b")
                elif v.race == "WHITE":
                    node_color.append("g")
                else:
                    raise ValueError("Check agents %s drug type %s" % (v, tmp_drugtype))
        else:
            raise ValueError(
                "coloring value invalid!\n%s\n \
            Only 'SO','DU','Tested', 'Trtmt', and 'HIV' allowed!"
                % str(coloring)
            )

        return node_color

    def visualize_network(
        self,
        coloring="SO",
        pos=None,
        return_layout=0,
        node_size=None,
        iterations=1,
        curtime=0,
        txtboxLabel=0,
        label="Network",
    ):
        """
        :Purpose:
            Visualize the network using the spring layout (default). \n

        :Input:
            graph : networkX graph
        """
        G = self.G
        print(("\tPlotting {} colored by {}...").format(label, coloring))
        fig = plt.figure()
        ax = fig.add_axes([0, 0, 1, 1])
        fig.clf()

        # build a rectangle in axes coords
        left, width = 0.0, 1.0
        bottom, height = 0.0, 1.0
        right = left + width
        top = bottom + height

        fig = plt.figure()
        ax = fig.add_axes([0, 0, 1, 1])

        # axes coordinates are 0,0 is bottom left and 1,1 is upper right
        p = patches.Rectangle(
            (left, bottom),
            width,
            height,
            fill=False,
            transform=ax.transAxes,
            clip_on=False,
        )

        ax.add_patch(p)

        if not pos:
            pos = graphviz_layout(G, prog="neato", args="")

        edge_color = "k"
        node_shape = "o"

        # node color to by type
        node_color = self.get_network_color(coloring)

        # node size indicating node degree
        NodeSize = []
        if node_size:
            for v in G:
                NodeSize.append(node_size)
        else:
            for v in G:
                NodeSize.append((10 * G.degree(v)) ** (1.0))

        # draw:
        nx.draw(
            G,
            pos,
            node_size=NodeSize,
            node_color=node_color,
            node_shape=node_shape,
            edge_color=edge_color,
            with_labels=False,
            linewidths=0.5,
            width=0.5,
        )

        textstr = "\n".join(
            (r"N infection=%.2f" % (txtboxLabel,), r"Time=%.2f" % (curtime,))
        )

        # these are matplotlib.patch.Patch properties
        props = dict(boxstyle="round", facecolor="wheat", alpha=0.9)

        # place a text box in upper right in axes coords
        ax.text(
            right - 0.025,
            top - 0.025,
            textstr,
            horizontalalignment="right",
            verticalalignment="top",
            transform=ax.transAxes,
            bbox=props,
        )

        filename = "images/%s_%d_%s_%d.png" % (
            label,
            G.number_of_nodes(),
            coloring,
            curtime,
        )

        fig.savefig(filename)

        if return_layout:
            return pos
