from unittest import TestCase

from graph import Graph


class GraphTestCase(TestCase):
    """Test Graph class"""

    def test_parse_with_representation(self):
        representations = ["adjlist", "adjmatrix", "incmatrix"]

        graphs = []
        for representation in representations:
            with open(f"test/resources/graph_representations/{representation}.txt", "r",
                      encoding="utf-8") as file:
                graphs.append(Graph.parse(
                    representation, file.read()))  # type: ignore

        # check if all graphs are equal
        for g0, g1 in zip(graphs, graphs[1:]):
            self.assertEqual(g0, g1)

    def test_dump_with_representation(self):
        representations = ["adjlist", "adjmatrix", "incmatrix"]

        with open("test/resources/graph_representations/adjlist.txt", "r", encoding="utf-8") as file:
            graph = Graph.parse(
                "adjlist", file.read())

        for representation in representations:
            with open(f"test/resources/graph_representations/{representation}.txt", "r",
                      encoding="utf-8") as file:
                self.assertEqual(graph.dump(representation),  # type: ignore
                                 file.read())
