import argparse
import sys
import math

from graph import WeightedDigraph, Digraph


def task1(arguments):
    digraph = Digraph.parse(sys.stdin.read())

    visits = None
    if arguments.page_type == "random":
        visits = digraph.PageRank_Random(arguments.iteration_count)
    elif arguments.page_type == "power":
        visits = digraph.PageRank_PowerMethod(arguments.iteration_count)
    assert visits is not None

    for v in visits:
        print(f"{v[0]} ==> PageRank = {v[1]}")


def task2(arguments):
    lines = sys.stdin.read().splitlines()
    points = [tuple(map(int, line.split())) for line in lines]
    order = WeightedDigraph.find_approximate_2d_tsp_solution(
        points, arguments.temperature_iteration_count, arguments.inner_iteration_count)

    ordered_points = [points[i] for i in order]
    distance = 0.0
    for first_position, second_position in zip(
            ordered_points, ordered_points[1:] + ordered_points[:1]):
        x_difference = second_position[0] - first_position[0]
        y_difference = second_position[1] - first_position[1]
        distance += math.sqrt(x_difference ** 2 + y_difference ** 2)
        
    print(distance)
    print("\n".join(lines[i] for i in order))


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="task", required=True)

    subparser_1 = subparsers.add_parser(
        "1", help="apply PageRank analysis to a digraph")
    subparser_1.add_argument("iteration_count", type=int,
                             help="number of iterations")
    subparser_1.add_argument("page_type", choices=["random", "power"],
                             type=str, help="variant of the PageRank algorithm to use")

    subparser_2 = subparsers.add_parser(
        "2", help="compute an approximate solution to"
        " the travelling salesman problem in 2 dimensions")
    subparser_2.add_argument(
        "temperature_iteration_count", type=int,
        help="number of iterations over the temperature variable")
    subparser_2.add_argument("inner_iteration_count", type=int,
                             help="number of iterations per temperature value")

    arguments = parser.parse_args()
    arguments.task = int(arguments.task)

    if arguments.task == 1:
        task1(arguments)

    if arguments.task == 2:
        task2(arguments)


if __name__ == "__main__":
    main()
