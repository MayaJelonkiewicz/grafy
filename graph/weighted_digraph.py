from __future__ import annotations
from typing import Self
from random import randrange

from graph import IUndirectedGraph, IWeightedGraph


class WeightedDigraph(IUndirectedGraph, IWeightedGraph):
    """A weighted directed graph stored as an adjacency list"""

    @classmethod
    def parse(cls, string: str) -> Self:
        """Parse raw string data into a WeightedDigraph object"""
        adjacency_list = []
        for line in string.splitlines():
            adjacencies = []
            for pair in line.split(","):
                vertex, weight = map(int, pair.strip().split(":"))
                adjacencies.append(IWeightedGraph.Adjacency(vertex, weight))
            adjacency_list.append(adjacencies)
        return cls(adjacency_list)

    @classmethod
    def generate_weighted_digraph(cls, digraph, lower, upper):
        """Generate random weighted digraph using digraph."""
        adjacency_list = []
        for i in digraph.adjacency_list:
            adjacencies = []
            for j in i:
                adjacencies.append(IWeightedGraph.Adjacency(
                    j, randrange(lower, upper)))
            adjacency_list.append(adjacencies)
        return cls(adjacency_list)


if __name__ == "__main__":
    pass
