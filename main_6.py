import argparse
import sys
import math

from graph import WeightedDigraph


def task2(arguments):
    points = [tuple(map(int, line.split()))
              for line in sys.stdin.read().splitlines()]
    order = WeightedDigraph.find_approximate_2d_tsp_solution(
        points, arguments.temperature_iteration_count, arguments.inner_iteration_count)
    print(" ".join(map(str, order)))

    ordered_points = [points[i] for i in order]
    distance = 0.0
    for first_position, second_position in zip(
            ordered_points, ordered_points[1:] + ordered_points[:1]):
        x_difference = second_position[0] - first_position[0]
        y_difference = second_position[1] - first_position[1]
        distance += math.sqrt(x_difference ** 2 + y_difference ** 2)
    print(distance)


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="task", required=True)

    subparser_2 = subparsers.add_parser("2")
    subparser_2.add_argument("temperature_iteration_count", type=int)
    subparser_2.add_argument("inner_iteration_count", type=int)

    arguments = parser.parse_args()
    arguments.task = int(arguments.task)

    if arguments.task == 2:
        task2(arguments)


if __name__ == "__main__":
    main()
