#!/usr/bin/env python3

import argparse
import sys
import matplotlib.pyplot as plt
import networkx as nx
from graph import Graph


def task1(arguments):
    input_graph = Graph.parse(arguments.input_representation, sys.stdin.read())
    output_graph = input_graph.convert_to(arguments.output_representation)
    print(output_graph.data_to_string(), end="")


def task2(arguments):
    adjacencies = Graph.parse(
        arguments.input_representation, sys.stdin.read()).convert_to("adjlist").data

    graph = nx.Graph()
    for i in range(1, len(adjacencies) + 1):
        graph.add_node(i)
    for i in range(len(adjacencies)):
        for j in range(len(adjacencies[i])):
            if not graph.has_edge(adjacencies[i][j], i+1):
                graph.add_edge(i+1, adjacencies[i][j])
    pos = nx.circular_layout(graph)
    nx.draw(graph, pos=pos, with_labels=True)
    plt.savefig(arguments.output_filename)
    plt.clf()


def task3(arguments):
    if arguments.model == "gnl":
        print(Graph.generate_with_gnl_model(arguments.n, arguments.l)
              .convert_to(arguments.output_representation)
              .data_to_string(),
              end="")
    elif arguments.model == "gnp":
        print(Graph.generate_with_gnp_model(arguments.n, arguments.p)
              .convert_to(arguments.output_representation)
              .data_to_string(),
              end="")


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="task", required=True)

    subparser_1 = subparsers.add_parser("1")
    subparser_1.add_argument("-i", "--input-representation",
                             choices=["adjlist", "adjmatrix", "incmatrix"], required=True)
    subparser_1.add_argument("-o", "--output-representation",
                             choices=["adjlist", "adjmatrix", "incmatrix"], required=True)

    subparser_2 = subparsers.add_parser("2")
    subparser_2.add_argument("-i", "--input-representation",
                             choices=["adjlist", "adjmatrix", "incmatrix"], required=True)
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
