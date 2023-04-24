import argparse
from graph import Digraph

def task1(arguments):
    print(Digraph.generate_with_gnp_model(arguments.n, arguments.p).data_to_string())

def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="task", required=True)

    subparser_1 = subparsers.add_parser("1")
    subparser_1.add_argument("n", type=int)
    subparser_1.add_argument("p", type=float)

    arguments = parser.parse_args()
    arguments.task = int(arguments.task)

    if arguments.task == 1:
        task1(arguments)


if __name__ == "__main__":
    main()
