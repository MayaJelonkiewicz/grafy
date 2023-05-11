from __future__ import annotations
from random import randrange

from graph import IUndirectedGraph, IWeightedGraph


class WeightedDigraph(IUndirectedGraph, IWeightedGraph):
    """A weighted directed graph stored as an adjacency list"""

    def add_edge(self, vertex_a, vertex_b, weight):
        self.adjacency_list[vertex_a].append(
            IWeightedGraph.Adjacency(vertex_b, weight))

    def remove_edge(self, vertex_a, vertex_b):
        self.adjacency_list[vertex_a] = [
            a for a in self.adjacency_list[vertex_a] if a.vertex != vertex_b]

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

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, WeightedDigraph):
            return False

        if self.adjacency_list != other.adjacency_list:
            return False

        return True


if __name__ == "__main__":
    pass
