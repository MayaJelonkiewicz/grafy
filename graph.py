from __future__ import annotations
from typing import Literal, Self
import random
import warnings
import numpy as np


class Graph:
    """A graph with a given representation"""

    def __init__(self,
                 representation: Literal["adjlist", "adjmatrix", "incmatrix"],
                 data: list[list[int]]):
        self.representation = representation
        self.data = data

    @classmethod
    def parse(cls, representation: Literal["adjlist", "adjmatrix", "incmatrix"], string: str) -> Self:
        "parse raw string data into a Graph object"
        return cls(representation,
                     [[int(value) for value in line.split()]
                      for line in string.splitlines()])

    @classmethod
    def generate_with_gnl_model(cls, n: int, l: int) -> Self:
        """Generate graph using number of edges"""
        output = [[0 for _ in range(n)] for _ in range(n)]

        if 0 < l < n*(n-1)/2:
            while l > 0:
                row = random.randrange(0, n)
                col = random.randrange(1, n)

                if row != col:
                    if output[row][col] == 0:
                        output[row][col] = 1
                        output[col][row] = 1
                        l -= 1
        elif l == n*(n-1)/2:
            for i in range(n):
                for j in range(i+1, n):
                    output[i][j] = output[j][i] = 1
        else:
            raise RuntimeError(
                f"{l = } is too large for graph where {n = }")

        return cls("adjmatrix", output)

    @classmethod
    def generate_with_gnp_model(cls, n: int, p: float) -> Self:
        """Generate graph using probability"""
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

        return cls("adjmatrix", output)

    @classmethod
    def generate_random_regular(cls, n, k) -> Self:
        if n <= k:
            raise ValueError('n <= k')

        if k % 2 == 1 and n % 2 == 1:
            raise ValueError('both k and n are odd')

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

        return cls('adjlist', output)

    def convert_to(self, representation: Literal["adjlist", "adjmatrix", "incmatrix"]) -> Self:
        """convert graph to a given representation. returns the new Graph object"""
        conversion_functions = {
            ("adjlist", "adjmatrix"):
                Graph._adjacency_list_to_adjacency_matrix,
            ("adjlist", "incmatrix"):
                Graph._adjacency_list_to_incidence_matrix,
            ("adjmatrix", "adjlist"):
                Graph._adjacency_matrix_to_adjacency_list,
            ("adjmatrix", "incmatrix"):
                Graph._adjacency_matrix_to_incidence_matrix,
            ("incmatrix", "adjlist"):
                Graph._incidence_matrix_to_adjacency_list,
            ("incmatrix", "adjmatrix"):
                Graph._incidence_matrix_to_adjacency_matrix,
        }

        if self.representation == representation:
            # fmt: off
            conversion_function = lambda d: d # no conversion needed
            # fmt: on
        elif (self.representation, representation) in conversion_functions:
            conversion_function = conversion_functions[(
                self.representation, representation)]  # type: ignore
        else:
            raise RuntimeError(
                f"conversion not implemented: {self.representation} to {representation}")

        return Graph(representation, conversion_function(self.data))

    def data_to_string(self) -> str:
        string = ""
        for row in self.data:
            string += " ".join(map(lambda v: f"{v}", row)) + "\n"
        return string

    @staticmethod
    def _adjacency_matrix_to_adjacency_list(input: list[list[int]]) -> list[list[int]]:
        """transform 'adjacency matrix' to 'adjacency list'"""
        output = []
        for i in input:
            row = []
            for id, j in enumerate(i):
                if j == 1:
                    row.append(id+1)
            output.append(row)
        return output

    @staticmethod
    def _adjacency_list_to_adjacency_matrix(input: list[list[int]]) -> list[list[int]]:
        """transform 'adjacency list' to 'adjacency matrix'"""
        node_amount = len(input)
        output = [[0 for i in range(node_amount)] for j in range(node_amount)]
        for iid, i in enumerate(input):
            for j in i:
                output[iid][j-1] = 1
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
                    output[j-1][col_it] = 1
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
                        output[id].append(j+1)
                        output[j].append(id+1)
                        break
                    else:
                        id = j
        output = list(map(sorted, output))  # sort rows
        return output

    @staticmethod
    def _incidence_matrix_to_adjacency_matrix(input: list[list[int]]) -> list[list[int]]:
        """transform 'incidence matrix' to 'adjacency matrix'"""
        n = len(input)
        k = len(input[0])
        output = []
        for l in range(n):
            output.append([])
            for _ in range(n):
                output[l].append(0)
        for i in range(k):
            u = 0
            v = 0
            for j in range(n):
                if (input[j][i] == 1 and u != 0):
                    v = j+1
                if (input[j][i] == 1 and u == 0):
                    u = j+1

            if (u != 0 and v != 0):
                output[u-1][v-1] = 1
                output[v-1][u-1] = 1
        return output

    @staticmethod
    def _adjacency_matrix_to_incidence_matrix(input: list[list[int]]) -> list[list[int]]:
        """transform 'adjacency matrix' to 'incidence matrix'"""
        n = len(input)
        idx = 0
        for i in range(n):
            for j in range(n):
                if input[i][j] == 1:
                    idx = idx+1

        output = []
        for k in range(n):
            output.append([])
            for _ in range(idx//2):
                output[k].append(0)
        nr_krawedzi = 0
        znaleziono = False
        for a in range(n):
            for b in range(n):
                if input[a][b] == 1:
                    for c in range(idx//2):
                        if output[a][c] == 1 and output[b][c] == 1:
                            znaleziono = True
                    if not znaleziono:
                        output[a][nr_krawedzi] = 1
                        output[b][nr_krawedzi] = 1
                        nr_krawedzi = nr_krawedzi+1
                    znaleziono = False
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
    def from_graphic_sequence(cls,
                              representation: Literal["adjlist", "adjmatrix", "incmatrix"],
                              sequence: list[int]) -> Self | None:
        if not sequence:
            # a sequence of length 0 corresponds to a graph with no vertices
            return cls(representation, [])

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
                return cls('adjlist', adjacency_list).convert_to(representation)

            if min(remaining_edges) < 0:
                # one of the vertices has more incident edges than its
                # target degree
                return None

            # create edges between the vertex with the largest number of remaining
            # edges n and the n next vertices with the largest number of remaining
            # edges
            for index in range(1, remaining_edges[0] + 1):
                remaining_edges[index] -= 1
                adjacency_list[vertex_indices[0]].append(
                    vertex_indices[index] + 1)
                adjacency_list[vertex_indices[index]].append(
                    vertex_indices[0] + 1)
            remaining_edges[0] = 0

    def find_components(self):
        """Function, which finds components of the graph and prints the number of the largest one.
        Its argument is a neighbour list."""

        def components_r(nr: int, v: int, g: list[list[int]], comp: list) -> None:
            for i in range(len(g[v])):
                if comp[g[v][i]-1] == -1:
                    comp[g[v][i]-1] = nr
                    components_r(nr, g[v][i]-1, g, comp)

        adjacency_list = self.convert_to('adjlist').data

        nr = 0
        comp = []
        for i in range(len(adjacency_list)):
            comp.append(-1)
        for i in range(len(adjacency_list)):
            if comp[i] == -1:
                nr = nr+1
                comp[i] = nr
                components_r(nr, i, adjacency_list, comp)

        components = [[] for _ in range(nr)]
        for vertex_index, component_index in enumerate(comp):
            components[component_index - 1].append(vertex_index + 1)
        return components

    def find_hamiltonian_cycle(self):
        adjacency_list = self.convert_to('adjlist').data
        return self._dfs_hamilton_recursive(adjacency_list, 1, [0 for _ in adjacency_list], [])

    @classmethod
    def _dfs_hamilton_recursive(cls, adjacency_list: list[list[int]], vertex: int,
                                visited: list[int], s: list) -> list[int] | None:
        """A function that returns a Hamiltonian cycle of the graph if one exists,
        or None otherwise"""
        s.append(vertex)
        if len(s) < len(adjacency_list):
            visited[vertex-1] = True
            for i in range(len(adjacency_list[vertex-1])):
                if not visited[adjacency_list[vertex-1][i]-1]:
                    result = cls._dfs_hamilton_recursive(
                        adjacency_list, adjacency_list[vertex-1][i], visited, s)
                    if result is not None:
                        return result
            visited[vertex-1] = False
            s.pop()
        else:
            for i in range(len(adjacency_list[vertex-1])):
                if adjacency_list[vertex-1][i]-1 == 0:
                    return s

            s.pop()

        return None

    def randomize_edges(self, rand_it: int, max_rerolling_attempt: int = 99) -> Self:
        """
        A function that returns graph with rerandomized edges, nodes degree is kept.

        Attributes
        -------------
        rand_it : int
        number of randomization
        max_rerolling_attempt : int, optional
        how much attempts in finding swap pair before abandoning (default is 99)
        """
        output = self.convert_to('incmatrix').data
        node_n = len(output)
        if node_n*(node_n-1)/2 - 2 < len(output[0]):
            warnings.warn(
                'this graph have no free space for randomizing edge', RuntimeWarning)
            return Graph('incmatrix', output)

        x_1, x_2, y_1, y_2 = None, None, None, None
        c_1, c_2 = None, None
        rer_att = max_rerolling_attempt
        for _ in range(rand_it):
            while True:
                if rer_att == 0:
                    warnings.warn('failed to find pair of edges to swap in a max_rerolling_attempt',
                                  RuntimeWarning)
                    return Graph('incmatrix', output)
                rer_att -= 1
                try:
                    c_1 = random.randint(0, len(output[0])-1)
                    x_1, x_2 = (i for i in range(len(output))
                              if output[i][c_1] == 1)
                    c_2 = random.choices([i for i in range(len(output[0])) if (
                        output[x_1][i] != 1 and output[x_2][i] != 1)])[0]
                    y_1, y_2 = (i for i in range(len(output))
                              if output[i][c_2] == 1)
                    if random.getrandbits(1):
                        y_1, y_2 = y_2, y_1
                    tmp = [i for i in range(len(output[0]))
                           if
                            (output[x_1][i] == 1 and output[y_1][i] == 1) or
                            (output[x_2][i] == 1 and output[y_2][i] == 1)]
                    if len(tmp) == 0:
                        break
                except IndexError:
                    pass

            output[x_2][c_1] = 0
            output[y_1][c_2] = 0
            output[y_1][c_1] = 1
            output[x_2][c_2] = 1

        return Graph('incmatrix', output)

    @classmethod
    def euler_graph_generator(cls, node: int, edge: int) -> Self:
        """Generate euler graph.

        Attributes
        -------------
        node : int
        number of nodes
        edge : int
        number of edges"""
        edge -= node
        if edge < 0 or edge+node > node*(node-1)/2:
            raise ArithmeticError("")
        output = np.ones(node).astype(int)
        for _ in range(edge):
            random_id = random.randrange(0, node)
            while (2 * output[random_id] + 1 > output.sum() or 2*output[random_id]+2 > node):
                random_id = random.randrange(0, node)
            output[random_id] += 1

        output *= 2

        output = list(output)
        result = cls.from_graphic_sequence('adjlist', output)
        if edge+node < node*(node-1)/2:
            result = result.randomize_edges(random.randrange(4))

        return result


    def euler_cycle_finder(self: Self) -> list:
        """Find euler cycle
        Returns list of nodes number counted from 1"""
        data = self.convert_to('adjlist').data
        node_id = 0
        while len(data[node_id]) == 0:
            node_id += 1
        id_of_next = -1
        output = list()
        while len(data[node_id]) != 0:
            next_node_id = data[node_id][id_of_next]-1
            ndata = list([j for j in i
                        if (id not in [node_id, next_node_id] or j-1 not in [node_id, next_node_id])
                        ]for id, i in enumerate(data))
            components = [i for i in Graph('adjlist', ndata).find_components() if len(
                i) > 1 or i[0] == next_node_id+1]

            if len(components) == 1:
                data = ndata
                output.append(node_id+1)
                node_id = next_node_id
                id_of_next = -1
            else:
                id_of_next -= 1

        output.append(node_id+1)
        return output

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Graph):
            return False

        if self.representation != other.representation:
            return False

        if str(self.data) != str(other.data):
            return False

        return True

    def __repr__(self):
        return f"Graph({self.representation}, {self.data})"


if __name__ == "__main__":
    pass
