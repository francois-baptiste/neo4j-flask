import sys
from .views import app

sys.path.append("..")
from common import GRAPH, Neo4jUtils

def create_indexes():
    neo_utils = Neo4jUtils(GRAPH)
    neo_utils.create_graph_unique_constraint("User", "username")
    neo_utils.create_graph_unique_constraint("Tag", "name")
    neo_utils.create_graph_unique_constraint("Post", "id")


create_indexes()
