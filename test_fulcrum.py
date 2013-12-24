import unittest

import httpretty

from fulcrum import Fulcrum
from fulcrum.api import APIConfig
from fulcrum.exceptions import NotFoundException, InvalidAPIVersionException

key = 'e30e6ed0382322e7dbcb71ff365a5652f40eb602891b02a3b2ef67a4ad467b11'
api_root = 'https://api.fulcrumapp.com/api/v2'


class APIConfigTest(unittest.TestCase):
    def test_invalid_version(self):
        exc = None
        try:
            api_config = APIConfig(key='foo', version=99)
        except Exception as exc:
            pass
        self.assertTrue(isinstance(exc, InvalidAPIVersionException))


class FormTest(unittest.TestCase):
    
    def setUp(self):
        self.fulcrum_api = Fulcrum(key=key)

    @httpretty.activate
    def test_all(self):
        httpretty.register_uri(httpretty.GET, api_root + '/forms',
            body='{"forms": [{"id": 1},{"id": 2}], "total_count": 2, "current_page": 1, "total_pages": 1, "per_page": 20000}',
            status=200)

        forms = self.fulcrum_api.form.all()
        self.assertTrue(isinstance(forms, dict))
        self.assertEqual(len(forms['forms']), 2)

    @httpretty.activate
    def test_find(self):
        httpretty.register_uri(httpretty.GET, api_root + '/forms/5b656cd8-f3ef-43e9-8d22-84d015052778',
            body='{"record_count": 4, "description": "Food Carts and Trucks in Denver", "id": "5b656cd8-f3ef-43e9-8d22-84d015052778"}',
            status=200)
        form = self.fulcrum_api.form.find('5b656cd8-f3ef-43e9-8d22-84d015052778')
        self.assertTrue(isinstance(form, dict))
        self.assertEqual(form['id'], '5b656cd8-f3ef-43e9-8d22-84d015052778')

    @httpretty.activate
    def test_find_not_found(self):
        httpretty.register_uri(httpretty.GET, api_root + '/forms/lobster', status=404)
        exc = None
        try:
            form = self.fulcrum_api.form.find('lobster')
        except Exception as exc:
            pass
        self.assertTrue(isinstance(exc, NotFoundException))

    @httpretty.activate
    def test_delete(self):
        httpretty.register_uri(httpretty.DELETE, api_root + '/forms/5b656cd8-f3ef-43e9-8d22-84d015052778', status=200)
        self.fulcrum_api.form.delete('5b656cd8-f3ef-43e9-8d22-84d015052778')