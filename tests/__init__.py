import unittest

from fulcrum import Fulcrum
from fulcrum.api import APIConfig
from fulcrum.exceptions import InvalidAPIVersionException

key = 'super_secret_key'


class APIConfigTest(unittest.TestCase):
    def test_invalid_version(self):
        try:
            APIConfig(key='foo', version=99)
        except Exception as exc:
            self.assertIsInstance(exc, InvalidAPIVersionException)


class FulcrumTestCase(unittest.TestCase):
    api_root = 'https://api.fulcrumapp.com/api/v2'

    def setUp(self):
        self.fulcrum_api = Fulcrum(key=key)
