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

    @staticmethod
    def generate_with_gnp_model(n: int, p: float) -> Digraph:
        """Generate digraph using probability"""
        output = [[] for _ in range(n)]

        for i in range(n):
            for j in range(1,n+1):
                
                if rand.random() <= p and j-1 != i:
                    output[i].append(j)

        return Digraph(output)


    def data_to_string(self) -> str:
        string = ""
        for row in self.adjacency_list:
            string += " ".join(map(lambda v: f"{v}", row)) + "\n"
        return string

if __name__ == "__main__":
    pass
