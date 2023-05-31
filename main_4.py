import argparse
import sys
from graph import Digraph
from graph import WeightedDigraph


def task1(arguments):
    print(Digraph.generate_with_gnp_model(
        arguments.n, arguments.p).dump(), end="")


def task2(_):
    for component in Digraph.parse(sys.stdin.read()).find_strongly_connected_components():
        print(' '.join(map(str, component)))


def task3(arguments):
    result = Digraph.Bellman_Ford(arguments.n, arguments.p, arguments.v)
    print(result[0])


def task4(arguments):
    asdf = sys.stdin.read()
    result = WeightedDigraph.parse(asdf).johnson(verbose=arguments.verbose)
    if result is None:
        print("graph has negative cycle")
    else:
        for i in result:
            print(i)


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="task", required=True)

    subparser_1 = subparsers.add_parser("1", help="generate a random digraph")
    subparser_1.add_argument(
        "n", type=int, help="number of vertices in the generated graph")
    subparser_1.add_argument(
        "p", type=float, help="probability of an edge existing between any two vertices")

    subparsers.add_parser(
        "2", help="find all strongly connected components of a digraph")

    subparser_3 = subparsers.add_parser(
        "3", help="generate a random weighted digraph "
        "and find all the shortest paths from a given vertex in that graph")
    subparser_3.add_argument(
        "n", type=int, help="number of vertices in the generated graph")
    subparser_3.add_argument(
        "p", type=float, help="probability of an edge existing between any two vertices")
    subparser_3.add_argument(
        "v", type=int, help="index of the vertex to search for shortest paths from")

    subparser_4 = subparsers.add_parser(
        "4", help="find all the shortest paths between vertices in a weighted digraph")
    subparser_4.add_argument(
        "-v", "--verbose", action="store_true", help="verbose output")

    arguments = parser.parse_args()
    arguments.task = int(arguments.task)

    if arguments.task == 1:
        task1(arguments)
    elif arguments.task == 2:
        task2(arguments)
    elif arguments.task == 3:
        task3(arguments)
    elif arguments.task == 4:
        task4(arguments)


if __name__ == "__main__":
    main()
