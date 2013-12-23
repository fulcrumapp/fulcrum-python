import unittest

import httpretty

from fulcrum import Fulcrum
from fulcrum.exceptions import InvalidObjectException

key = 'super_secret_key'
api_root = 'https://api.fulcrumapp.com/api/v2'


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
    def test_delete(self):
        httpretty.register_uri(httpretty.DELETE, api_root + '/forms/5b656cd8-f3ef-43e9-8d22-84d015052778', status=200)
        form = self.fulcrum_api.form.delete('5b656cd8-f3ef-43e9-8d22-84d015052778')

    def test_create_needs_form(self):
        exc = None
        try:
            form = self.fulcrum_api.form.create({'cats': True})
        except Exception as exc:
            pass
        self.assertTrue(isinstance(exc, InvalidObjectException))
    """
    @httpretty.activate
    def test_create(self):
        httpretty.register_uri(httpretty.POST, api_root + '/forms', status=200, body='{"id": 54321}')
        form = self.fulcrum_api.form.create({'cats': True})
        self.assertTrue('id' in form)
    """
