class Digraph:
    """A directed graph, stored as an adjacency list"""

    def __init__(self, adjacency_list: list[list[int]]):
        self.adjacency_list = adjacency_list

    @property
    def vertex_count(self):
        return len(self.adjacency_list)

    @property
    def edge_count(self):
        return sum(map(len, self.adjacency_list))

    def iterate_arcs(self):
        """Iterate over all the arcs in the graph.
        Returns an iterator of tuples (x, y) corresponding to arcs directed from x to y."""
        for first_edge, second_edges in enumerate(self.adjacency_list):
            for second_edge in second_edges:
                yield first_edge, second_edge

    @classmethod
    def parse(cls, string: str):
        """Parse raw string data into a Digraph object"""
        return cls([[int(value) for value in line.split()] for line in string.splitlines()])


if __name__ == "__main__":
    pass
