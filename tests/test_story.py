from datetime import time
from datetime import date
from datetime import datetime
from unittest import TestCase

from data_models.story import Story


class TestStory(TestCase):

    def __init__(self, methodName):
        super(TestStory, self).__init__(methodName=methodName)
        self.story = Story(title='', url='', author='', score=0, time=0, timestamp=datetime.now(), hid=0, descendants=0, ranking=0)

    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()

    def test_story_test_get_hash_id(self):
        self.assertEqual(self.story.test_get_hash_id(), True)

    def test_story_test_to_data(self):
        self.assertEqual(self.story.test_to_data(), True)

    def test_story_test_from_data(self):
        self.assertEqual(self.story.test_from_data(), True)
