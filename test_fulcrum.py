import copy
import unittest

import httpretty

from fulcrum import Fulcrum
from fulcrum.api import APIConfig
from fulcrum.exceptions import NotFoundException, InvalidAPIVersionException, InvalidObjectException, InternalServerErrorException
from fulcrum.validators import FormValidator

key = 'super_secret_key'
api_root = 'https://api.fulcrumapp.com/api/v2'


class APIConfigTest(unittest.TestCase):
    def test_invalid_version(self):
        try:
            APIConfig(key='foo', version=99)
        except Exception as exc:
            self.assertIsInstance(exc, InvalidAPIVersionException)


class FormTest(unittest.TestCase):
    valid_form = {
        'form': {
            'name': 'Fire Hydrants',
            'description': 'Locations of fire hydrants near my house',
            'elements': [
                {
                    'key': 'a',
                    'label': 'Hydrant ID',
                    'data_name': 'hydrant_id',
                    'type': 'TextField',
                    'description': 'The ID of the fire hydrant',
                    'required': True,
                    'hidden': False,
                    'disabled': False
                },
                {
                    'key': 'b',
                    'label': 'Year Manufactured',
                    'data_name': 'year_manufactured',
                    'type': 'TextField',
                    'description': 'The four digit year the hydrant was manufactured',
                    'required': False,
                    'hidden': False,
                    'disabled': False,
                    'numeric': True
                },
                {
                    'key': 'c',
                    'label': 'Structural',
                    'data_name': 'structural',
                    'type': 'Section',
                    'description': 'Structural information about the hydrant',
                    'required': False,
                    'hidden': False,
                    'disabled': False,
                    'elements': [
                        {
                            'key': 'd',
                            'label': 'Color',
                            'data_name': 'color',
                            'type': 'ChoiceField',
                            'description': 'The color of the fire hydrant',
                            'required': True,
                            'hidden': False,
                            'disabled': False,
                            'choices': [
                                {
                                    'value': 'red',
                                    'label': 'Red'
                                },
                                {
                                    'value': 'yellow',
                                    'label': 'Yellow'
                                },
                                {
                                    'value': 'white',
                                    'label': 'White'
                                }
                            ],
                            'allow_other': True
                        },
                        {
                            'key': 'e',
                            'label': 'Height',
                            'data_name': 'height',
                            'type': 'TextField',
                            'description': 'The hight of the fire hydrant in meters',
                            'required': True,
                            'hidden': False,
                            'disabled': False,
                            'numeric': True
                        },
                        {
                            'key': 'f',
                            'label': 'Type',
                            'data_name': 'type',
                            'type': 'ClassificationField',
                            'classification_set_id': 9999,
                            'description': 'The type of fire hydrant',
                            'required': False,
                            'hidden': False,
                            'disabled': False
                        }
                    ]
                }
            ]
        }
    }

    def setUp(self):
        self.fulcrum_api = Fulcrum(key=key)

    @httpretty.activate
    def test_all(self):
        httpretty.register_uri(httpretty.GET, api_root + '/forms',
            body='{"forms": [{"id": 1},{"id": 2}], "total_count": 2, "current_page": 1, "total_pages": 1, "per_page": 20000}',
            status=200)

        forms = self.fulcrum_api.form.all()
        self.assertIsInstance(forms, dict)
        self.assertEqual(len(forms['forms']), 2)

    @httpretty.activate
    def test_find(self):
        httpretty.register_uri(httpretty.GET, api_root + '/forms/5b656cd8-f3ef-43e9-8d22-84d015052778',
            body='{"record_count": 4, "description": "Food Carts and Trucks in Denver", "id": "5b656cd8-f3ef-43e9-8d22-84d015052778"}',
            status=200)
        form = self.fulcrum_api.form.find('5b656cd8-f3ef-43e9-8d22-84d015052778')
        self.assertIsInstance(form, dict)
        self.assertEqual(form['id'], '5b656cd8-f3ef-43e9-8d22-84d015052778')

    @httpretty.activate
    def test_find_not_found(self):
        httpretty.register_uri(httpretty.GET, api_root + '/forms/lobster', status=404)
        try:
            self.fulcrum_api.form.find('lobster')
        except Exception as exc:
            self.assertIsInstance(exc, NotFoundException)

    @httpretty.activate
    def test_delete(self):
        httpretty.register_uri(httpretty.DELETE, api_root + '/forms/5b656cd8-f3ef-43e9-8d22-84d015052778', status=200)
        self.fulcrum_api.form.delete('5b656cd8-f3ef-43e9-8d22-84d015052778')

    @httpretty.activate
    def test_create_500(self):
        httpretty.register_uri(httpretty.POST, api_root + '/forms', status=500)
        try:
            self.fulcrum_api.form.create(self.valid_form)
        except Exception as exc:
            self.assertIsInstance(exc, InternalServerErrorException)

    def test_create_no_form(self):
        try:
            self.fulcrum_api.form.create({'cats': True})
        except Exception as exc:
            self.assertIsInstance(exc, InvalidObjectException)
            self.assertEqual(str(exc), 'form must exist and not be empty.')

    def test_create_invalid_name(self):
        a_form = copy.deepcopy(self.valid_form)
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
        a_form = copy.deepcopy(self.valid_form)
        del a_form['form']['name']
        del a_form['form']['elements']
        try:
            self.fulcrum_api.form.create(a_form)
        except Exception as exc:
            self.assertIsInstance(exc, InvalidObjectException)
            self.assertTrue(str(exc) == 'form elements must exist and not be empty. form name must exist and not be empty.' or str(exc) == 'form name must exist and not be empty. form elements must exist and not be empty.')

    def test_create_bad_element(self):
        a_form = copy.deepcopy(self.valid_form)
        a_form['form']['elements'][0] = {}
        try:
            self.fulcrum_api.form.create(a_form)
        except Exception as exc:
            self.assertIsInstance(exc, InvalidObjectException)
            self.assertTrue(str(exc) == 'elements element must be of type dict and not be empty.')

    def test_create_element_missing_data_name(self):
        a_form = copy.deepcopy(self.valid_form)
        del a_form['form']['elements'][0]['data_name']
        try:
            self.fulcrum_api.form.create(a_form)
        except Exception as exc:
            self.assertIsInstance(exc, InvalidObjectException)
            self.assertEqual(str(exc), 'a data_name must exist.')

    def test_element_no_key(self):
        a_form = copy.deepcopy(self.valid_form)
        del a_form['form']['elements'][0]['key']
        try:
            self.fulcrum_api.form.create(a_form)
        except Exception as exc:
            self.assertIsInstance(exc, InvalidObjectException)
            self.assertEqual(str(exc), 'element key must exist and not be empty.')

    def test_element_duplicate_key(self):
        a_form = copy.deepcopy(self.valid_form)
        a_form['form']['elements'][1]['key'] = a_form['form']['elements'][0]['key']
        try:
            self.fulcrum_api.form.create(a_form)
        except Exception as exc:
            self.assertIsInstance(exc, InvalidObjectException)
            self.assertEqual(str(exc), 'a key must be unique.')

    def test_element_no_type(self):
        a_form = copy.deepcopy(self.valid_form)
        del a_form['form']['elements'][0]['type']
        try:
            self.fulcrum_api.form.create(a_form)
        except Exception as exc:
            self.assertIsInstance(exc, InvalidObjectException)
            self.assertEqual(str(exc), 'a type must exist and be one of {0}.'.format(FormValidator.TYPES))

    def test_element_no_required(self):
        a_form = copy.deepcopy(self.valid_form)
        del a_form['form']['elements'][0]['required']
        try:
            self.fulcrum_api.form.create(a_form)
        except Exception as exc:
            self.assertIsInstance(exc, InvalidObjectException)
            self.assertEqual(str(exc), 'a required must exist and be of type bool.')

    def test_element_classification_field_missing_classification_set_id(self):
        a_form = copy.deepcopy(self.valid_form)
        del a_form['form']['elements'][2]['elements'][2]['classification_set_id']
        try:
            self.fulcrum_api.form.create(a_form)
        except Exception as exc:
            self.assertIsInstance(exc, InvalidObjectException)
            self.assertEqual(str(exc), 'f classification_set_id must exist.')

    def test_element_section_not_a_list(self):
        a_form = copy.deepcopy(self.valid_form)
        a_form['form']['elements'][2]['elements'] = 'a random string that is not a list or tuple'
        try:
            self.fulcrum_api.form.create(a_form)
        except Exception as exc:
            self.assertIsInstance(exc, InvalidObjectException)
            self.assertEqual(str(exc), 'c elements must exist and be of type list or tuple.')

    def test_element_section_empty_list(self):
        a_form = copy.deepcopy(self.valid_form)
        a_form['form']['elements'][2]['elements'] = []
        try:
            self.fulcrum_api.form.create(a_form)
        except Exception as exc:
            self.assertIsInstance(exc, InvalidObjectException)
            self.assertEqual(str(exc), 'c elements must contain additional elements.')

    def test_element_choices_empty_list(self):
        a_form = copy.deepcopy(self.valid_form)
        a_form['form']['elements'][2]['elements'][0]['choices'] = []
        try:
            self.fulcrum_api.form.create(a_form)
        except Exception as exc:
            self.assertIsInstance(exc, InvalidObjectException)
            self.assertEqual(str(exc), 'd choices must exist, be of type list or tuple, and not be empty.')

    def test_element_choices_choice_list_id_none(self):
        a_form = copy.deepcopy(self.valid_form)
        del a_form['form']['elements'][2]['elements'][0]['choices']
        a_form['form']['elements'][2]['elements'][0]['choice_list_id'] = None
        try:
            self.fulcrum_api.form.create(a_form)
        except Exception as exc:
            self.assertIsInstance(exc, InvalidObjectException)
            self.assertEqual(str(exc), 'd choice_list_id must exist.')

    @httpretty.activate
    def test_create_valid(self):
        httpretty.register_uri(httpretty.POST, api_root + '/forms',
            body='{"form": {"id": 1}}',
            status=200)
        form = self.fulcrum_api.form.create(self.valid_form)
        self.assertIsInstance(form, dict)
        self.assertTrue(form['form']['id'] == 1)

    @httpretty.activate
    def test_update(self):
        httpretty.register_uri(httpretty.PUT, api_root + '/forms/abc-123',
            body='{"form": {"id": "abc-123"}}',
            status=200)
        form = self.fulcrum_api.form.update('abc-123', self.valid_form)
        self.assertIsInstance(form, dict)
        self.assertTrue(form['form']['id'] == 'abc-123')

    def test_update_no_name(self):
        a_form = copy.deepcopy(self.valid_form)
        del a_form['form']['name']
        a_form['form']['id'] = 'abc-123'
        try:
            self.fulcrum_api.form.update('abc-123', a_form)
        except Exception as exc:
            self.assertIsInstance(exc, InvalidObjectException)
            self.assertEqual(str(exc), 'form name must exist and not be empty.')


