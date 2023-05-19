from __future__ import annotations
import random
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

        adjacency_list=[]
        for id in range(len(G.adjacency_list)):
            adjacency_list.append([])
            for elem in range(len(G.adjacency_list[id])):
                weight=random.randint(-2,10)
                adjacency_list[id].append((G.adjacency_list[id][elem],weight))
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
                    return False, d
        printResult(p,d)
        return True, d
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Digraph):
            return False

        if self.adjacency_list != other.adjacency_list:
            return False

        return True


if __name__ == "__main__":
    pass
