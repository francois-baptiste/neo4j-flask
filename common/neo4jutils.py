from datetime import datetime
from .text_utils import TextCleanUp


class Neo4jUtils(object):

    def __init__(self, graph):
        self.graph = graph
        return

    @staticmethod
    def get_neo_prop(text: str) -> str:
        return TextCleanUp.remove_double_whitespace(TextCleanUp.remove_punctuation(text.lower())).replace(" ", "_")

    @staticmethod
    def timestamp() -> float:
        epoch = datetime.utcfromtimestamp(0)
        now = datetime.now()
        delta = now - epoch
        return delta.total_seconds()

    @staticmethod
    def date() -> str:
        return datetime.now().strftime('%Y-%m-%d')

    @staticmethod
    def get_neo_label(text: str) -> str:
        return TextCleanUp.remove_double_whitespace(TextCleanUp.remove_punctuation(text.upper())).replace(" ", "_")

    def create_graph_unique_constraint(self, label, property_key):
        graph = self.graph

        label = self.get_neo_label(label)
        property_key = self.get_neo_prop(property_key)
        
        if property_key not in graph.schema.get_indexes(label):
            if property_key not in graph.schema.get_uniqueness_constraints(label):
                graph.schema.create_uniqueness_constraint(label, property_key)
                print("Created unqiue constraint", label, property_key)

    def create_graph_index(self, label, property_key):
        graph = self.graph

        label = self.get_neo_label(label)
        property_key = self.get_neo_prop(property_key)

        if property_key not in graph.schema.get_indexes(label):
            graph.schema.create_index(label, property_key)
            print("Created index constraint", label, property_key)
