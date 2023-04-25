import argparse
import sys

from graph import Graph


def task1(arguments):
    sequence = [int(v) for v in sys.stdin.read().split(" ")]
    if Graph.check_if_sequence_is_graphic(sequence):
        output_graph = Graph.from_graphic_sequence(sequence)
        assert output_graph is not None
        print(output_graph.dump(arguments.output_representation), end="")
    else:
        print("-")


def task2(arguments):
    sequence = [int(v) for v in sys.stdin.read().split(" ")]
    if Graph.check_if_sequence_is_graphic(sequence):
        graph_from_sequence = Graph.from_graphic_sequence(sequence)
        assert graph_from_sequence is not None
        output_graph = graph_from_sequence.randomize_edges(
            graph_from_sequence.edge_count)
        print(output_graph.dump(arguments.output_representation), end="")
    else:
        print("-")


def task3(arguments):
    input_graph = Graph.parse_with_representation(
        sys.stdin.read(), arguments.input_representation)
    print(*max(input_graph.find_components(), key=len))


def task4(arguments):
    graph = Graph.euler_graph_generator(arguments.n, arguments.k)
    cycle = graph.euler_cycle_finder()
    print(" ".join(map(str, cycle)))
    print(graph.dump(arguments.output_representation))


def task5(arguments):
    output_graph = Graph.generate_random_regular(arguments.n, arguments.k)
    print(output_graph.dump(arguments.output_representation), end="")


def task6(arguments):
    input_graph = Graph.parse_with_representation(
        sys.stdin.read(), arguments.input_representation)
    print("yes" if input_graph.find_hamiltonian_cycle() is not None else "no")


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="task", required=True)

    subparser_1 = subparsers.add_parser("1")
    subparser_1.add_argument("-o", "--output-representation",
                             choices=["adjlist", "adjmatrix", "incmatrix"], default="adjlist")

    subparser_2 = subparsers.add_parser("2")
    subparser_2.add_argument("-o", "--output-representation",
                             choices=["adjlist", "adjmatrix", "incmatrix"], default="adjlist")

    subparser_3 = subparsers.add_parser("3")
    subparser_3.add_argument("-i", "--input-representation",
                             choices=["adjlist", "adjmatrix", "incmatrix"], default="adjlist")

    subparser_4 = subparsers.add_parser("4")
    subparser_4.add_argument("n", type=int)
    subparser_4.add_argument("k", type=int)
    subparser_4.add_argument("-o", "--output-representation",
                             choices=["adjlist", "adjmatrix", "incmatrix"], default="adjlist")

    subparser_5 = subparsers.add_parser("5")
    subparser_5.add_argument("n", type=int)
    subparser_5.add_argument("k", type=int)
    subparser_5.add_argument("-o", "--output-representation",
                             choices=["adjlist", "adjmatrix", "incmatrix"], default="adjlist")

    subparser_6 = subparsers.add_parser("6")
    subparser_6.add_argument("-i", "--input-representation",
                             choices=["adjlist", "adjmatrix", "incmatrix"], default="adjlist")

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
    elif arguments.task == 5:
        task5(arguments)
    elif arguments.task == 6:
        task6(arguments)


if __name__ == "__main__":
    main()
