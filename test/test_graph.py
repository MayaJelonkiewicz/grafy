import itertools
import random
from typing import Iterable
from unittest import TestCase
import numpy as np

from graph import Graph


class GraphTestCase(TestCase):
    """Test Graph class"""

    def setUp(self):
        # hack to use seeded randomness for all tests
        global random  # pylint: disable=global-statement,invalid-name
        random = __import__("random").Random(12345)

    @staticmethod
    def get_all_hamiltonian_cycles(graph: Graph) -> Iterable[list[int]]:
        # iterate over potential cycles
        for cycle in itertools.permutations(range(graph.vertex_count)):
            cycle = [*cycle, cycle[0]]
            # check if all relevant edges exist
            if all(a in graph.iter_adjacent(b) for a, b in zip(cycle, cycle[1:])):
                yield [v for v in cycle][:-1]

    @staticmethod
    def has_euler_cycle(graph: Graph) -> bool:
        edges = list(graph.iter_edges())
        # iterate over potential cycles
        for cycle in itertools.permutations(edges):
            cycle = [*cycle, cycle[0]]
            if all(a[1] == b[0] for a, b in zip(cycle, cycle[1:])):
                return True
        return False

    @staticmethod
    def generate_all_graphs_with_vertex_count(vertex_count: int) -> Iterable[Graph]:
        for edge_sequence in itertools.product([False, True],
                                               repeat=vertex_count * (vertex_count - 1) // 2):
            graph = Graph.empty(vertex_count)
            edge_count_iterator = iter(edge_sequence)
            for a in range(vertex_count):
                for b in range(a + 1, vertex_count):
                    if next(edge_count_iterator):
                        graph.add_edge(a, b)
            yield graph

    def test_parse_with_representation(self):
        representations = ["adjlist", "adjmatrix", "incmatrix"]

        graphs = []
        for representation in representations:
            with open(f"test/resources/graph_representations/{representation}.txt",
                      encoding="utf-8") as file:
                graphs.append(Graph.parse_with_representation(
                    file.read(), representation)) # type: ignore

        # check if all graphs are equal
        for g0, g1 in zip(graphs, graphs[1:]):
            self.assertEqual(g0, g1)

    def test_dump_with_representation(self):
        representations = ["adjlist", "adjmatrix", "incmatrix"]

        with open("test/resources/graph_representations/adjlist.txt", encoding="utf-8") as file:
            graph = Graph.parse_with_representation(file.read(), "adjlist")

        for representation in representations:
            with open(f"test/resources/graph_representations/{representation}.txt", "r",
                      encoding="utf-8") as file:
                a = file.read()
                self.assertEqual(graph.dump_with_representation(representation),  # type: ignore
                                 a)

    def test_gnl_generation_edge_count(self):
        for n in range(10):
            for l in range(n * (n - 1) // 2 + 1):
                generated_edge_count = Graph.generate_with_gnl_model(
                    n, l).edge_count
                self.assertEqual(
                    generated_edge_count,
                    l,
                    f"{n=}, {l=}, {generated_edge_count=}"
                )

    def test_gnl_generation_invalid_arguments(self):
        for arguments in [
            (-1, 0),
            (1, 1),
            (2, 2),
            (10, 10 * 9 // 2 + 1),
        ]:
            self.assertRaises(
                ValueError, Graph.generate_with_gnl_model, *arguments)

    def test_gnp_generation_valid_arguments(self):
        for arguments in [
            (0, 0),
            (5, 0.5),
            (5, 1),
            (5, 0.98),
            (10, 0.3),
        ]:
            try:
                Graph.generate_with_gnp_model(*arguments)
            except ValueError:
                self.fail("ValueError was raised")

    def test_gnp_generation_invalid_arguments(self):
        for arguments in [
            (-1, 0),
            (5, -0.0001),
            (5, 1.0001)
        ]:
            self.assertRaises(
                ValueError, Graph.generate_with_gnp_model, *arguments)

    def test_regular_generation(self):
        for vertex_count in range(1, 7):
            graphs = self.generate_all_graphs_with_vertex_count(vertex_count)
            # include only graphic sequences which consist of one repeated value, and keep just
            # that value
            possible_degrees = {next(iter(s)) for g in graphs if len(
                s := set(g.vertex_degrees)) == 1}
            min_checked_degree = min(possible_degrees) - 1
            max_checked_degree = max(possible_degrees) + 1
            for degree in range(min_checked_degree, max_checked_degree + 1):
                try:
                    graph = Graph.generate_random_regular(vertex_count, degree)
                    self.assertIn(degree, possible_degrees)
                    unique_degrees = set(graph.vertex_degrees)
                    self.assertEqual(len(unique_degrees), 1)
                    self.assertEqual(next(iter(unique_degrees)), degree)
                except ValueError:
                    self.assertNotIn(degree, possible_degrees)

    def test_graphic_sequence_check_and_graph_generation(self):
        for vertex_count in range(7):
            graphic_sequences = {tuple(graph.vertex_degrees) for graph in
                                 self.generate_all_graphs_with_vertex_count(vertex_count)}

            # check correctness for all possible sequences with values in [-1; vertex_count + 1]
            # (this includes all possible sequences plus extras)
            for sequence in itertools.product(range(-1, vertex_count + 2), repeat=vertex_count):
                self.assertEqual(
                    Graph.check_if_sequence_is_graphic(list(sequence)),
                    sequence in graphic_sequences
                )
                self.assertEqual(
                    (graph := Graph.from_graphic_sequence(
                        list(sequence))) is not None,
                    sequence in graphic_sequences
                )
                if graph is not None:
                    self.assertEqual(
                        sorted(graph.vertex_degrees),
                        sorted(sequence)
                    )

    def test_find_components(self):
        for _ in range(1000):
            vertex_count = random.randrange(1, 50)
            edge_count = random.randrange(vertex_count * 4)
            graph = Graph.empty(vertex_count)

            # the value at index i is the identifier of the component that vertex belongs to.
            # at the start, each vertex is in its unique component, but they get merged as new
            # edges get added
            vertex_component_ids = list(range(vertex_count))

            # add random edges to graph
            for _ in range(edge_count):
                vertex_0 = random.randrange(vertex_count)
                vertex_1 = random.randrange(vertex_count)
                if vertex_0 in graph.iter_adjacent(vertex_1):
                    continue

                graph.add_edge(vertex_0, vertex_1)

                new_component_id = vertex_component_ids[vertex_0]
                old_component_id = vertex_component_ids[vertex_1]
                for index, value in enumerate(vertex_component_ids):
                    if value == old_component_id:
                        vertex_component_ids[index] = new_component_id

            component_ids = list(np.unique(vertex_component_ids))
            components = [[] for _ in component_ids]
            for vertex, vertex_component_id in enumerate(vertex_component_ids):
                components[component_ids.index(
                    vertex_component_id)].append(vertex)

            # use set-like type because order is irrelevant
            # use frozenset specifically because it is hashable
            self.assertEqual(
                frozenset(map(frozenset, graph.find_components())),
                frozenset(map(frozenset, components))
            )

    def test_find_hamiltonian_cycle(self):
        for vertex_count in range(1, 6):
            for graph in self.generate_all_graphs_with_vertex_count(vertex_count):
                cycles = list(GraphTestCase.get_all_hamiltonian_cycles(graph))
                found_cycle = graph.find_hamiltonian_cycle()
                if found_cycle is not None:
                    self.assertIn(found_cycle, cycles)
                else:
                    self.assertFalse(cycles)
