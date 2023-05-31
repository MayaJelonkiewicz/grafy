import argparse
import sys
from graph import WeightedDigraph


def task1(arguments):
    WDigraph = WeightedDigraph.generate_flow_graph(arguments.n)
    print(WDigraph.dump(), end="")


def task2(arguments):
    WDigraph = WeightedDigraph.parse(sys.stdin.read())
    WDigraph.Edmonds_Karp(arguments.s, arguments.t, arguments.filename)


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="task", required=True)

    subparser_1 = subparsers.add_parser(
        "1", help="generate random flow network (weighted digraph)")
    subparser_1.add_argument("n", type=int, help="number of layers")

    subparser_2 = subparsers.add_parser(
        "2", help="calculate maximum flow in a flow network (weighted digraph)"
        " and draw graph with flows visualised")
    subparser_2.add_argument("s", type=int, help="index of the source vertex")
    subparser_2.add_argument("t", type=int, help="index of the sink vertex")
    subparser_2.add_argument(
        "filename", type=str, default="graph", nargs="?", help="filename for the graph drawing")

    arguments = parser.parse_args()
    arguments.task = int(arguments.task)

    if arguments.task == 1:
        task1(arguments)
    elif arguments.task == 2:
        task2(arguments)


if __name__ == "__main__":
    main()
