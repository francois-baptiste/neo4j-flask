import os
from py2neo import Graph

def get_graph_connection():
    url = os.environ.get('GRAPHENEDB_URL', 'http://localhost:7474')
    username = os.environ.get('NEO4J_USERNAME')
    password = os.environ.get('NEO4J_PASSWORD')

    return Graph(url + '/db/data/', username=username, password=password)

GRAPH = get_graph_connection()