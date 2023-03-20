import argparse
import sys

from graph import Graph


def task1(arguments):
    sequence = [int(v) for v in sys.stdin.read().split(' ')]
    if Graph.check_if_sequence_is_graphic(sequence):
        output_graph = Graph.from_graphic_sequence(
            arguments.output_representation, sequence)
        assert output_graph is not None
        print(output_graph.data_to_string(), end="")
    else:
        print('-')


def task3(arguments):
    input_graph = Graph.parse(arguments.input_representation, sys.stdin.read())
    print(*max(input_graph.find_components(), key=len))


def task6(arguments):
    input_graph = Graph.parse(arguments.input_representation, sys.stdin.read())
    print('tak' if input_graph.find_hamiltonian_cycle() is not None else 'nie')


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="task", required=True)

    subparser_1 = subparsers.add_parser("1")
    subparser_1.add_argument("-o", "--output-representation",
                             choices=["adjlist", "adjmatrix", "incmatrix"], required=True)

    subparser_3 = subparsers.add_parser("3")
    subparser_3.add_argument("-i", "--input-representation",
                             choices=["adjlist", "adjmatrix", "incmatrix"], required=True)

    subparser_6 = subparsers.add_parser("6")
    subparser_6.add_argument("-i", "--input-representation",
                             choices=["adjlist", "adjmatrix", "incmatrix"], required=True)

    arguments = parser.parse_args()
    arguments.task = int(arguments.task)

    if arguments.task == 1:
        task1(arguments)
    elif arguments.task == 3:
        task3(arguments)
    elif arguments.task == 6:
        task6(arguments)


if __name__ == "__main__":
    main()
