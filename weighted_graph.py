from __future__ import annotations
from random import randrange
from graph import Graph


class WeightedGraph:
    """A weighted graph stored as an adjacency list"""

    class Adjacency:
        """An entry in the adjacency list of a WeightedGraph"""

        def __init__(self, vertex, weight):
            self.vertex = vertex
            self.weight = weight

        def __repr__(self):
            return f"{self.vertex} {self.weight}"

    def __init__(self, adjacency_list: list[list[Adjacency]]):
        self.adjacency_list = adjacency_list

    @classmethod
    def parse(cls, string: str) -> WeightedGraph:
        """Parse raw string data into a WeightedGraph object"""
        adjacency_list = []
        for line in string.splitlines():
            adjacencies = []
            for pair in line.split(","):
                vertex, weight = map(int, pair.strip().split(":"))
                adjacencies.append(cls.Adjacency(vertex, weight))
            adjacency_list.append(adjacencies)
        return cls(adjacency_list)

    @staticmethod
    def generate_weighted_connected(n: int, l: int) -> WeightedGraph:
        """Generate random weighted, connected graph using gnl algorithm.
           Weights are random numbers from 1 to 10 included."""

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

                    edges = [i for i in range(0, n) if graph.data[v2][i] == 1]

                    toDel = graph.data[v1].index(
                        1) if 1 in graph.data[v1] else None

                    choice = edges[randrange(0, len(edges))]

                    graph.data[v1][v2] = graph.data[v2][v1] = 1
                    graph.data[v2][choice] = graph.data[choice][v2] = 0

                    if toDel != None:
                        graph.data[v2][toDel] = graph.data[toDel][v2] = 0

                    prev = v2

                    comp_list = graph.find_components()

                    mainComp.remove(prev+1)

                    if 1 not in graph.data[choice]:
                        mainComp.remove(choice+1)

                    if mainComp == []:
                        mainComp = comp_list[-1]

            adjlist = graph.convert_to("adjlist").data

            for i in range(n):
                for j in adjlist[i]:
                    weight = randrange(1, 10 + 1)

                    output[i].append(WeightedGraph.Adjacency(j, weight))
                    output[j-1].append(WeightedGraph.Adjacency(i + 1, weight))

                    adjlist[j-1].remove(i + 1)
        else:
            raise RuntimeError(
                f"{l = } is too small to make connected graph of {n = } vertexes."
            )

        return WeightedGraph(output)

    def dijkstra(self, s: int) -> tuple[list, list]:
        """Dijkstra algorithm - finds shortest paths from one vertex to all others in the graph.
        Returns a tuple of two lists, where the first contains the distances to each vertex,
        and the second contains each vertex's predecessor in all shortest paths."""

        def init(g: WeightedGraph, s: int) -> tuple[list, list]:
            """A function where tables containing distances and predecessors are initialized"""
            d = []
            p = []
            for _ in range(len(g.adjacency_list)):
                d.append(1e7)
                p.append(None)
            d[s] = 0
            return d, p

        def relax(w: int, u: int, d: list, p: list, g: WeightedGraph) -> tuple[list, list]:
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


if __name__ == "__main__":
    pass
