import unittest

from fulcrum import Fulcrum

key = 'super_secret_key'


class FulcrumTestCase(unittest.TestCase):
    api_root = 'https://api.fulcrumapp.com/api/v2'

    def setUp(self):
        self.fulcrum_api = Fulcrum(key=key)
