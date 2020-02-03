import httpretty

from fulcrum.exceptions import NotFoundException, InternalServerErrorException

from tests import FulcrumTestCase
from tests.valid_objects import form as valid_form


class FormTest(FulcrumTestCase):
    @httpretty.activate
    def test_all(self):
        httpretty.register_uri(httpretty.GET, self.api_root + '/forms',
            body='{"forms": [{"id": 1},{"id": 2}], "total_count": 2, "current_page": 1, "total_pages": 1, "per_page": 20000}',
            status=200)

        forms = self.fulcrum_api.forms.search()
        self.assertIsInstance(forms, dict)
        self.assertEqual(len(forms['forms']), 2)

    @httpretty.activate
    def test_find(self):
        httpretty.register_uri(httpretty.GET, self.api_root + '/forms/5b656cd8-f3ef-43e9-8d22-84d015052778',
            body='{"record_count": 4, "description": "Food Carts and Trucks in Denver", "id": "5b656cd8-f3ef-43e9-8d22-84d015052778"}',
            status=200)
        form = self.fulcrum_api.forms.find('5b656cd8-f3ef-43e9-8d22-84d015052778')
        self.assertIsInstance(form, dict)
        self.assertEqual(form['id'], '5b656cd8-f3ef-43e9-8d22-84d015052778')

    @httpretty.activate
    def test_find_not_found(self):
        httpretty.register_uri(httpretty.GET, self.api_root + '/forms/lobster', status=404)
        try:
            self.fulcrum_api.forms.find('lobster')
        except Exception as exc:
            self.assertIsInstance(exc, NotFoundException)

    @httpretty.activate
    def test_delete(self):
        httpretty.register_uri(httpretty.DELETE, self.api_root + '/forms/5b656cd8-f3ef-43e9-8d22-84d015052778', status=200)
        self.fulcrum_api.forms.delete('5b656cd8-f3ef-43e9-8d22-84d015052778')

    @httpretty.activate
    def test_create_500(self):
        httpretty.register_uri(httpretty.POST, self.api_root + '/forms', status=500)
        try:
            self.fulcrum_api.forms.create(valid_form)
        except Exception as exc:
            self.assertIsInstance(exc, InternalServerErrorException)

    @httpretty.activate
    def test_create_valid(self):
        httpretty.register_uri(httpretty.POST, self.api_root + '/forms',
            body='{"form": {"id": 1}}',
            status=200)
        form = self.fulcrum_api.forms.create(valid_form)
        self.assertIsInstance(form, dict)
        self.assertTrue(form['form']['id'] == 1)

    @httpretty.activate
    def test_update(self):
        httpretty.register_uri(httpretty.PUT, self.api_root + '/forms/abc-123',
            body='{"form": {"id": "abc-123"}}',
            status=200)
        form = self.fulcrum_api.forms.update('abc-123', valid_form)
        self.assertIsInstance(form, dict)
        self.assertTrue(form['form']['id'] == 'abc-123')
