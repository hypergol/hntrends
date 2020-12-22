from datetime import time
from datetime import date
from datetime import datetime
from unittest import TestCase

from data_models.cluster_model import ClusterModel


class TestClusterModel(TestCase):

    def __init__(self, methodName):
        super(TestClusterModel, self).__init__(methodName=methodName)
        self.clusterModel = ClusterModel(date='', model={"sample": "sample"})

    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()

    def test_cluster_model_test_get_hash_id(self):
        self.assertEqual(self.clusterModel.test_get_hash_id(), True)

    def test_cluster_model_test_to_data(self):
        self.assertEqual(self.clusterModel.test_to_data(), True)

    def test_cluster_model_test_from_data(self):
        self.assertEqual(self.clusterModel.test_from_data(), True)
