from __future__ import annotations
from typing import Literal
import random


class Graph():
    """a graph with a given representation"""

    def __init__(self,
                 representation: Literal["adjlist", "adjmatrix", "incmatrix"],
                 data: list[list[int]]):
        self.representation = representation
        self.data = data

    @staticmethod
    def parse(representation: Literal["adjlist", "adjmatrix", "incmatrix"], string: str) -> Graph:
        "parse raw string data into a Graph object"
        return Graph(representation,
                     [[int(value) for value in line.split()]
                      for line in string.splitlines()])

    @staticmethod
    def generate_with_gnl_model(n: int, l: int) -> Graph:
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

        return Graph("adjmatrix", output)

    @staticmethod
    def generate_with_gnp_model(n: int, p: float) -> Graph:
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

        return Graph("adjmatrix", output)

    def convert_to(self, representation: Literal["adjlist", "adjmatrix", "incmatrix"]) -> Graph:
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
