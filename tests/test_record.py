import copy

import httpretty

from fulcrum.exceptions import InvalidObjectException

from tests import FulcrumTestCase
from tests.valid_objects import record as valid_record


class RecordTest(FulcrumTestCase):
    def test_record_missing_record(self):
        a_record = copy.deepcopy(valid_record)
        del a_record['record']
        try:
            self.fulcrum_api.record.create(a_record)
        except Exception as exc:
            self.assertIsInstance(exc, InvalidObjectException)
            self.assertEqual(str(exc), 'record must exist and not be empty.')

    def test_missing_latitude(self):
        a_record = copy.deepcopy(valid_record)
        del a_record['record']['latitude']
        try:
            self.fulcrum_api.record.create(a_record)
        except Exception as exc:
            self.assertIsInstance(exc, InvalidObjectException)
            self.assertEqual(str(exc), 'record latitude must exist and be of type int or float.')

    def test_missing_longitude(self):
        a_record = copy.deepcopy(valid_record)
        del a_record['record']['longitude']
        try:
            self.fulcrum_api.record.create(a_record)
        except Exception as exc:
            self.assertIsInstance(exc, InvalidObjectException)
            self.assertEqual(str(exc), 'record longitude must exist and be of type int or float.')

    def test_missing_form_id(self):
        a_record = copy.deepcopy(valid_record)
        del a_record['record']['form_id']
        try:
            self.fulcrum_api.record.create(a_record)
        except Exception as exc:
            self.assertIsInstance(exc, InvalidObjectException)
            self.assertEqual(str(exc), 'record form_id must exist and be of type str.')

    def test_missing_form_values(self):
        a_record = copy.deepcopy(valid_record)
        del a_record['record']['form_values']
        try:
            self.fulcrum_api.record.create(a_record)
        except Exception as exc:
            self.assertIsInstance(exc, InvalidObjectException)
            self.assertEqual(str(exc), 'record form_values must exist and be of type dict.')

    def test_missing_form_values_empty_dict(self):
        a_record = copy.deepcopy(valid_record)
        a_record['record']['form_values'] = {}
        try:
            self.fulcrum_api.record.create(a_record)
        except Exception as exc:
            self.assertIsInstance(exc, InvalidObjectException)
            self.assertEqual(str(exc), 'record form_values must exist and be of type dict and not be empty.')

    @httpretty.activate
    def test_records_from_form_via_url_params(self):
        httpretty.register_uri(httpretty.GET, self.api_root + '/records?form_id=abc-123',
            body='{"records": [{"id": 1},{"id": 2}], "total_count": 2, "current_page": 1, "total_pages": 1, "per_page": 20000}',
            status=200)

        records = self.fulcrum_api.record.all(params={'form_id': 'abc-123'})
        self.assertIsInstance(records, dict)
        self.assertEqual(len(records['records']), 2)
