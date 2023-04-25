from __future__ import annotations
from typing import Literal, Self
import random
import warnings
import numpy as np

from graph import IUndirectedGraph, IUnweightedGraph


class Graph(IUndirectedGraph, IUnweightedGraph):
    """A graph with a given representation"""

    @property
    def vertex_degrees(self) -> list[int]:
        return [len(inner_list) for inner_list in self.adjacency_list]

    @classmethod
    def parse_with_representation(
        cls, string: str, representation: Literal["adjlist", "adjmatrix", "incmatrix"]
    ) -> Self:
        "parse raw string data into a Graph object"

        data = [[int(value) for value in line.split()]
                for line in string.splitlines()]
        match representation:
            case "adjlist":
                adjacency_list = data
            case "adjmatrix":
                adjacency_list = Graph._adjacency_matrix_to_adjacency_list(
                    data)
            case "incmatrix":
                adjacency_list = Graph._incidence_matrix_to_adjacency_list(
                    data)

        return cls(adjacency_list)

    def dump(self, representation: Literal["adjlist", "adjmatrix", "incmatrix"]) -> str:
        data = []
        match representation:
            case "adjlist":
                data = self.adjacency_list
            case "adjmatrix":
                data = Graph._adjacency_list_to_adjacency_matrix(
                    self.adjacency_list)
            case "incmatrix":
                data = Graph._adjacency_list_to_incidence_matrix(
                    self.adjacency_list)

        string = ""
        for row in data:
            string += " ".join(map(lambda v: f"{v}", row)) + "\n"
        return string

    @classmethod
    def generate_with_gnl_model(cls, n: int, l: int) -> Self:
        """Generate graph using number of edges"""
        if n < 0:
            raise ValueError("n < 0")

        if l < 0:
            raise ValueError("l < 0")

        if l > n*(n-1)//2:
            raise ValueError(f"{l = } is too large for graph where {n = }")

        output = [[0 for _ in range(n)] for _ in range(n)]
        if 0 < l < n*(n-1)/2:
            while l > 0:
                row = random.randrange(0, n)
                col = random.randrange(0, n)

                if row != col:
                    if output[row][col] == 0:
                        output[row][col] = 1
                        output[col][row] = 1
                        l -= 1
        elif l == n*(n-1)//2:
            for i in range(n):
                for j in range(i+1, n):
                    output[i][j] = output[j][i] = 1

        return cls(cls._adjacency_matrix_to_adjacency_list(output))

    @classmethod
    def generate_with_gnp_model(cls, n: int, p: float) -> Self:
        """Generate graph using probability"""
        if p < 0 or p > 1:
            raise ValueError("p < 0 or p > 1")

        if n < 0:
            raise ValueError("n < 0")

        output = [[0 for _ in range(n)] for _ in range(n)]

        edge = 0

        for i in range(n):
            for j in range(i+1, n):

                if random.random() <= p:
                    if output[i][j] == 0 and edge <= n*(n-1)/2.:

                        output[i][j] = output[j][i] = 1

                        edge += 1
                    else:
                        break

        return cls(cls._adjacency_matrix_to_adjacency_list(output))

    @classmethod
    def generate_random_regular(cls, n, k) -> Self:
        # TODO: fix use of 1-indexing

        if n < 0:
            raise ValueError("n < 0")

        if k < 0:
            raise ValueError("k < 0")

        if k >= n:
            raise ValueError("k >= n")

        if k % 2 == 1 and n % 2 == 1:
            raise ValueError("both k and n are odd")

        output = [[] for j in range(n)]

        edges = [[k, i+1] for i in range(0, n)]
        random.shuffle(edges)

        while edges[0][0] != 0:
            v = edges[0][1]
            amount = edges[0][0]

            for i in range(amount):
                edges[0][0] -= 1
                edges[i+1][0] -= 1

                v2 = edges[i+1][1]

                output[v-1].append(v2)
                output[v2-1].append(v)

            edges.sort(reverse=True)

        return cls(output)

    @staticmethod
    def _adjacency_matrix_to_adjacency_list(input: list[list[int]]) -> list[list[int]]:
        """transform 'adjacency matrix' to 'adjacency list'"""
        output = []
        for i in input:
            row = []
            for id, j in enumerate(i):
                if j == 1:
                    row.append(id)
            output.append(row)
        return output

    @staticmethod
    def _adjacency_list_to_adjacency_matrix(input: list[list[int]]) -> list[list[int]]:
        """transform 'adjacency list' to 'adjacency matrix'"""
        node_amount = len(input)
        output = [[0 for i in range(node_amount)] for j in range(node_amount)]
        for iid, i in enumerate(input):
            for j in i:
                output[iid][j] = 1
        return output

    @staticmethod
    def _adjacency_list_to_incidence_matrix(input: list[list[int]]) -> list[list[int]]:
        """transform 'adjacency list' to 'incidence matrix'"""
        m = len(input)
        n = 0
        for i in input:
            n += len(i)
        n = int(n/2)
        output = [[0 for i in range(n)] for j in range(m)]
        col_it = 0
        for iid, i in enumerate(input):
            for j in i:
                if iid < j:
                    output[iid][col_it] = 1
                    output[j][col_it] = 1
                    col_it += 1
            if col_it == n:
                break
        return output

    @staticmethod
    def _incidence_matrix_to_adjacency_list(input: list[list[int]]) -> list[list[int]]:
        """transform 'incidence matrix' to 'adjacency list'"""
        m = len(input)
        n = len(input[0])
        output = [[] for j in range(m)]
        for i in range(n):
            id = -1
            for j in range(m):
                if input[j][i] == 1:
                    if id > -1:
                        output[id].append(j)
                        output[j].append(id)
                        break
                    else:
                        id = j
        output = list(map(sorted, output))  # sort rows
        return output

    @staticmethod
    def check_if_sequence_is_graphic(sequence: list[int]) -> bool:
        """Check whether or not a provided sequence is a graphic sequence,
        i.e. can be the sequence of degrees for some graph"""

        if not sequence:
            # a sequence of length 0 is always graphic
            return True

        if max(sequence) >= len(sequence):
            # highest degree of a vertex is larger than the number of other
            # vertices, meaning the graph can't be constructed
            return False

        if sum(sequence) % 2 == 1:
            # sum of degrees must be even
            return False

        # create new list to avoid modifying input
        remaining_edges = list(sequence)

        # this loop involves "adding" edges until all vertices have the target
        # number of incident edges. the actual edges are not tracked, only the
        # remaining number of incident edges for each vertex
        while True:
            remaining_edges.sort(reverse=True)

            if all(d == 0 for d in remaining_edges):
                # all vertices have the correct number of edges
                return True

            if min(remaining_edges) < 0:
                # one of the vertices has more incident edges than its
                # target degree
                return False

            # create edges between the vertex with the largest number of remaining
            # edges n and the n next vertices with the largest number of remaining
            # edges
            for index in range(1, remaining_edges[0] + 1):
                remaining_edges[index] -= 1
            remaining_edges[0] = 0

    @classmethod
    def from_graphic_sequence(cls, sequence: list[int]) -> Self | None:
        if not sequence:
            # a sequence of length 0 corresponds to a graph with no vertices
            return cls([])

        if max(sequence) >= len(sequence):
            # highest degree of a vertex is larger than the number of other
            # vertices, meaning the graph can't be constructed
            return None

        if sum(sequence) % 2 == 1:
            # sum of degrees must be even
            return None

        # tracks how many more incident edges must still be added to each vertex
        remaining_edges = list(sequence)

        # tracks vertex indices. when remaining_edges gets sorted, this list
        # gets rearranged in the same way
        vertex_indices = list(range(len(sequence)))

        # adjacency list, to be built up during the upcoming loop
        adjacency_list = [[] for _ in sequence]

        # this loop involves adding edges until all vertices have the target
        # number of incident edges.
        while True:
            # sort remaining_edges, but rearrange vertex_indices in the same way
            remaining_edges, vertex_indices = (list(t) for t in zip(
                *sorted(zip(remaining_edges, vertex_indices), reverse=True)))

            if all(d == 0 for d in remaining_edges):
                # all vertices have the correct number of edges
                return cls(adjacency_list)

            if min(remaining_edges) < 0:
                # one of the vertices has more incident edges than its
                # target degree
                return None

            # create edges between the vertex with the largest number of remaining
            # edges n and the n next vertices with the largest number of remaining
            # edges
            for index in range(1, remaining_edges[0] + 1):
                remaining_edges[index] -= 1
                adjacency_list[vertex_indices[0]].append(vertex_indices[index])
                adjacency_list[vertex_indices[index]].append(vertex_indices[0])
            remaining_edges[0] = 0

    def find_components(self):
        """Finds and returns all the components of the graph."""

        def components_r(nr: int, v: int, g: list[list[int]], comp: list) -> None:
            for i in range(len(g[v])):
                if comp[g[v][i]] is None:
                    comp[g[v][i]] = nr
                    components_r(nr, g[v][i], g, comp)

        nr = 0
        comp = []
        for i in range(len(self.adjacency_list)):
            comp.append(None)
        for i in range(len(self.adjacency_list)):
            if comp[i] is None:
                comp[i] = nr
                components_r(nr, i, self.adjacency_list, comp)
                nr += 1

        components = [[] for _ in range(nr)]
        for vertex_index, component_index in enumerate(comp):
            components[component_index].append(vertex_index)
        return components

    def find_hamiltonian_cycle(self):
        """A function that returns a Hamiltonian cycle of the graph if one exists,
        or None otherwise"""
        def recurse(adjacency_list: list[list[int]], vertex: int,
                    visited: list[int], s: list) -> list[int] | None:
            s.append(vertex)
            if len(s) < len(adjacency_list):
                visited[vertex] = True
                for i in range(len(adjacency_list[vertex])):
                    if not visited[adjacency_list[vertex][i]]:
                        result = recurse(
                            adjacency_list, adjacency_list[vertex][i], visited, s)
                        if result is not None:
                            return result
                visited[vertex] = False
                s.pop()
            else:
                for i in range(len(adjacency_list[vertex])):
                    if adjacency_list[vertex][i] == 0:
                        return s

                s.pop()

            return None

        return recurse(self.adjacency_list, 0, [0 for _ in self.adjacency_list], [])

    def randomize_edges(self, rand_it: int) -> Self:
        """
        A function that returns graph with rerandomized edges, nodes degree is kept.

        Attributes
        -------------
        rand_it : int
        number of randomization
        max_rerolling_attempt : int, optional
        how much attempts in finding swap pair before abandoning (default is 99)
        """
        def _check_if_can_swap(y1, y2, edgesFromx1, edgesFromx2):
            return (len(output[y1, [edgesFromx1]].nonzero()[0]) == 0 and
                    len(output[y2, [edgesFromx2]].nonzero()[0]) == 0)

        output = np.array(
            Graph._adjacency_list_to_incidence_matrix(self.adjacency_list))
        node_n = len(output)
        if node_n*(node_n-1)/2 - 2 < len(output[0]):
            warnings.warn(
                "this graph have no free space for randomizing edge", RuntimeWarning)
            return Graph(Graph._incidence_matrix_to_adjacency_list(output))

        for _ in range(rand_it):
            possibilities = list()
            x1, x2, y1, y2 = None, None, None, None
            for i in range(len(output[0])):
                for j in range(i+1, len(output[0])):
                    x1, x2 = output[:, i].nonzero()[0]
                    if ((x1 not in output[:, j].nonzero()[0]) and (x2 not in output[:, j].nonzero()[0])):
                        edgesFromx1 = output[x1].nonzero()[0]
                        edgesFromx2 = output[x2].nonzero()[0]
                        y1, y2 = output[:, j].nonzero()[0]
                        edgesfromx = np.unique(
                            np.concatenate((edgesFromx1, edgesFromx2)))
                        if (_check_if_can_swap(y1, y2, edgesFromx1, edgesFromx2)
                           or
                           _check_if_can_swap(y2, y1, edgesFromx1, edgesFromx2)):
                            possibilities.append((i, j))

            if (not possibilities):
                break
            c1, c2 = random.choice(possibilities)
            x1, x2 = output[:, c1].nonzero()[0]
            y1, y2 = output[:, c2].nonzero()[0]
            edgesFromx1 = output[x1].nonzero()[0]
            edgesFromx2 = output[x2].nonzero()[0]
            if ((not _check_if_can_swap(y1, y2, edgesFromx1, edgesFromx2))
                or (random.randint(0, 1) == 0 and
                    _check_if_can_swap(y2, y1, edgesFromx1, edgesFromx2))):
                output[x1, c1] = 0
                output[x1, c2] = 1
                output[y1, c2] = 0
                output[y1, c1] = 1
            else:
                output[x2, c1] = 0
                output[x2, c2] = 1
                output[y1, c2] = 0
                output[y1, c1] = 1

        return Graph(Graph._incidence_matrix_to_adjacency_list(output))

    @classmethod
    def euler_graph_generator(cls, node: int, edge: int, is_connected: bool = True) -> Self:
        """Generate euler graph.

        Attributes
        -------------
        node : int
        number of nodes
        edge : int
        number of edges"""
        if node < 0 or edge < 0:
            raise ArithmeticError("number of node and edge must be positive")
        output = None
        if is_connected:
            edge -= node
            if edge < 0 or edge+node > node*(node-1)/2:
                raise ArithmeticError(
                    "number of edge is too big or too small for connected graph")
            output = np.ones(node).astype(int)
        else:
            if edge > node*(node-1)/2:
                raise ArithmeticError("number of edge is too big")
            output = np.zeros(node).astype(int)
            output[random.randint(0, node-1)] = 1
            edge -= 1
        for _ in range(edge):
            choices = [i for i in range(node)
                       if (2 * output[i] + 1 <= output.sum() and 2*output[i]+2 < node)]
            if not choices:
                raise ArithmeticError(
                    "number of edge and node can't be used to generate euler graph")
            random_id = random.choice(choices)
            output[random_id] += 1

        output *= 2

        output = list(output)
        result = cls.from_graphic_sequence(output)

        if result is None:
            raise ArithmeticError(
                "number of edge and node can't be used to generate euler graph")

        try:
            if edge+node < node*(node-1)/2:
                result = result.randomize_edges(random.randrange(4))
        except RuntimeWarning:
            pass

        if is_connected:
            while len(result.find_components()) != 1:
                result = result.randomize_edges(random.randrange(1))

        return result

    def euler_cycle_finder(self: Self) -> list:
        """Find euler cycle
        Returns list of nodes number counted from 1"""
        data = self.adjacency_list
        node_id = 0
        while len(data[node_id]) == 0:
            node_id += 1
        id_of_next = -1
        output = list()
        while len(data[node_id]) != 0:
            next_node_id = data[node_id][id_of_next]
            ndata = list([j for j in i if (id not in [node_id, next_node_id]
                         or j not in [node_id, next_node_id])] for id, i in enumerate(data))
            components = [i for i in Graph(ndata).find_components() if len(
                i) > 1 or i[0] == next_node_id]

            if len(components) == 1:
                data = ndata
                output.append(node_id)
                node_id = next_node_id
                id_of_next = -1
            else:
                id_of_next -= 1

        if node_id != 0:
            raise ArithmeticError(
                "graph is not euler graph, but has euler path")

        output.append(node_id)
        return output

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Graph):
            return False

        if self.adjacency_list != other.adjacency_list:
            return False

        return True

    def __repr__(self):
        return f"Graph({self.adjacency_list})"

    def __hash__(self):
        return hash(tuple(frozenset(inner_list) for inner_list in self.adjacency_list))


if __name__ == "__main__":
    pass
