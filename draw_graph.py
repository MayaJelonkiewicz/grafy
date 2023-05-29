import argparse
import sys
import pygraphviz as pgv
from graph import Digraph, Graph, IGraph, IDirectedGraph, IWeightedGraph, WeightedDigraph, WeightedGraph


def draw_graph(graph: IGraph, layout="circo"):
    directed = isinstance(graph, IDirectedGraph)
    weighted = isinstance(graph, IWeightedGraph)

    if layout.casefold() == "circo" or layout.casefold() == "neato" or layout.casefold() == "dot":
        agraph = pgv.AGraph(directed=directed, overlap=False)
        nodelist = [i for i in range(graph.vertex_count)]

        agraph.add_nodes_from(nodelist)
        agraph.node_attr['shape'] = 'circle'
        agraph.node_attr['color'] = 'blue'
        agraph.edge_attr['arrowsize'] = 0.75
        agraph.graph_attr['mindist'] = 0
        agraph.graph_attr['scale'] = 2
        agraph.graph_attr['size'] = (2, 2)

        for i in range(graph.vertex_count):
            for j in range(len(graph.adjacency_list[i])):
                if weighted:
                    agraph.add_edge(i, graph.adjacency_list[i][j].vertex, weight=graph.adjacency_list[i]
                               [j].weight, label=graph.adjacency_list[i][j].weight, fontcolor='red')
                else:
                    agraph.add_edge(i, graph.adjacency_list[i][j])

        agraph.layout(prog=layout)
        agraph.draw("graph.png")
    else:
        raise ValueError("Invalid layout.")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-w", "--weighted", action="store_true")
    parser.add_argument("-d", "--directed", action="store_true")
    parser.add_argument("-o", "--output-filename", default="graph.png")

    arguments = parser.parse_args()

    graph_cls = None
    match (arguments.directed, arguments.weighted):
        case (False, False):
            graph_cls = Graph
        case (False, True):
            graph_cls = WeightedGraph
        case (True, False):
            graph_cls = Digraph
        case (True, True):
            graph_cls = WeightedDigraph
    assert graph_cls is not None

    draw_graph(graph_cls.parse(sys.stdin.read()), "dot")


if __name__ == "__main__":
    main()
