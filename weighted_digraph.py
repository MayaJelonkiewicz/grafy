from __future__ import annotations
from typing import Self
from random import randrange

class WeightedDigraph:
    """A weighted directed graph stored as an adjacency list"""

    class Adjacency:
        """An entry in the adjacency list of a WeightedDigraph"""

        def __init__(self, vertex, weight):
            self.vertex = vertex
            self.weight = weight

        def __repr__(self):
            return f"{self.vertex} {self.weight}"

    def __init__(self, adjacency_list: list[list[Adjacency]]):
        self.adjacency_list = adjacency_list

    @classmethod
    def parse(cls, string: str) -> Self:
        """Parse raw string data into a WeightedDigraph object"""
        adjacency_list = []
        for line in string.splitlines():
            adjacencies = []
            for pair in line.split(","):
                vertex, weight = map(int, pair.strip().split(":"))
                adjacencies.append(cls.Adjacency(vertex, weight))
            adjacency_list.append(adjacencies)
        return cls(adjacency_list)
    
    @classmethod
    def generate_weighted_digraph(cls, digraph, lower, upper):
        """Generate random weighted digraph using digraph."""
        adjacency_list = []
        for i in digraph.adjacency_list:
            adjacencies = []
            for j in i:
                adjacencies.append(cls.Adjacency(j, randrange(lower, upper)))
            adjacency_list.append(adjacencies)
        return cls(adjacency_list)
    

if __name__ == "__main__":
    pass