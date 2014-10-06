import httpretty

from tests import FulcrumTestCase


class RecordTest(FulcrumTestCase):
    @httpretty.activate
    def test_records_from_form_via_url_params(self):
        httpretty.register_uri(httpretty.GET, self.api_root + '/records?form_id=abc-123',
            body='{"records": [{"id": 1},{"id": 2}], "total_count": 2, "current_page": 1, "total_pages": 1, "per_page": 20000}',
            status=200)

        records = self.fulcrum_api.records.search(params={'form_id': 'abc-123'})
        self.assertIsInstance(records, dict)
        self.assertEqual(len(records['records']), 2)
