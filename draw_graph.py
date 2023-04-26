import argparse
import sys
import pygraphviz as pgv
from graph import Graph, Digraph, WeightedGraph


def draw_digraph(toDraw: Digraph, layout="circo"):

    if layout.casefold() == "circo" or layout.casefold() == "neato" or layout.casefold() == "dot":
        G = pgv.AGraph(directed=True, overlap=False)
        nodelist = [i for i in range(toDraw.vertex_count)]

        G.add_nodes_from(nodelist)
        G.node_attr['shape'] = 'circle'
        G.node_attr['color'] = 'blue'
        G.edge_attr['arrowsize'] = 0.75
        G.graph_attr['mindist'] = 0
        G.graph_attr['scale'] = 2
        G.graph_attr['size'] = (2, 2)

        for i in range(toDraw.vertex_count):
            for j in range(len(toDraw.adjacency_list[i])):
                G.add_edge(i, toDraw.adjacency_list[i][j])

        G.layout(prog=layout)
        G.draw("graph.png")
    else:
        raise ValueError("Invalid layout.")


def draw_graph(toDraw: Graph, layout="circo"):

    if layout.casefold() == "circo" or layout.casefold() == "neato" or layout.casefold() == "dot":
        G = pgv.AGraph(overlap=False)
        nodelist = [i for i in range(toDraw.vertex_count)]

        G.add_nodes_from(nodelist)
        G.node_attr['shape'] = 'circle'
        G.node_attr['color'] = 'blue'
        G.edge_attr['arrowsize'] = 0.75
        G.graph_attr['mindist'] = 0
        G.graph_attr['scale'] = 2
        G.graph_attr['size'] = (2, 2)

        for i in range(toDraw.vertex_count):
            for j in range(len(toDraw.adjacency_list[i])):
                G.add_edge(i, toDraw.adjacency_list[i][j])

        G.layout(prog=layout)
        G.draw("graph.png")
    else:
        raise ValueError("Invalid layout.")


def draw_weighted_graph(toDraw: WeightedGraph, layout="circo"):

    if layout.casefold() == "circo" or layout.casefold() == "neato" or layout.casefold() == "dot":
        G = pgv.AGraph(overlap=False)
        nodelist = [i for i in range(toDraw.vertex_count)]

        G.add_nodes_from(nodelist)
        G.node_attr['shape'] = 'circle'
        G.node_attr['color'] = 'blue'
        G.edge_attr['arrowsize'] = 0.75
        G.graph_attr['mindist'] = 0
        G.graph_attr['scale'] = 2
        G.graph_attr['size'] = (2, 2)

        for i in range(toDraw.vertex_count):
            for j in range(len(toDraw.adjacency_list[i])):
                G.add_edge(i, toDraw.adjacency_list[i][j].vertex, weight=toDraw.adjacency_list[i]
                           [j].weight, label=toDraw.adjacency_list[i][j].weight, fontcolor='red')

        G.layout(prog=layout)
        G.draw("graph.png")
    else:
        raise ValueError("Invalid layout.")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-w", "--weighted", action="store_true")

    arguments = parser.parse_args()

    if arguments.weighted:
        draw_weighted_graph(WeightedGraph.parse(sys.stdin.read()))
    else:
        draw_graph(Graph.parse(sys.stdin.read()))


if __name__ == "__main__":
    main()
