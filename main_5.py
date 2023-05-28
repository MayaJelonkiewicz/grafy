import argparse
import sys
from graph import WeightedDigraph

def task1(arguments):
    WDigraph= WeightedDigraph.generate_flow_graph(arguments.n)
    print(WDigraph.dump())

def task2(arguments):
    WDigraph= WeightedDigraph.parse(sys.stdin.read())
    WDigraph.Edmonds_Karp(arguments.s,arguments.t,arguments.name)



def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="task", required=True)

    subparser_1 = subparsers.add_parser("1")
    subparser_1.add_argument("n", type=int)

    subparser_2 = subparsers.add_parser("2")
    subparser_2.add_argument("s", type=int)
    subparser_2.add_argument("t", type=int)
    subparser_2.add_argument("name", type=str)

    arguments = parser.parse_args()
    arguments.task = int(arguments.task)

    if arguments.task == 1:
        task1(arguments)
    elif arguments.task == 2:
        task2(arguments)
    


if __name__ == "__main__":
    main()
