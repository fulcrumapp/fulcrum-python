import copy

import httpretty

from fulcrum.exceptions import NotFoundException, InvalidObjectException, InternalServerErrorException
from fulcrum.validators import FormValidator

from tests import FulcrumTestCase
from tests.valid_objects import form as valid_form


class FormTest(FulcrumTestCase):
    @httpretty.activate
    def test_all(self):
        httpretty.register_uri(httpretty.GET, self.api_root + '/forms',
            body='{"forms": [{"id": 1},{"id": 2}], "total_count": 2, "current_page": 1, "total_pages": 1, "per_page": 20000}',
            status=200)

        forms = self.fulcrum_api.form.all()
        self.assertIsInstance(forms, dict)
        self.assertEqual(len(forms['forms']), 2)

    @httpretty.activate
    def test_find(self):
        httpretty.register_uri(httpretty.GET, self.api_root + '/forms/5b656cd8-f3ef-43e9-8d22-84d015052778',
            body='{"record_count": 4, "description": "Food Carts and Trucks in Denver", "id": "5b656cd8-f3ef-43e9-8d22-84d015052778"}',
            status=200)
        form = self.fulcrum_api.form.find('5b656cd8-f3ef-43e9-8d22-84d015052778')
        self.assertIsInstance(form, dict)
        self.assertEqual(form['id'], '5b656cd8-f3ef-43e9-8d22-84d015052778')

    @httpretty.activate
    def test_find_not_found(self):
        httpretty.register_uri(httpretty.GET, self.api_root + '/forms/lobster', status=404)
        try:
            self.fulcrum_api.form.find('lobster')
        except Exception as exc:
            self.assertIsInstance(exc, NotFoundException)

    @httpretty.activate
    def test_delete(self):
        httpretty.register_uri(httpretty.DELETE, self.api_root + '/forms/5b656cd8-f3ef-43e9-8d22-84d015052778', status=200)
        self.fulcrum_api.form.delete('5b656cd8-f3ef-43e9-8d22-84d015052778')

    @httpretty.activate
    def test_create_500(self):
        httpretty.register_uri(httpretty.POST, self.api_root + '/forms', status=500)
        try:
            self.fulcrum_api.form.create(valid_form)
        except Exception as exc:
            self.assertIsInstance(exc, InternalServerErrorException)

    def test_create_no_form(self):
        try:
            self.fulcrum_api.form.create({'cats': True})
        except Exception as exc:
            self.assertIsInstance(exc, InvalidObjectException)
            self.assertEqual(str(exc), 'form must exist and not be empty.')

    def test_create_invalid_name(self):
        a_form = copy.deepcopy(valid_form)
        a_form['form']['name'] = ''
        try:
            self.fulcrum_api.form.create(a_form)
        except Exception as exc:
            self.assertIsInstance(exc, InvalidObjectException)
            self.assertEqual(str(exc), 'form name must exist and not be empty.')

    def test_create_invalid_elements(self):
        try:
            self.fulcrum_api.form.create({'form': {'name': 'cats', 'elements': []}})
        except Exception as exc:
            self.assertIsInstance(exc, InvalidObjectException)
            self.assertEqual(str(exc), 'form elements must exist and not be empty.')

    def test_create_no_name_no_elements(self):
        a_form = copy.deepcopy(valid_form)
        del a_form['form']['name']
        del a_form['form']['elements']
        try:
            self.fulcrum_api.form.create(a_form)
        except Exception as exc:
            self.assertIsInstance(exc, InvalidObjectException)
            self.assertTrue(str(exc) == 'form elements must exist and not be empty. form name must exist and not be empty.' or str(exc) == 'form name must exist and not be empty. form elements must exist and not be empty.')

    def test_create_bad_element(self):
        a_form = copy.deepcopy(valid_form)
        a_form['form']['elements'][0] = {}
        try:
            self.fulcrum_api.form.create(a_form)
        except Exception as exc:
            self.assertIsInstance(exc, InvalidObjectException)
            self.assertTrue(str(exc) == 'elements element must be of type dict and not be empty.')

    def test_create_element_missing_data_name(self):
        a_form = copy.deepcopy(valid_form)
        del a_form['form']['elements'][0]['data_name']
        try:
            self.fulcrum_api.form.create(a_form)
        except Exception as exc:
            self.assertIsInstance(exc, InvalidObjectException)
            self.assertEqual(str(exc), 'a data_name must exist.')

    def test_element_no_key(self):
        a_form = copy.deepcopy(valid_form)
        del a_form['form']['elements'][0]['key']
        try:
            self.fulcrum_api.form.create(a_form)
        except Exception as exc:
            self.assertIsInstance(exc, InvalidObjectException)
            self.assertEqual(str(exc), 'element key must exist and not be empty.')

    def test_element_duplicate_key(self):
        a_form = copy.deepcopy(valid_form)
        a_form['form']['elements'][1]['key'] = a_form['form']['elements'][0]['key']
        try:
            self.fulcrum_api.form.create(a_form)
        except Exception as exc:
            self.assertIsInstance(exc, InvalidObjectException)
            self.assertEqual(str(exc), 'a key must be unique.')

    def test_element_no_type(self):
        a_form = copy.deepcopy(valid_form)
        del a_form['form']['elements'][0]['type']
        try:
            self.fulcrum_api.form.create(a_form)
        except Exception as exc:
            self.assertIsInstance(exc, InvalidObjectException)
            self.assertEqual(str(exc), 'a type must exist and be one of {0}.'.format(FormValidator.TYPES))

    def test_element_no_required(self):
        a_form = copy.deepcopy(valid_form)
        del a_form['form']['elements'][0]['required']
        try:
            self.fulcrum_api.form.create(a_form)
        except Exception as exc:
            self.assertIsInstance(exc, InvalidObjectException)
            self.assertEqual(str(exc), 'a required must exist and be of type bool.')

    def test_element_classification_field_missing_classification_set_id(self):
        a_form = copy.deepcopy(valid_form)
        del a_form['form']['elements'][2]['elements'][2]['classification_set_id']
        try:
            self.fulcrum_api.form.create(a_form)
        except Exception as exc:
            self.assertIsInstance(exc, InvalidObjectException)
            self.assertEqual(str(exc), 'f classification_set_id must exist.')

    def test_element_section_not_a_list(self):
        a_form = copy.deepcopy(valid_form)
        a_form['form']['elements'][2]['elements'] = 'a random string that is not a list or tuple'
        try:
            self.fulcrum_api.form.create(a_form)
        except Exception as exc:
            self.assertIsInstance(exc, InvalidObjectException)
            self.assertEqual(str(exc), 'c elements must exist and be of type list or tuple.')

    def test_element_section_empty_list(self):
        a_form = copy.deepcopy(valid_form)
        a_form['form']['elements'][2]['elements'] = []
        try:
            self.fulcrum_api.form.create(a_form)
        except Exception as exc:
            self.assertIsInstance(exc, InvalidObjectException)
            self.assertEqual(str(exc), 'c elements must contain additional elements.')

    def test_element_choices_empty_list(self):
        a_form = copy.deepcopy(valid_form)
        a_form['form']['elements'][2]['elements'][0]['choices'] = []
        try:
            self.fulcrum_api.form.create(a_form)
        except Exception as exc:
            self.assertIsInstance(exc, InvalidObjectException)
            self.assertEqual(str(exc), 'd choices must exist, be of type list or tuple, and not be empty.')

    def test_element_choices_choice_list_id_none(self):
        a_form = copy.deepcopy(valid_form)
        del a_form['form']['elements'][2]['elements'][0]['choices']
        a_form['form']['elements'][2]['elements'][0]['choice_list_id'] = None
        try:
            self.fulcrum_api.form.create(a_form)
        except Exception as exc:
            self.assertIsInstance(exc, InvalidObjectException)
            self.assertEqual(str(exc), 'd choice_list_id must exist.')

    @httpretty.activate
    def test_create_valid(self):
        httpretty.register_uri(httpretty.POST, self.api_root + '/forms',
            body='{"form": {"id": 1}}',
            status=200)
        form = self.fulcrum_api.form.create(valid_form)
        self.assertIsInstance(form, dict)
        self.assertTrue(form['form']['id'] == 1)

    @httpretty.activate
    def test_update(self):
        httpretty.register_uri(httpretty.PUT, self.api_root + '/forms/abc-123',
            body='{"form": {"id": "abc-123"}}',
            status=200)
        form = self.fulcrum_api.form.update('abc-123', valid_form)
        self.assertIsInstance(form, dict)
        self.assertTrue(form['form']['id'] == 'abc-123')

    def test_update_no_name(self):
        a_form = copy.deepcopy(valid_form)
        del a_form['form']['name']
        a_form['form']['id'] = 'abc-123'
        try:
            self.fulcrum_api.form.update('abc-123', a_form)
        except Exception as exc:
            self.assertIsInstance(exc, InvalidObjectException)
            self.assertEqual(str(exc), 'form name must exist and not be empty.')
