#!/usr/bin/env python
# encoding: utf-8

import os

import networkx as nx  # type: ignore
from networkx.drawing.nx_agraph import graphviz_layout  # type: ignore
import matplotlib.pyplot as plt  # type: ignore
import matplotlib.patches as patches  # type: ignore

from .agent import Agent


class NetworkGraphUtils:
    def __init__(self, graph: nx.Graph):
        """
        :Purpose:
            This is the base class used to gather statistics from an
            exsting networkx graph object.

        :Input:
            graph : nx.Graph
              NetworkX graph object (typically attached to a Population self.nx_graph)
        """
        self.G = graph

    def connected_components(self):
        return list(self.G.subgraph(c).copy() for c in nx.connected_components(self.G))

    def write_graph_edgelist(self, path: str, id, time):
        file_path = os.path.join(path, f"{id}_Edgelist_t{time}.txt")
        nx.write_edgelist(self.G, file_path, delimiter="|", data=False)

    def write_network_stats(self, path: str, id, time):
        file_path = os.path.join(path, f"{id}_NetworkStats_t{time}.txt")

        components = sorted(self.connected_components(), key=len, reverse=True)

        outfile = open(file_path, "w")
        outfile.write(nx.info(self.G))

        cent_dict = nx.degree_centrality(self.G)

        outfile.write(
            "\nNumber of connected components: {}\n".format(
                nx.number_connected_components(self.G)
            )
        )

        tot_nodes = 0
        for c in components:
            tot_nodes += c.number_of_nodes()

        outfile.write(
            "Average component size: {}\n".format(
                tot_nodes * 1.0 / nx.number_connected_components(self.G)
            )
        )
        outfile.write(
            "Maximum component size: {}\n".format(nx.number_of_nodes(components[0]))
        )
        outfile.write("Degree Histogram: {}\n".format(nx.degree_histogram(self.G)))
        outfile.write("Graph density: {}\n".format(nx.density(self.G)))
        outfile.write(
            "Average node degree centrality: {}\n".format(
                sum(cent_dict.values()) / len(list(cent_dict.values()))
            )
        )

        outfile.write(
            "Average node clustering: {}\n".format(nx.average_clustering(self.G))
        )
        outfile.close()

    def get_network_color(self, coloring):
        G = self.G
        node_color = []

        # attribute based coloring
        color_order = ["b", "g", "c", "r", "y", "purple", "gray"]
        if hasattr(list(G.nodes)[0], coloring):
            attrs = []
            for v in G:
                val = getattr(v, coloring)
                if val not in attrs:
                    attrs.append(val)
                node_color.append(color_order[attrs.index(val)])

            return node_color

        # hard coded coloring schemes
        if coloring == "Tested":
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
        else:
            raise ValueError(
                "coloring value invalid!\n{coloring}\n \
            Only 'Tested', 'Trtmt', 'HR', 'HIV', or an Agent attribute allowed!"
            )

        return node_color

    def visualize_network(
        self,
        outdir,
        coloring="so",
        pos=None,
        return_layout=0,
        node_size=None,
        iterations=10,
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
        if node_size is None:
            node_size = 5000.0 / self.G.number_of_nodes()

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
            for v in self.G:
                NodeSize.append(node_size)
        else:
            for v in self.G:
                NodeSize.append((10 * G.degree(v)) ** (1.0))

        # draw:
        nx.draw(
            self.G,
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
            (
                r"N infection={:.2f}".format(txtboxLabel,),
                r"Time={:.2f}".format(curtime,),
            )
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

        filename = os.path.join(
            outdir, f"{label}_{G.number_of_nodes()}_{coloring}_{curtime}.png"
        )

        fig.savefig(filename)

        if return_layout:
            return pos
