import argparse
import sys
from graph import Digraph


def task1(arguments):
    print(Digraph.generate_with_gnp_model(arguments.n, arguments.p).dump())


def task2(_):
    for component in Digraph.parse(sys.stdin.read()).find_strongly_connected_components():
        print(' '.join(map(str, component)))


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="task", required=True)

    subparser_1 = subparsers.add_parser("1")
    subparser_1.add_argument("n", type=int)
    subparser_1.add_argument("p", type=float)

    subparser_2 = subparsers.add_parser("2")

    arguments = parser.parse_args()
    arguments.task = int(arguments.task)

    if arguments.task == 1:
        task1(arguments)
    elif arguments.task == 2:
        task2(arguments)


if __name__ == "__main__":
    main()
