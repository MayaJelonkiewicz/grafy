#!/usr/bin/env python3

import argparse
import sys
import matplotlib.pyplot as plt
import networkx as nx
from graph import Graph


def task1(arguments):
    graph = Graph.parse_with_representation(
        sys.stdin.read(), arguments.input_representation)
    print(graph.dump(arguments.output_representation), end="")


def task2(arguments):
    adjacencies = Graph.parse_with_representation(
        sys.stdin.read(), arguments.input_representation).adjacency_list

    graph = nx.Graph()
    for i in range(0, len(adjacencies)):
        graph.add_node(i)
    for i in range(len(adjacencies)):
        for j in range(len(adjacencies[i])):
            if not graph.has_edge(adjacencies[i][j], i):
                graph.add_edge(i, adjacencies[i][j])
    pos = nx.circular_layout(graph)
    nx.draw(graph, pos=pos, with_labels=True)
    plt.savefig(arguments.output_filename)
    plt.clf()


def task3(arguments):
    if arguments.model == "gnl":
        print(Graph.generate_with_gnl_model(arguments.n, arguments.l).dump(
            arguments.output_representation), end="")
    elif arguments.model == "gnp":
        print(Graph.generate_with_gnp_model(arguments.n, arguments.p).dump(
            arguments.output_representation), end="")


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="task", required=True)

    subparser_1 = subparsers.add_parser("1")
    subparser_1.add_argument("-i", "--input-representation",
                             choices=["adjlist", "adjmatrix", "incmatrix"], default="adjlist")
    subparser_1.add_argument("-o", "--output-representation",
                             choices=["adjlist", "adjmatrix", "incmatrix"], default="adjlist")

    subparser_2 = subparsers.add_parser("2")
    subparser_2.add_argument("-i", "--input-representation",
                             choices=["adjlist", "adjmatrix", "incmatrix"], default="adjlist")
    subparser_2.add_argument("-o", "--output-filename", default="output.png")

    subparser_3 = subparsers.add_parser("3")
    subparser_3_subparsers = subparser_3.add_subparsers(
        dest="model", required=True)

    subparser_3_gnl = subparser_3_subparsers.add_parser("gnl")
    subparser_3_gnl.add_argument("n", type=int)
    subparser_3_gnl.add_argument("l", type=int)
    subparser_3_gnl.add_argument(
        "-o", "--output-representation", required=True)

    subparser_3_gnp = subparser_3_subparsers.add_parser("gnp")
    subparser_3_gnp.add_argument("n", type=int)
    subparser_3_gnp.add_argument("p", type=float)
    subparser_3_gnp.add_argument(
        "-o", "--output-representation", required=True)

    arguments = parser.parse_args()
    arguments.task = int(arguments.task)

    if arguments.task == 1:
        task1(arguments)
    elif arguments.task == 2:
        task2(arguments)
    elif arguments.task == 3:
        task3(arguments)


if __name__ == "__main__":
    main()
