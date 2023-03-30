from unittest import TestCase

from graph import Graph


class GraphTestCase(TestCase):
    """Test Graph class"""

    def test_representation_conversions(self):
        representations = ["adjlist", "adjmatrix", "incmatrix"]

        graphs = {}
        for representation in representations:
            with open(f"test/resources/graph_representations/{representation}.txt", "r",
                      encoding="utf-8") as file:
                graphs[representation] = Graph.parse(
                    representation, file.read())  # type: ignore

        for first_representation in representations:
            for second_representation in representations:
                self.assertEqual(
                    graphs[first_representation].convert_to(
                        second_representation),
                    graphs[second_representation]
                )
