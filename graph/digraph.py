from __future__ import annotations
import random
from typing import Self

from graph import IDirectedGraph, IUnweightedGraph


class Digraph(IDirectedGraph, IUnweightedGraph):
    """A directed graph, stored as an adjacency list"""

    @classmethod
    def generate_with_gnp_model(cls, n: int, p: float) -> Self:
        """Generate digraph using probability"""
        output = [[] for _ in range(n)]

        for i in range(n):
            for j in range(1, n+1):

                if random.random() <= p and j-1 != i:
                    output[i].append(j)

        return cls(output)

    def data_to_string(self) -> str:
        string = ""
        for row in self.adjacency_list:
            string += " ".join(map(lambda v: f"{v}", row)) + "\n"
        return string


if __name__ == "__main__":
    pass
