from datetime import time
from datetime import date
from datetime import datetime
from unittest import TestCase

from data_models.raw_data import RawData


class TestRawData(TestCase):

    def __init__(self, methodName):
        super(TestRawData, self).__init__(methodName=methodName)
        self.rawData = RawData(title='', url='', text='', dead=0, author='', score=0, time=0, timestamp=datetime.now(), htype='', hid=0, parent=0, descendants=0, ranking=0, deleted=0)

    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()

    def test_raw_data_test_get_hash_id(self):
        self.assertEqual(self.rawData.test_get_hash_id(), True)

    def test_raw_data_test_to_data(self):
        self.assertEqual(self.rawData.test_to_data(), True)

    def test_raw_data_test_from_data(self):
        self.assertEqual(self.rawData.test_from_data(), True)
