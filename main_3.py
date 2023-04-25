import argparse
import sys

from graph import WeightedGraph


def task1(arguments):
    print(repr(WeightedGraph.generate_weighted_connected(
        arguments.n, arguments.l).adjacency_list))


def task2(arguments):
    graph = WeightedGraph.parse(sys.stdin.read())
    distances, predecessors = graph.dijkstra(arguments.v)
    for h in range(len(graph.adjacency_list)):
        vertex_predecessor = predecessors[h]
        predecessors_table = []
        predecessors_table.append(h)
        while vertex_predecessor is not None:
            predecessors_table.append(vertex_predecessor)
            x = predecessors[vertex_predecessor]
            vertex_predecessor = x
        print(
            f"d({arguments.v}, {h}) = {distances[h]} ==> {predecessors_table[::-1]}")


def task3(_):
    graph = WeightedGraph.parse(sys.stdin.read())
    distances = graph.calculate_all_distances()
    element_width = max(len(str(element))
                        for row in distances for element in row)
    for row in distances:
        for element in row:
            print(str(element).ljust(element_width), end=" ")
        print()


def task4(_):
    graph = WeightedGraph.parse(sys.stdin.read())
    min_sum_center = graph.find_min_sum_center()
    min_max_center = graph.find_min_max_center()
    print(f"center: {min_sum_center}")
    print(f"min-max center: {min_max_center}")


def task5(_):
    graph = WeightedGraph.parse(sys.stdin.read())
    print(graph.min_spanning_tree().dump())


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="task", required=True)

    subparser_1 = subparsers.add_parser("1")
    subparser_1.add_argument("n", type=int)
    subparser_1.add_argument("l", type=int)

    subparser_2 = subparsers.add_parser("2")
    subparser_2.add_argument("v", type=int)

    subparsers.add_parser("3")

    subparsers.add_parser("4")

    subparsers.add_parser("5")

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


if __name__ == "__main__":
    main()
