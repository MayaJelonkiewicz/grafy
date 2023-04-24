from __future__ import annotations
from random import randrange
from typing import Self

from graph import Graph, IUndirectedGraph, IWeightedGraph


class WeightedGraph(IUndirectedGraph, IWeightedGraph):
    """A weighted graph stored as an adjacency list"""

    @classmethod
    def parse(cls, string: str) -> Self:
        """Parse raw string data into a WeightedGraph object"""
        adjacency_list = []
        for line in string.splitlines():
            adjacencies = []
            for pair in line.split(","):
                vertex, weight = map(int, pair.strip().split(":"))
                adjacencies.append(IWeightedGraph.Adjacency(vertex, weight))
            adjacency_list.append(adjacencies)
        return cls(adjacency_list)

    @classmethod
    def generate_weighted_connected(cls, n: int, l: int) -> Self:
        """Generate random weighted, connected graph using gnl algorithm.
           Weights are random numbers from 1 to 10 included."""

        # TODO: fix use of 1-indexing

        output = [[] for _ in range(n)]

        if l >= n-1:
            graph = Graph.generate_with_gnl_model(n, l)

            comp_list = graph.find_components()
            comp_list.sort(key=len)

            while (len(comp_list) > 1):
                comp_list.sort(key=len)
                toAdd = comp_list[0]
                mainComp = comp_list[-1]
                prev = comp_list[0][0]

                for i in range(len(toAdd)):
                    v1 = toAdd[i] - 1
                    v2 = mainComp[randrange(0, len(mainComp))] - 1

                    edges = [i for i in range(
                        0, n) if graph.adjacency_list[v2][i] == 1]

                    toDel = graph.adjacency_list[v1].index(
                        1) if 1 in graph.adjacency_list[v1] else None

                    choice = edges[randrange(0, len(edges))]

                    graph.adjacency_list[v1][v2] = graph.adjacency_list[v2][v1] = 1
                    graph.adjacency_list[v2][choice] = graph.adjacency_list[choice][v2] = 0

                    if toDel != None:
                        graph.adjacency_list[v2][toDel] = graph.adjacency_list[toDel][v2] = 0

                    prev = v2

                    comp_list = graph.find_components()

                    mainComp.remove(prev+1)

                    if 1 not in graph.adjacency_list[choice]:
                        mainComp.remove(choice+1)

                    if mainComp == []:
                        mainComp = comp_list[-1]

            adjlist = graph.adjacency_list

            for i in range(n):
                for j in adjlist[i]:
                    weight = randrange(1, 10 + 1)

                    output[i].append(IWeightedGraph.Adjacency(j, weight))
                    output[j-1].append(IWeightedGraph.Adjacency(i + 1, weight))

                    adjlist[j-1].remove(i + 1)
        else:
            raise RuntimeError(
                f"{l = } is too small to make connected graph of {n = } vertexes."
            )

        return cls(output)

    def dijkstra(self, s: int) -> tuple[list, list]:
        """Dijkstra algorithm - finds shortest paths from one vertex to all others in the graph.
        Returns a tuple of two lists, where the first contains the distances to each vertex,
        and the second contains each vertex's predecessor in all shortest paths."""

        def init(g: Self, s: int) -> tuple[list, list]:
            """A function where tables containing distances and predecessors are initialized"""
            d = []
            p = []
            for _ in range(len(g.adjacency_list)):
                d.append(1e7)
                p.append(None)
            d[s] = 0
            return d, p

        def relax(w: int, u: int, d: list, p: list, g: Self) -> tuple[list, list]:
            """Relaxing edges in Dijkstra algorithm"""
            id_u = -1
            for i in range(len(self.adjacency_list[w])):
                if g.adjacency_list[w][i].vertex == u:
                    id_u = i
            if d[w] > d[u]+g.adjacency_list[w][id_u].weight:
                d[w] = d[u]+g.adjacency_list[w][id_u].weight
                p[w] = u
            return d, p

        init_result = init(self, s)
        d = init_result[0]
        p = init_result[1]
        S = []
        Q = []
        for i in range(len(self.adjacency_list)):
            Q.append(i)
        min_d = 1e7
        id = -1
        while len(Q) > 0:
            min_d = 1e7
            for j in range(len(Q)):
                if d[Q[j]] < min_d:
                    min_d = d[Q[j]]
                    id = Q[j]
            S.append(id)
            Q.remove(id)
            for k in range(len(self.adjacency_list[id])):
                w = self.adjacency_list[id][k].vertex
                fl = False
                for l in range(len(Q)):
                    if Q[l] == w:
                        fl = True
                if not fl:
                    continue
                relax_result = relax(w, id, d, p, self)
                d = relax_result[0]
                p = relax_result[1]
        return d, p

    def calculate_all_distances(self) -> list:
        """Finds the distances between each two vertices"""
        final_result = []
        for i in range(len(self.adjacency_list)):
            tab = self.dijkstra(i)[0]
            final_result.append([])
            for j in range(len(tab)):
                final_result[i].append(tab[j])
        return final_result

    def find_min_sum_center(self):
        """Finds the vertex with the smallest sum of distances to the other vertices"""
        tab = self.calculate_all_distances()
        tab_sum = []
        tab_max = []
        for i in range(len(tab)):
            s = 0
            max_val = -1
            for j in range(len(tab[i])):
                s = s+tab[i][j]
                if tab[i][j] > max_val:
                    max_val = tab[i][j]
            tab_sum.append(s)
            tab_max.append(max_val)
        id = -1
        min_sum = 1e7
        for k in range(len(tab_sum)):
            if tab_sum[k] < min_sum:
                min_sum = tab_sum[k]
                id = k
        return id

    def find_min_max_center(self):
        """Finds the vertex with the smallest maximum distance to a vertex"""
        tab = self.calculate_all_distances()
        tab_max = []
        for i in range(len(tab)):
            s = 0
            max_val = -1
            for j in range(len(tab[i])):
                s = s+tab[i][j]
                if tab[i][j] > max_val:
                    max_val = tab[i][j]
            tab_max.append(max_val)
        id = -1
        min_max = 1e7
        for k in range(len(tab_max)):
            if tab_max[k] < min_max:
                min_max = tab_max[k]
                id = k
        return id

    def min_spanning_tree(self) -> WeightedGraph:
        """Finds the minimum spanning tree of a graph using Kruskal's algorithm"""
        def find_set(x: int, parent: list) -> int:
            """A function that finds the set of a given vertex"""
            if x != parent[x]:
                parent[x] = find_set(parent[x], parent)
            return parent[x]

        def union(x: int, y: int, parent: list, rank: list):
            """A function that unites two sets"""
            x_root = find_set(x, parent)
            y_root = find_set(y, parent)
            if rank[x_root] < rank[y_root]:
                parent[x_root] = y_root
            elif rank[x_root] > rank[y_root]:
                parent[y_root] = x_root
            else:
                parent[y_root] = x_root
                rank[x_root] += 1

        parent = list(range(len(self.adjacency_list)))
        rank = [0 for i in range(len(self.adjacency_list))]

        edges = [
            (self.adjacency_list[i][j].weight,
             i, self.adjacency_list[i][j].vertex)
            for i in range(len(self.adjacency_list))
            for j in range(len(self.adjacency_list[i]))
        ]
        edges.sort()
        result = [[] for i in range(len(self.adjacency_list))]
        for edge in edges:
            weight, x_v, y_v = edge
            if find_set(x_v, parent) != find_set(y_v, parent):
                result[x_v].append(IWeightedGraph.Adjacency(y_v, weight))
                result[y_v].append(IWeightedGraph.Adjacency(x_v, weight))
                union(x_v, y_v, parent, rank)
        return WeightedGraph(result)


if __name__ == "__main__":
    pass
