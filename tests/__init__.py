import unittest

from fulcrum import Fulcrum

key = 'super_secret_key'

api_root = 'https://api.fulcrumapp.com/api/v2'

class FulcrumTestCase(unittest.TestCase):
    api_root = api_root

    def setUp(self):
        self.fulcrum_api = Fulcrum(key=key)
