from py2neo import Node, Relationship
import uuid
from .graph import GRAPH
from  .neo4jutils import Neo4jUtils
from .text_utils import TextCleanUp

class BaseNode:
    def __init__(self, label: str, identity_key: str = id, identity_value: object = str(uuid.uuid4()), values: dict = None, allow_update: bool = False, tx = None):
        tc = TextCleanUp()
        if tc.is_empty_string(label):
            raise ValueError("label must be specified")
        if tc.is_empty_string(identity_key):
            raise ValueError("identity_key must be specified")
        if tc.is_empty_string(identity_value):
            raise ValueError("identity_value must be specified")

        self.label = Neo4jUtils.get_neo_label(label)
        self.identity_key = Neo4jUtils.get_neo_prop(identity_key)
        self.identity_value = identity_value            
        self.allow_update = allow_update
        self.tx = tx

        if values is None:
            self.values = {}
        else:
            self.values = values


    def find(self):
        result = GRAPH.find_one(self.label, self.identity_key, self.identity_value)

        if result is not None:
            for key in result:
                self.values[key] = result[key]

        return result

    def update(self, values=None):        

        if values is not None:
            self.values.update(values)

        if self.values is not None:
            result = Node(self.label, **self.values)            
        else:
            result = Node(self.label)        

        result[self.identity_key] = self.identity_value

        if self.allow_update:
            GRAPH.merge(result)
        else:            
            # ensure there is no match
            if self.find() is None:
                GRAPH.create(result)
            else:
                raise Exception("Attempted to create already existing node")

        result = self.find()

        return result

    def create_node_relationship(
        self, 
        relationship: str, 
        other_node: Node, 
        relationship_properties: dict, 
        outgoing: bool, 
        allow_self_reference: bool = False
    ):
        node = self.find()

        if other_node is None:
            raise ValueError("Other_node is None")

        if node == other_node:
            if not allow_self_reference:
                return None

        relationship_neo = Neo4jUtils.get_neo_label(relationship)
        if outgoing:
            product_relationship = Relationship(node, relationship_neo, other_node)
        else:
            product_relationship = Relationship(other_node, relationship_neo, node)

        if relationship_properties is not None:
            for item in relationship_properties:
                product_relationship[Neo4jUtils.get_neo_prop(item)] = relationship_properties[item]

        if self.tx is None:
            return GRAPH.merge(product_relationship)
        else:
            return self.tx.merge(product_relationship)    

    def join_simple_relationship(
        self, 
        other_label: str, 
        other_identity_key: str, 
        other_identiy_value: object, 
        relationship: str, 
        relationship_properties: dict = None, 
        outgoing : bool = True        
        ):
            other = BaseNode(other_label, other_identity_key, other_identiy_value)
            other_node = other.find()
            if other_node is None:
                raise Exception("Other Node doesn't exist cannont join_simple_relationship")

            return self.create_node_relationship(relationship, other_node, relationship_properties, outgoing, False)

    def create_simple_relationship(
        self, 
        other_label: str, 
        other_identity_key: str, 
        other_identiy_value: object, 
        other_values: dict,
        relationship: str, 
        relationship_properties: dict = None, 
        outgoing : bool = True
        ):

        other = BaseNode(other_label, other_identity_key, other_identiy_value)
        other_node = other.find()
        if other_node is None:
            other_node = other.update(other_values)

        return self.create_node_relationship(relationship, other_node, relationship_properties, outgoing, False)

    def remove_node_relationships(self):
        node = self.find()

        if node is not None:
            for item in node.relationships():
                GRAPH.separate(item)

    def join(
        self,
        other_basenode: object,
        relationship: str,        
        relationship_properties: dict = None, 
        outgoing: bool = True, 
        ):

        # if not type(other_basenode) is BaseNode:
        #    raise ValueError("other_basenode is not of BaseNode type")

        other_node = other_basenode.find()
        if other_node is None:
            other_node = other_basenode.update()

        return self.create_node_relationship(relationship, other_node, None, outgoing)
                