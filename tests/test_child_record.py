import httpretty

from tests import FulcrumTestCase


class ChildRecordTest(FulcrumTestCase):
    @httpretty.activate
    def test_records_from_form_via_url_params(self):
        httpretty.register_uri(httpretty.GET, self.api_root + '/child_records?form_id=cf6f189e-7d50-404f-946a-835952da5083',
            body='{"total_count": 1, "current_page": 1, "total_pages": 1, "records": [{"status": "occupied", "updated_by": "Jason Sanford", "latitude": null, "geometry": null, "created_at": "2014-11-30T23:44:55Z", "updated_at": "2014-11-30T23:44:55Z", "created_by": "Jason Sanford", "form_values": {"2541": "2014-11-13", "2c7f": "12:34", "e05a": "Good stuff", "348f": [{"caption": "", "photo_id": "03656c9b-24ad-fed5-abee-6e3b514bb927"}]}, "client_created_at": "2014-11-30T23:44:54Z", "assigned_to_id": null, "version": 1, "updated_by_id": "4f1efa091441405373000445", "longitude": null, "client_updated_at": "2014-11-30T23:44:54Z", "record_id": "beef678b-fb89-4b15-9ee7-1f8be3e2abe7", "created_by_id": "4f1efa091441405373000445", "project_id": null, "changeset_id": "00291a46-232b-417c-a14d-b0be3e7eca94", "id": "5911af53-8c48-502a-2d07-17010aef73f9", "form_id": "cf6f189e-7d50-404f-946a-835952da5083"}], "per_page": 20000}',
            status=200)

        records = self.fulcrum_api.child_records.search(url_params={'form_id': 'cf6f189e-7d50-404f-946a-835952da5083'})
        self.assertIsInstance(records, dict)
        self.assertEqual(len(records['records']), 1)
