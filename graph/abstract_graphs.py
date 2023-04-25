from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any, Iterator, Self


class IGraph(ABC):
    """Abstract type for all graphs"""

    @abstractmethod
    def __init__(self, adjacency_list: list[list[Any]]):
        self.adjacency_list = adjacency_list

    @property
    def vertex_count(self) -> int:
        return len(self.adjacency_list)

    @property
    @abstractmethod
    def edge_count(self) -> int:
        pass

    @classmethod
    @abstractmethod
    def parse(cls, string) -> Self:
        pass


class IUndirectedGraph(IGraph):
    """Abstract type for all undirected graphs"""

    @property
    def edge_count(self) -> int:
        return sum(map(len, self.adjacency_list)) // 2


class IDirectedGraph(IGraph):
    """Abstract type for all directed graphs"""

    @property
    def edge_count(self) -> int:
        return sum(map(len, self.adjacency_list))

    def iter_edges(self) -> Iterator[int]:
        for row in self.adjacency_list:
            yield from row


class IUnweightedGraph(IGraph):
    """Abstract type for all unweighted graphs"""

    def __init__(self, adjacency_list: list[list[int]]):
        self.adjacency_list = adjacency_list

    @classmethod
    def parse(cls, string: str):
        """Parse raw string data into a Digraph object"""
        return cls([[int(value) for value in line.split()] for line in string.splitlines()])

    def iter_edges(self) -> Iterator[tuple[int, int]]:
        for first_vertex, second_vertices in enumerate(self.adjacency_list, start=1):
            for second_vertex in second_vertices:
                yield (first_vertex, second_vertex)

    def iter_edges_from(self, index) -> Iterator[int]:
        return self.adjacency_list[index]


class IWeightedGraph(IGraph):
    """Abstract type for all weighted graphs"""

    class Adjacency:
        """An entry in the adjacency list of a WeightedGraph"""

        def __init__(self, vertex, weight):
            self.vertex = vertex
            self.weight = weight

        def __repr__(self):
            return f"{self.vertex} {self.weight}"

    def __init__(self, adjacency_list: list[list[Adjacency]]):
        self.adjacency_list = adjacency_list
