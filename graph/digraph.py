from __future__ import annotations
import random
import numpy as np
from typing import Self

from graph import IDirectedGraph, IUnweightedGraph


class Digraph(IDirectedGraph, IUnweightedGraph):
    """A directed graph, stored as an adjacency list"""

    def add_edge(self, vertex_a, vertex_b):
        self.adjacency_list[vertex_a].append(vertex_b)

    def remove_edge(self, vertex_a, vertex_b):
        self.adjacency_list[vertex_a].remove(vertex_b)

    @classmethod
    def generate_with_gnp_model(cls, n: int, p: float) -> Self:
        """Generate digraph using probability"""
        output = [[] for _ in range(n)]

        for i in range(n):
            for j in range(n):
                if random.random() <= p and j != i:
                    output[i].append(j)

        return cls(output)

    def transpose(self) -> Self:
        edges = [(vertex_a, vertex_b) for vertex_a in range(
            self.vertex_count) for vertex_b in self.iter_adjacent(vertex_a)]
        transposed_graph = Digraph.empty(self.vertex_count)
        for edge in edges:
            transposed_graph.add_edge(edge[1], edge[0])
        return transposed_graph

    def find_strongly_connected_components(self) -> set[frozenset[int]]:
        # the order needs to be tracked, but a seperate set object is also
        # used to have O(1) lookup
        visited_vertices = set()
        visited_vertices_in_order = []

        def visit_recursively(vertex: int):
            if vertex in visited_vertices:
                return
            visited_vertices.add(vertex)

            for adjacent_vertex in self.iter_adjacent(vertex):
                visit_recursively(adjacent_vertex)

            visited_vertices_in_order.append(vertex)

        for start_vertex in range(self.vertex_count):
            visit_recursively(start_vertex)

        transposed_graph = self.transpose()
        visited_vertices = set()
        components = set()

        def get_components_recursively(vertex: int, component: set | None = None):
            if vertex in visited_vertices:
                return component
            visited_vertices.add(vertex)

            if component is None:
                component = set()

            component.add(vertex)
            for adjacent_vertex in transposed_graph.iter_adjacent(vertex):
                get_components_recursively(adjacent_vertex, component)
            return component

        for start_vertex in reversed(visited_vertices_in_order):
            component = get_components_recursively(start_vertex)
            if component is not None:
                components.add(frozenset(component))
        return components
    
    @staticmethod
    def Bellman_Ford(n: int, p: float, v: int) -> tuple[bool, list]:
        """Bellman-Ford's algorithm. Function prints costs and path from start vertex to every vertex in graph. 
        It also checks if graph contains negative cycle, then function returns False. Range of edges weights was modified from (-5,10)
        to (-2,10) because with previous range graph often contained negative cycle"""
        index=0
        G=Digraph.generate_with_gnp_model(n,p)
        res=G.find_strongly_connected_components()

        while(len(res)>1 and index<30):
            index+=1
            G=Digraph.generate_with_gnp_model(n,p)
            res=G.find_strongly_connected_components()
        if(index==30):
            tab=[]
            print("Po 30 losowaniach nie udało się uzyskać spójnego grafu. Proszę powtórzyć wywołanie funkcji lub zwiększyć wartość parametru p")
            return False,tab
        adjacency_list=[]
        for id in range(len(G.adjacency_list)):
            adjacency_list.append([])
            for elem in range(len(G.adjacency_list[id])):
                weight=random.randint(-2,10)
                adjacency_list[id].append((G.adjacency_list[id][elem],weight))
        print("Lista sąsiedztwa wraz z wagami")
        print(adjacency_list)
        d = []
        p = []
        for i in range(n):
            d.append(1e7)
            p.append(-1)
        d[v] = 0
        def printResult(pList,dList):
            tab=[]
            for i in range(len(dList)):
                print (dList[i] ,end=" ")
                x=i
                while(x!=-1):
                    x=pList[x]
                    if(x!=-1):
                        tab.append(x)
                tab.insert(0,i)
                print(tab[::-1])
                tab=[]
                
        for j in range(1, n):
            test = True
            for x in range(n):
                for k in range(len(adjacency_list[x])):
                    y = adjacency_list[x][k][0]
                    if d[y] > d[x]+adjacency_list[x][k][1]:
                        test = False
                        d[y] = d[x]+adjacency_list[x][k][1]
                        p[y] = x
            if test == True:
                printResult(p,d)
                return True, d
        for x in range(n):
            for g in range(len(adjacency_list[x])):
                y = adjacency_list[x][g][0]
                if d[y] > d[x]+adjacency_list[x][g][1]:
                    print("Graf zawiera ujemny cykl")
                    return False, d
        printResult(p,d)
        return True, d

    def PageRank_Random(self, N: int):
        """PageRank algorithm with random walk"""   
        visits = np.zeros(self.vertex_count)
        choice = random.randint(0, self.vertex_count-1)
        d = 0.15

        for _ in range(N):
            rand = random.random()

            if rand < (1 - d):
                choice = self.adjacency_list[choice][random.randint(0, len(self.adjacency_list[choice]) - 1)]
                visits[choice] += 1
            else:
                choice = random.randint(0, self.vertex_count - 1)
                visits[choice] += 1

        visits = visits / N
        res = {}
        for i in range(len(visits)):
            res[f'{chr(i + ord("A"))}'] = round(visits[i], 6)

        return sorted(res.items(), key=lambda x:x[1], reverse=True)

    def PageRank_PowerMethod(self: Digraph, N: int, eps=1e-8):
        """PageRank algorithm using power method"""

        adj_mat = [[0 for _ in range(self.vertex_count)] for _ in range(self.vertex_count)]
        d = 0.15

        for i in range(self.vertex_count):
            for j in range(len(self.adjacency_list[i])):
                v = self.adjacency_list[i][j]
                adj_mat[i][v] = 1

        v_degrees = [len(self.adjacency_list[i]) for i in range(self.vertex_count)]

        P = [[0 for _ in range(self.vertex_count)] for _ in range(self.vertex_count)]
        
        p0 = [ 1. / self.vertex_count for _ in range(self.vertex_count)]
        p0_next = []

        for i in range(len(adj_mat)):
            for j in range(len(adj_mat[i])):
                P[i][j] = (1 - d)*(adj_mat[i][j]/v_degrees[i]) + (d / self.vertex_count)

        # print(P)
        N=10
        for i in range(N):
            if i != 0: 
                p0 = p0_next

            p0_next = np.dot(p0, P)

            sub = np.subtract(p0, p0_next)

            check = np.sqrt(sum(sub**2))

            if check < eps:
                break
            

        res = {}
        for i in range(len(p0_next)):
            res[f'{chr(i + ord("A"))}'] = round(p0_next[i], 6)

        return sorted(res.items(), key=lambda x:x[1], reverse=True) 

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Digraph):
            return False

        if self.adjacency_list != other.adjacency_list:
            return False

        return True


if __name__ == "__main__":
    pass
