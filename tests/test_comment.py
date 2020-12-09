from datetime import time
from datetime import date
from datetime import datetime
from unittest import TestCase

from data_models.comment import Comment


class TestComment(TestCase):

    def __init__(self, methodName):
        super(TestComment, self).__init__(methodName=methodName)
        self.comment = Comment(text='', author='', time=0, timestamp=datetime.now(), hid=0, parent=0)

    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()

    def test_comment_test_get_hash_id(self):
        self.assertEqual(self.comment.test_get_hash_id(), True)

    def test_comment_test_to_data(self):
        self.assertEqual(self.comment.test_to_data(), True)

    def test_comment_test_from_data(self):
        self.assertEqual(self.comment.test_from_data(), True)
