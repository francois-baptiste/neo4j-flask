from unittest import TestCase
from common.neo4jutils import Neo4jUtils
from common.graph import GRAPH
from datetime import datetime
import uuid

class TestNeo4jUtils(TestCase):
    neo_util = Neo4jUtils(GRAPH)

    def test_get_neo_prop(self):
        prop_name_target = "first_name"
        self.assertEqual(self.neo_util.get_neo_prop(prop_name_target), prop_name_target)
        self.assertEqual(self.neo_util.get_neo_prop("First Name"), prop_name_target)
        self.assertEqual(self.neo_util.get_neo_prop("FIRST NAME"), prop_name_target)
        self.assertEqual(self.neo_util.get_neo_prop("First  Name "), prop_name_target)
        self.assertEqual(self.neo_util.get_neo_prop("first.name"), prop_name_target)
        self.assertEqual(self.neo_util.get_neo_prop(" first.name"), prop_name_target)

    def test_timestamp(self):
        # ryancollingwood: I have no idea how to test this
        epoch = datetime.utcfromtimestamp(0)
        now = datetime.now()
        delta = now - epoch
        test_value = delta.total_seconds()

        self.assertAlmostEqual(self.neo_util.timestamp(), test_value)

    def test_date(self):
        # ryancollingwood: I have no idea how to test this
        self.assertEqual(self.neo_util.date(), datetime.now().strftime('%Y-%m-%d'))

    def test_get_neo_label(self):
        label_name_target = "CAT_PERSON"
        self.assertEqual(self.neo_util.get_neo_label(label_name_target), label_name_target)
        self.assertEqual(self.neo_util.get_neo_label("cat person"), label_name_target)
        self.assertEqual(self.neo_util.get_neo_label("CAT PERSON"), label_name_target)
        self.assertEqual(self.neo_util.get_neo_label("Cat  Person "), label_name_target)
        self.assertEqual(self.neo_util.get_neo_label("cat.person"), label_name_target)
        self.assertEqual(self.neo_util.get_neo_label(" cat.person"), label_name_target)

    def test_create_graph_unique_constraint(self):
        label = str(uuid.uuid4())
        property_key = str(uuid.uuid4())

        # as the label and key are transformed
        actual_label = label.replace("-", "_").upper()
        actual_property_key = property_key.replace("-", "_").lower()

        # assert they are not there
        self.assertEqual(actual_property_key not in GRAPH.schema.get_indexes(actual_label), True)
        self.assertEqual(actual_property_key not in GRAPH.schema.get_uniqueness_constraints(actual_label), True)

        # execute method
        self.neo_util.create_graph_unique_constraint(label, property_key)

        # are they created
        self.assertEqual(actual_property_key not in GRAPH.schema.get_indexes(actual_label), False)
        self.assertEqual(actual_property_key not in GRAPH.schema.get_uniqueness_constraints(actual_label), False)

        # clean up
        GRAPH.schema.drop_uniqueness_constraint(actual_label, actual_property_key)

        # assert they are not there
        self.assertEqual(actual_property_key not in GRAPH.schema.get_indexes(actual_label), True)
        self.assertEqual(actual_property_key not in GRAPH.schema.get_uniqueness_constraints(actual_label), True)

    def test_create_graph_index(self):
        label = str(uuid.uuid4())
        property_key = str(uuid.uuid4())

        # as the label and key are transformed
        actual_label = label.replace("-", "_").upper()
        actual_property_key = property_key.replace("-", "_").lower()

        # assert they are not there
        self.assertEqual(actual_property_key not in GRAPH.schema.get_indexes(actual_label), True)

        # execute method
        self.neo_util.create_graph_index(label, property_key)

        # are they created
        self.assertEqual(actual_property_key in GRAPH.schema.get_indexes(actual_label), True)

        # clean up
        GRAPH.schema.drop_index(actual_label, actual_property_key)

        # assert they are not there
        self.assertEqual(actual_property_key not in GRAPH.schema.get_indexes(actual_label), True)
