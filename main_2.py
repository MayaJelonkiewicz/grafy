import argparse
import sys

from graph import Graph


def task3(arguments):
    input_graph = Graph.parse(arguments.input_representation, sys.stdin.read())
    print(*max(input_graph.find_components(), key=len))


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="task", required=True)

    subparser_1 = subparsers.add_parser("3")
    subparser_1.add_argument("-i", "--input-representation",
                             choices=["adjlist", "adjmatrix", "incmatrix"], required=True)

    arguments = parser.parse_args()
    arguments.task = int(arguments.task)

    if arguments.task == 3:
        task3(arguments)


if __name__ == "__main__":
    main()