class RecordTest(unittest.TestCase):
    valid_record = {
        'record': {
            'latitude': 40.678,
            'longitude': -100.567,
            'form_id': 'abc-123',
            'form_values': {
                'height': 34,
                'bathrooms': 2.5,
            }
        }
    }

    def setUp(self):
        self.fulcrum_api = Fulcrum(key=key)

    def test_record_missing_record(self):
        a_record = copy.deepcopy(self.valid_record)
        del a_record['record']
        try:
            self.fulcrum_api.record.create(a_record)
        except Exception as exc:
            self.assertIsInstance(exc, InvalidObjectException)
            self.assertEqual(str(exc), 'record must exist and not be empty.')

    def test_missing_latitude(self):
        a_record = copy.deepcopy(self.valid_record)
        del a_record['record']['latitude']
        try:
            self.fulcrum_api.record.create(a_record)
        except Exception as exc:
            self.assertIsInstance(exc, InvalidObjectException)
            self.assertEqual(str(exc), 'record latitude must exist and be of type int or float.')

    def test_missing_longitude(self):
        a_record = copy.deepcopy(self.valid_record)
        del a_record['record']['longitude']
        try:
            self.fulcrum_api.record.create(a_record)
        except Exception as exc:
            self.assertIsInstance(exc, InvalidObjectException)
            self.assertEqual(str(exc), 'record longitude must exist and be of type int or float.')

    def test_missing_form_id(self):
        a_record = copy.deepcopy(self.valid_record)
        del a_record['record']['form_id']
        try:
            self.fulcrum_api.record.create(a_record)
        except Exception as exc:
            self.assertIsInstance(exc, InvalidObjectException)
            self.assertEqual(str(exc), 'record form_id must exist and be of type str.')

    def test_missing_form_values(self):
        a_record = copy.deepcopy(self.valid_record)
        del a_record['record']['form_values']
        try:
            self.fulcrum_api.record.create(a_record)
        except Exception as exc:
            self.assertIsInstance(exc, InvalidObjectException)
            self.assertEqual(str(exc), 'record form_values must exist and be of type dict.')

    def test_missing_form_values_empty_dict(self):
        a_record = copy.deepcopy(self.valid_record)
        a_record['record']['form_values'] = {}
        try:
            self.fulcrum_api.record.create(a_record)
        except Exception as exc:
            self.assertIsInstance(exc, InvalidObjectException)
            self.assertEqual(str(exc), 'record form_values must exist and be of type dict and not be empty.')

    @httpretty.activate
    def test_records_from_form_via_url_params(self):
        httpretty.register_uri(httpretty.GET, api_root + '/records?form_id=abc-123',
            body='{"records": [{"id": 1},{"id": 2}], "total_count": 2, "current_page": 1, "total_pages": 1, "per_page": 20000}',
            status=200)

        records = self.fulcrum_api.record.all(params={'form_id': 'abc-123'})
        self.assertIsInstance(records, dict)
        self.assertEqual(len(records['records']), 2)


