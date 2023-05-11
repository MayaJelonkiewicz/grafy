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

    def transpose(self) -> Self:
        edges = [(vertex_a, vertex_b) for vertex_a in range(
            self.vertex_count) for vertex_b in self.iter_adjacent(vertex_a)]
        transposed_graph = Digraph.empty(self.vertex_count)
        for edge in edges:
            transposed_graph.add_edge(edge[1], edge[0])
        return transposed_graph

    def find_strongly_connected_components(self) -> set[frozenset[int]]:
        # the order needs to be tracked, but a seperate set object is also
        # used to have O(1) lookup
        visited_vertices = set()
        visited_vertices_in_order = []

        def visit_recursively(vertex: int):
            if vertex in visited_vertices:
                return
            visited_vertices.add(vertex)

            for adjacent_vertex in self.iter_adjacent(vertex):
                visit_recursively(adjacent_vertex)

            visited_vertices_in_order.append(vertex)

        for start_vertex in range(self.vertex_count):
            visit_recursively(start_vertex)

        transposed_graph = self.transpose()
        visited_vertices = set()
        components = set()

        def get_components_recursively(vertex: int, component: set | None = None):
            if vertex in visited_vertices:
                return component
            visited_vertices.add(vertex)

            if component is None:
                component = set()

            component.add(vertex)
            for adjacent_vertex in transposed_graph.iter_adjacent(vertex):
                get_components_recursively(adjacent_vertex, component)
            return component

        for start_vertex in reversed(visited_vertices_in_order):
            component = get_components_recursively(start_vertex)
            if component is not None:
                components.add(frozenset(component))
        return components

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Digraph):
            return False

        if self.adjacency_list != other.adjacency_list:
            return False

        return True


if __name__ == "__main__":
    pass
