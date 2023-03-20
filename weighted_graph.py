from __future__ import annotations


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
