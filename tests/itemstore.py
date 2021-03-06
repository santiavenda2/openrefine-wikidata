
import unittest
import requests_mock
import re
import requests
from itemstore import ItemStore
from config import redis_client

class ItemStoreTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.s = ItemStore(redis_client)

    def setUp(self):
        redis_client.flushall()

    def test_label(self):
        self.assertEqual(self.s.get_label('Q3918', 'en'),
                        'university')

    def test_label_fallback(self):
        # this item currently does not have a label in catalan
        self.assertTrue(self.s.get_label('Q3578062', 'ca'))

    def test_preferred_rank(self):
        """
        The first value in the list should be the preferred rank,
        if any. This item (Australia) contains various currencies
        that have been in use before, and Australian Dollar
        is the preferred one.
        """
        self.assertEqual(self.s.get_item('Q408')['P38'][0],
                        'Q259502')

    def test_caching(self):
        item = self.s.get_item('Q750483')
        with requests_mock.Mocker() as mocker: # disable all HTTP reqs
            item2 = self.s.get_item('Q750483')
            # we still get the same item
            self.assertEqual(set(item), set(item2))

    def test_500_error(self):
        with requests_mock.Mocker() as mocker: # disable all HTTP reqs
            mocker.get(re.compile('.*\.wikidata\.org/.*'), status_code=500)
            with self.assertRaises(requests.exceptions.HTTPError):
                item = self.s.get_item('Q750484')

