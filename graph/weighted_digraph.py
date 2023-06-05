from __future__ import annotations
import ctypes
import random
from copy import deepcopy
import networkx as nx
import matplotlib.pyplot as plt
from typing import Self
from graph import IDirectedGraph, IWeightedGraph


class WeightedDigraph(IDirectedGraph, IWeightedGraph):
    """A weighted directed graph stored as an adjacency list"""

    _approximate_tsp = None

    def add_edge(self, vertex_a, vertex_b, weight):
        self.adjacency_list[vertex_a].append(
            IWeightedGraph.Adjacency(vertex_b, weight))

    def remove_edge(self, vertex_a, vertex_b):
        self.adjacency_list[vertex_a] = [
            a for a in self.adjacency_list[vertex_a] if a.vertex != vertex_b]

    @classmethod
    def generate_weighted_digraph(cls, digraph, lower, upper):
        """Generate random weighted digraph using digraph."""
        adjacency_list = []
        for i in digraph.adjacency_list:
            adjacencies = []
            for j in i:
                adjacencies.append(IWeightedGraph.Adjacency(
                    j, random.randrange(lower, upper)))
            adjacency_list.append(adjacencies)
        return cls(adjacency_list)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, WeightedDigraph):
            return False

        if self.adjacency_list != other.adjacency_list:
            return False

        return True

    def bellman_ford(self, v: int, verbose: bool = False) -> tuple[bool, list]:
        """Bellman-Ford's algorithm. 
        Function prints costs and path from start vertex to every vertex in graph. 
        It also checks if graph contains negative cycle, then function returns False."""
        d = []
        p = []
        for _ in range(self.vertex_count):
            d.append(float('inf'))
            p.append(-1)
        d[v] = 0

        for _ in range(1, self.vertex_count):
            test = True
            for x in range(self.vertex_count):
                for k in range(len(self.adjacency_list[x])):
                    y = self.adjacency_list[x][k].vertex
                    if d[y] > d[x]+self.adjacency_list[x][k].weight:
                        test = False
                        d[y] = d[x]+self.adjacency_list[x][k].weight
                        p[y] = x
            if test is True:
                if verbose:
                    self.__print_result(p, d)
                return True, d
        for x in range(self.vertex_count):
            for g in range(len(self.adjacency_list[x])):
                y = self.adjacency_list[x][g].vertex
                if d[y] > d[x]+self.adjacency_list[x][g].weight:
                    return False, d
        if verbose:
            self.__print_result(p, d)
        return True, d

    def dijkstra(self, v: int, verbose: bool = False) -> list:
        """Dijkstra's algorithm. 
        Function prints costs and path from start vertex to every vertex in graph.
        """
        d = []
        p = []
        for _ in range(self.vertex_count):
            d.append(float('inf'))
            p.append(-1)
        d[v] = 0

        queue = [v]
        while queue:
            x = queue.pop(0)
            for k in range(len(self.adjacency_list[x])):
                y = self.adjacency_list[x][k].vertex
                if d[y] > d[x]+self.adjacency_list[x][k].weight:
                    d[y] = d[x]+self.adjacency_list[x][k].weight
                    p[y] = x
                    queue.append(y)
        if verbose:
            self.__print_result(p, d)
        return d

    def johnson(self, verbose: bool = False) -> list[list] | None:
        """algorithm for finding all pairs shortest path"""

        # adding a new vertex to the graph
        n = self.vertex_count
        s = [IWeightedGraph.Adjacency(i, 0) for i in range(n)]
        self.adjacency_list.append(s)

        # running Bellman-Ford ,checking for negative cycles
        bellf_success, bellf_d = self.bellman_ford(n)
        if not bellf_success:
            return None

        # removing the new vertex from the graph
        self.adjacency_list.pop()

        # creating a new graph, b-f reweighting
        new_graph = WeightedDigraph(deepcopy(self.adjacency_list))
        d = []
        for i in range(self.vertex_count):
            for j in range(len(new_graph.adjacency_list[i])):
                new_graph.adjacency_list[i][j].weight = new_graph.adjacency_list[i][j].weight + \
                    bellf_d[i] - bellf_d[new_graph.adjacency_list[i][j].vertex]

        # running Dijkstra and reweighting
        for i in range(self.vertex_count):
            dijkstra_d = new_graph.dijkstra(i)
            for j in range(self.vertex_count):
                if dijkstra_d[j] != float('inf'):
                    dijkstra_d[j] = dijkstra_d[j] + bellf_d[j] - bellf_d[i]
            d.append(dijkstra_d)

        # printing reweighted graph
        if verbose:
            print("--------------------")
            print(f"Reweighted Graph:")
            print(new_graph)
            print("--------------------")
        # returning result matrix
        return d

    def Edmonds_Karp(self, s: int, t: int, name: str) -> int:
        """Edmonds-Karp algorithm, returns maximum flow in digraph."""
        # https://eduinf.waw.pl/inf/alg/001_search/0146.php
        adjacency_list = []
        for i in range(len(self.adjacency_list)):
            adjacency_list.append([])
            for j in range(len(self.adjacency_list[i])):
                elem = self.adjacency_list[i][j]
                adjacency_list[i].append((elem.vertex, elem.weight))
        n = len(self.adjacency_list)
        fmax = 0
        F = [[0 for i in range(n)] for j in range(n)]
        C = [[0 for i in range(n)] for j in range(n)]
        P = [0 for i in range(n)]
        CFP = [0 for i in range(n)]
        Q = []
        for i in range(len(adjacency_list)):
            for j in range(len(adjacency_list[i])):
                C[i][adjacency_list[i][j][0]] = adjacency_list[i][j][1]
        while (True):
            for i in range(n):
                P[i] = -1
            P[s] = -2
            CFP[s] = 1e7
            while (len(Q) > 0):
                Q.pop(0)
            Q.append(s)
            esc = False
            while (len(Q) > 0):
                x = Q.pop(0)
                for k in range(n):
                    cp = C[x][k]-F[x][k]
                    if (cp and (P[k] == -1)):
                        P[k] = x
                        if CFP[x] > cp:
                            CFP[k] = cp
                        else:
                            CFP[k] = CFP[x]
                        if k == t:
                            fmax = fmax+CFP[t]
                            l = k
                            while l != s:
                                x = P[l]
                                F[x][l] = F[x][l]+CFP[t]
                                F[l][x] = F[l][x]-CFP[t]
                                l = x
                            esc = True
                            break
                        Q.append(k)
                if esc == True:
                    break
            if esc == False:
                break
        print("Wartość maksymalnego przepływu to:" + str(fmax))

        G = nx.DiGraph()
        for i in range(0, n):
            G.add_node(i)
        for i in range(len(adjacency_list)):
            for j in range(len(adjacency_list[i])):
                if (G.has_edge(adjacency_list[i][j][0], i) == False):
                    G.add_edge(i, adjacency_list[i][j][0])
        pos = nx.circular_layout(G)
        nx.draw(G, pos=pos, with_labels=True)
        edge_labels = {}
        for i in range(len(adjacency_list)):
            for j in range(len(adjacency_list[i])):
                edge_labels[(i, adjacency_list[i][j][0])] = str(
                    F[i][adjacency_list[i][j][0]])+"/"+str(adjacency_list[i][j][1])
        nx.draw_networkx_edge_labels(G, pos, edge_labels)

        plt.savefig(name+".png")
        plt.clf()
        return fmax

    @classmethod
    def generate_flow_graph(cls, n: int) -> Self:
        """Generate flow graph
        with n layers of vertices with n vertices each"""
        # output = [[] for _ in range(N*N + 2)]

        if n < 2:
            raise ValueError("N must be greater than 1")

        layers = [[[] for _ in range(random.randint(2, n))] for _ in range(n)]

        counter = 1
        for i in range(n-1):
            l = list(range(len(layers[i])))
            r = list(range(len(layers[i+1])))
            counter += len(layers[i])
            while l or r:
                v1 = None
                v2 = None
                if l:
                    v1 = random.choice(l)
                    l.remove(v1)
                else:
                    v1 = random.randint(0, len(layers[i])-1)

                if r:
                    v2 = random.choice(r)
                    r.remove(v2)
                else:
                    v2 = random.randint(0, len(layers[i+1])-1)

                layers[i][v1].append(IWeightedGraph.Adjacency(v2 + counter, random.randint(1, 10)))

        counter += len(layers[n-1])
        for i in range(len(layers[n-1])):
            layers[n-1][i].append(IWeightedGraph.Adjacency(counter, random.randint(1, 10)))

        basin = [IWeightedGraph.Adjacency(i+1, random.randint(1, 10))
                 for i in range(len(layers[0]))]
        output = [basin] + [vertex for layer in layers for vertex in layer] + [[]]

        possibilities = [(j + 1,i + 1) for j in range(counter-1) for i in range(j+1, counter-1)
                         if i != j] + \
                        [(0,i) for i in range(1, counter)] + \
                        [(i,counter) for i in range(1, counter)]

        for vertex in range(0,len(output)):
            for adj in output[vertex]:
                a = adj.vertex
                b = vertex
                if a > b:
                    a,b = b,a
                try:
                    possibilities.remove((a,b))
                except ValueError:
                    pass

        new_vertices = random.sample(possibilities, 2*n)
        for i in new_vertices:
            a = i[0]
            b = i[1]
            if random.randint(0,1) == 0:
                a,b = b,a
            if b == 0 or a == counter:
                a,b = b,a
            output[a].append(IWeightedGraph.Adjacency(b, random.randint(1, 10)))

        return WeightedDigraph(output)

    @staticmethod
    def __print_result(plist, dlist):
        tab = []
        for i in range(len(dlist)):
            print(dlist[i], end=" ")
            x = i
            while x != -1:
                x = plist[x]
                if x != -1:
                    tab.append(x)
            tab.insert(0, i)
            print(tab[::-1])
            tab = []

    @classmethod
    def find_approximate_2d_tsp_solution(cls, points, temperature_iteration_count, inner_iteration_count) -> list[int]:
        """Finds an approximate solution for the travelling salesman problem in 2 dimensions
        Returns the solution as an ordering of indices into the provided list of points."""

        class CPoint(ctypes.Structure):
            """ctypes-compatible structure for a 2-dimensional point"""
            _fields_ = [("x", ctypes.c_int), ("y", ctypes.c_int)]

        if cls._approximate_tsp is None:
            cls._approximate_tsp = ctypes.CDLL("tsp/libtsp.so").approximate_tsp
            cls._approximate_tsp.argtypes = ctypes.POINTER(
                CPoint), ctypes.c_size_t, ctypes.c_int
            cls._approximate_tsp.restype = ctypes.POINTER(ctypes.c_int)

        points_array = (CPoint * len(points))()
        for index, point in enumerate(points):
            points_array[index] = CPoint(point[0], point[1])

        # pylint: disable=not-callable
        order_array = cls._approximate_tsp(
            points_array,
            len(points),
            temperature_iteration_count,
            inner_iteration_count,
        )
        return [order_array[i] for i in range(len(points))]


if __name__ == "__main__":
    pass
