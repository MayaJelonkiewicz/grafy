from __future__ import annotations
from random import randrange
from typing import Self

from graph import Graph, IUndirectedGraph, IWeightedGraph


class WeightedGraph(IUndirectedGraph, IWeightedGraph):
    """A weighted graph stored as an adjacency list"""

    def add_edge(self, vertex_a, vertex_b, weight):
        self.adjacency_list[vertex_a].append(
            IWeightedGraph.Adjacency(vertex_b, weight))
        self.adjacency_list[vertex_b].append(
            IWeightedGraph.Adjacency(vertex_a, weight))

    def remove_edge(self, vertex_a, vertex_b):
        self.adjacency_list[vertex_a] = [
            a for a in self.adjacency_list[vertex_a] if a.vertex != vertex_b]
        self.adjacency_list[vertex_b] = [
            a for a in self.adjacency_list[vertex_b] if a.vertex != vertex_a]

    @classmethod
    def generate_weighted_connected(cls, n: int, l: int) -> Self:
        """Generate random weighted, connected graph using gnl algorithm.
           Weights are random numbers from 1 to 10 included."""

        output = [[] for _ in range(n)]

        if l >= n-1:
            graph = Graph.generate_with_gnl_model(n, l)

            comp_list = graph.find_components()
            comp_list.sort(key=len)

            adj_mat = Graph.adjacency_list_to_adjacency_matrix(
                graph.adjacency_list)

            while len(comp_list) > 1:
                adj_mat = Graph.adjacency_list_to_adjacency_matrix(
                    graph.adjacency_list)
                comp_list.sort(key=len)
                to_add = comp_list[0]
                main_comp = comp_list[-1]
                prev = comp_list[0][0]

                for i in range(len(to_add)):
                    v1 = to_add[i]
                    v2 = main_comp[randrange(0, len(main_comp))]

                    edges = [i for i in range(
                        0, n) if adj_mat[v2][i] == 1]

                    to_del = adj_mat[v1].index(
                        1) if 1 in adj_mat[v1] else None

                    choice = edges[randrange(0, len(edges))]

                    adj_mat[v1][v2] = adj_mat[v2][v1] = 1
                    adj_mat[v2][choice] = adj_mat[choice][v2] = 0

                    if to_del is not None:
                        adj_mat[v2][to_del] = adj_mat[to_del][v2] = 0

                    prev = v2

                    graph.adjacency_list = Graph.adjacency_matrix_to_adjacency_list(
                        adj_mat)
                    comp_list = graph.find_components()

                    main_comp.remove(prev)

                    if 1 not in adj_mat[choice]:
                        main_comp.remove(choice)

                    if main_comp == []:
                        main_comp = comp_list[-1]

            adjlist = graph.adjacency_list

            for i in range(n):
                for j in adjlist[i]:
                    weight = randrange(1, 10 + 1)

                    output[i].append(IWeightedGraph.Adjacency(j, weight))
                    output[j].append(IWeightedGraph.Adjacency(i, weight))

                    adjlist[j].remove(i)
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
        s_list = []
        q_list = []
        for i in range(len(self.adjacency_list)):
            q_list.append(i)
        min_d = 1e7
        id = -1
        while len(q_list) > 0:
            min_d = 1e7
            for j in range(len(q_list)):
                if d[q_list[j]] < min_d:
                    min_d = d[q_list[j]]
                    id = q_list[j]
            s_list.append(id)
            q_list.remove(id)
            for k in range(len(self.adjacency_list[id])):
                w = self.adjacency_list[id][k].vertex
                fl = False
                for l in range(len(q_list)):
                    if q_list[l] == w:
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

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, WeightedGraph):
            return False

        if self.adjacency_list != other.adjacency_list:
            return False

        return True


if __name__ == "__main__":
    pass
