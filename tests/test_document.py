from datetime import time
from datetime import date
from datetime import datetime
from unittest import TestCase

from data_models.document import Document


class TestDocument(TestCase):

    def __init__(self, methodName):
        super(TestDocument, self).__init__(methodName=methodName)
        self.document = Document(hid=0, timestamp=datetime.now(), tokens=['', ''], labels=['', ''])

    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()

    def test_document_test_get_hash_id(self):
        self.assertEqual(self.document.test_get_hash_id(), True)

    def test_document_test_to_data(self):
        self.assertEqual(self.document.test_to_data(), True)

    def test_document_test_from_data(self):
        self.assertEqual(self.document.test_from_data(), True)
