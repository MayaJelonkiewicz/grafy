from __future__ import annotations
from random import randrange
from copy import deepcopy

from graph import IDirectedGraph, IWeightedGraph


class WeightedDigraph(IDirectedGraph, IWeightedGraph):
    """A weighted directed graph stored as an adjacency list"""

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
                    j, randrange(lower, upper)))
            adjacency_list.append(adjacencies)
        return cls(adjacency_list)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, WeightedDigraph):
            return False

        if self.adjacency_list != other.adjacency_list:
            return False

        return True

    def bellman_ford(self, v: int) -> tuple[bool, list]:
        """Bellman-Ford's algorithm. 
        Function prints costs and path from start vertex to every vertex in graph. 
        It also checks if graph contains negative cycle, then function returns False."""
        d = []
        p = []
        for _ in range(self.vertex_count):
            d.append(float('inf'))
            p.append(-1)
        d[v] = 0

        # def print_result(plist, dlist):
        #     tab = []
        #     for i in range(len(dlist)):
        #         print(dlist[i], end=" ")
        #         x = i
        #         while x != -1:
        #             x = plist[x]
        #             if x != -1:
        #                 tab.append(x)
        #         tab.insert(0, i)
        #         print(tab[::-1])
        #         tab = []

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
                # print_result(p, d)
                return True, d
        for x in range(self.vertex_count):
            for g in range(len(self.adjacency_list[x])):
                y = self.adjacency_list[x][g].vertex
                if d[y] > d[x]+self.adjacency_list[x][g].weight:
                    return False, d
        # print_result(p, d)
        return True, d

    def dijkstra(self, v: int) -> list:
        """Dijkstra's algorithm. 
        Function prints costs and path from start vertex to every vertex in graph."""
        d = []
        p = []
        for _ in range(self.vertex_count):
            d.append(float('inf'))
            p.append(-1)
        d[v] = 0

        # def print_result(plist, dlist):
        #     tab = []
        #     for i in range(len(dlist)):
        #         print(dlist[i], end=" ")
        #         x = i
        #         while x != -1:
        #             x = plist[x]
        #             if x != -1:
        #                 tab.append(x)
        #         tab.insert(0, i)
        #         print(tab[::-1])
        #         tab = []

        queue = [v]
        while queue:
            x = queue.pop(0)
            for k in range(len(self.adjacency_list[x])):
                y = self.adjacency_list[x][k].vertex
                if d[y] > d[x]+self.adjacency_list[x][k].weight:
                    d[y] = d[x]+self.adjacency_list[x][k].weight
                    p[y] = x
                    queue.append(y)
        # print_result(p, d)
        return d

    def johnson(self):
        """algorithm for finding all pairs shortest path"""

        # adding a new vertex to the graph
        n = self.vertex_count
        s = [IWeightedGraph.Adjacency(i, 0) for i in range(n)]
        self.adjacency_list.append(s)

        # running Bellman-Ford ,checking for negative cycles
        bellf_success, bellf_d = self.bellman_ford(n)
        if not bellf_success:
            return False

        # removing the new vertex from the graph
        self.adjacency_list.pop()

        # creating a new graph, b-f reweighting
        new_graph = WeightedDigraph(deepcopy(self.adjacency_list))
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
            # printing the results
            print(f"Vertex {i}: {dijkstra_d}")
        # returning the reweighted graph
        return new_graph


if __name__ == "__main__":
    pass
