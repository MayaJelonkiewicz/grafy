from __future__ import annotations
from random import randrange
from copy import deepcopy
import networkx as nx
import matplotlib.pyplot as plt
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

    def johnson(self, verbose: bool = False):
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
            if verbose:
                print(f"Vertex {i}: {dijkstra_d}")
        # returning the reweighted graph
        return new_graph
    
    def Edmonds_Karp(self, s: int, t: int,name:str) -> int:
        """Edmonds-Karp algorithm, returns maximum flow in digraph."""
        adjacency_list=[]
        for i in range(len(self.adjacency_list)):
            adjacency_list.append([])
            for j in range(len(self.adjacency_list[i])):
                elem=self.adjacency_list[i][j]
                adjacency_list[i].append((elem.vertex,elem.weight))
        n=len(self.adjacency_list)
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


if __name__ == "__main__":
    pass
