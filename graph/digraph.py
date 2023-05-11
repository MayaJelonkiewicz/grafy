from __future__ import annotations
import random
from typing import Self

from graph import IDirectedGraph, IUnweightedGraph


class Digraph(IDirectedGraph, IUnweightedGraph):
    """A directed graph, stored as an adjacency list"""

    def add_edge(self, vertex_a, vertex_b):
        self.adjacency_list[vertex_a].append(vertex_b)

    def remove_edge(self, vertex_a, vertex_b):
        self.adjacency_list[vertex_a].remove(vertex_b)

    @classmethod
    def generate_with_gnp_model(cls, n: int, p: float) -> Self:
        """Generate digraph using probability"""
        output = [[] for _ in range(n)]

        for i in range(n):
            for j in range(n):
                if random.random() <= p and j != i:
                    output[i].append(j)

        return cls(output)
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Digraph):
            return False

        if self.adjacency_list != other.adjacency_list:
            return False

        return True


if __name__ == "__main__":
    pass
