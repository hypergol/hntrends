from datetime import time
from datetime import date
from datetime import datetime
from unittest import TestCase

from data_models.element import Element


class TestElement(TestCase):

    def __init__(self, methodName):
        super(TestElement, self).__init__(methodName=methodName)
        self.element = Element(date='', timestamp=datetime.now(), hid='', parent='', author='', entities=['', ''], vector={"sample": "sample"})

    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()

    def test_element_test_get_hash_id(self):
        self.assertEqual(self.element.test_get_hash_id(), True)

    def test_element_test_to_data(self):
        self.assertEqual(self.element.test_to_data(), True)

    def test_element_test_from_data(self):
        self.assertEqual(self.element.test_from_data(), True)