class WebhookTest(unittest.TestCase):
    valid_webhook = {
        'webhook': {
            'url': 'http://google.com/hookit',
            'name': 'The very best webhook',
            'active': True
        }
    }

    def setUp(self):
        self.fulcrum_api = Fulcrum(key=key)

    def test_no_webhook(self):
        a_webhook = copy.deepcopy(self.valid_webhook)
        del a_webhook['webhook']
        try:
            self.fulcrum_api.webhook.create(a_webhook)
        except Exception as exc:
            self.assertIsInstance(exc, InvalidObjectException)
            self.assertEqual(str(exc), 'webhook must exist and not be empty.')

    def test_no_url(self):
        a_webhook = copy.deepcopy(self.valid_webhook)
        del a_webhook['webhook']['url']
        try:
            self.fulcrum_api.webhook.create(a_webhook)
        except Exception as exc:
            self.assertIsInstance(exc, InvalidObjectException)
            self.assertEqual(str(exc), 'webhook url must exist.')

    def test_active_not_a_bool(self):
        a_webhook = copy.deepcopy(self.valid_webhook)
        a_webhook['webhook']['active'] = 'lobster'
        try:
            self.fulcrum_api.webhook.create(a_webhook)
        except Exception as exc:
            self.assertIsInstance(exc, InvalidObjectException)
            self.assertEqual(str(exc), 'webhook active must be of type bool.')
