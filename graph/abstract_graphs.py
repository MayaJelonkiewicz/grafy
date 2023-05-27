from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any, Iterator, Self


class IGraph(ABC):
    """Abstract type for all graphs"""

    @abstractmethod
    def __init__(self, adjacency_list: list[list[Any]]):
        self.adjacency_list = adjacency_list

    @classmethod
    def empty(cls, vertex_count: int) -> Self:
        return cls([[] for _ in range(vertex_count)])

    @property
    def vertex_count(self) -> int:
        return len(self.adjacency_list)

    @property
    @abstractmethod
    def edge_count(self) -> int:
        pass

    @abstractmethod
    def iter_adjacent(self, index) -> Iterator[Any]:
        return iter(self.adjacency_list[index])

    @classmethod
    @abstractmethod
    def parse(cls, string) -> Self:
        pass

    @abstractmethod
    def dump(self) -> str:
        pass

    def __repr__(self):
        return f"{self.__class__.__name__}({self.adjacency_list})"

    def __hash__(self):
        return hash(tuple(frozenset(inner_list) for inner_list in self.adjacency_list))


class IUndirectedGraph(IGraph):
    """Abstract type for all undirected graphs"""

    @property
    def edge_count(self) -> int:
        return sum(map(len, self.adjacency_list)) // 2

    @property
    def vertex_degrees(self) -> list[int]:
        return [len(inner_list) for inner_list in self.adjacency_list]


class IDirectedGraph(IGraph):
    """Abstract type for all directed graphs"""

    @property
    def edge_count(self) -> int:
        return sum(map(len, self.adjacency_list))


class IUnweightedGraph(IGraph):
    """Abstract type for all unweighted graphs"""

    def __init__(self, adjacency_list: list[list[int]]):
        self.adjacency_list = adjacency_list

    @classmethod
    def parse(cls, string: str) -> Self:
        """Parse raw string data into an IUnweightedGraph object"""
        return cls([[int(value) for value in line.split()] for line in string.splitlines()])

    def iter_adjacent(self, index) -> Iterator[int]:
        return iter(self.adjacency_list[index])

    def dump(self) -> str:
        string = ""
        for row in self.adjacency_list:
            string += " ".join(map(lambda v: f"{v}", row)) + "\n"
        return string


class IWeightedGraph(IGraph):
    """Abstract type for all weighted graphs"""

    class Adjacency:
        """An entry in the adjacency list of a WeightedGraph"""

        def __init__(self, vertex, weight):
            self.vertex = vertex
            self.weight = weight

        def __repr__(self):
            return f"{self.vertex}:{self.weight}"

    def __init__(self, adjacency_list: list[list[Adjacency]]):
        self.adjacency_list = adjacency_list

    def iter_adjacent(self, index) -> Iterator[Adjacency]:
        return iter(self.adjacency_list[index])

    @classmethod
    def parse(cls, string: str) -> Self:
        """Parse raw string data into an IWeightedGraph object"""
        adjacency_list = []
        for line in string.splitlines():
            adjacencies = []
            for pair in line.split():
                vertex, weight = map(int, pair.strip().split(":"))
                adjacencies.append(IWeightedGraph.Adjacency(vertex, weight))
            adjacency_list.append(adjacencies)
        return cls(adjacency_list)

    def dump(self) -> str:
        string = ""
        for row in self.adjacency_list:
            string += " ".join(
                map(lambda a: f"{a.vertex}:{a.weight}", row)) + "\n"
        return string
