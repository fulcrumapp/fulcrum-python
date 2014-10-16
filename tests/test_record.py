import httpretty

from tests import FulcrumTestCase


class RecordTest(FulcrumTestCase):
    @httpretty.activate
    def test_records_from_form_via_url_params(self):
        httpretty.register_uri(httpretty.GET, self.api_root + '/records?form_id=abc-123',
            body='{"records": [{"id": 1},{"id": 2}], "total_count": 2, "current_page": 1, "total_pages": 1, "per_page": 20000}',
            status=200)

        records = self.fulcrum_api.records.search(url_params={'form_id': 'abc-123'})
        self.assertIsInstance(records, dict)
        self.assertEqual(len(records['records']), 2)

    @httpretty.activate
    def test_record_history(self):
        httpretty.register_uri(httpretty.GET, self.api_root + '/records/b88edefd-d6d5-4d8b-a45e-495f3541d94a/history',
            body='{"total_count": 2, "current_page": 1, "total_pages": 1, "records": [{"vertical_accuracy": null, "updated_at": "2014-10-15T22:25:14Z", "course": null, "assigned_to_id": null, "updated_by_id": "3f1efa691441405373000445", "form_version": 2, "speed": null, "id": "b88edefd-d6d5-4d8b-a45e-495f3541d94a", "form_id": "50a0e558-47fd-476b-914d-89a02dc40147", "history_changed_by_id": "4f1efa091441405373100445", "altitude": null, "created_by": "Jason Sanford", "form_values": {"dc0e": "19"}, "client_created_at": "2014-10-15T22:25:14Z", "version": 1, "latitude": 35.5550349, "project_id": null, "status": null, "history_changed_by": "Jason Sanford", "updated_by": "Jason Sanford", "horizontal_accuracy": null, "history_id": "8e15a5d8-a48d-48bc-865c-87c8ba1a3191", "history_change_type": "c", "client_updated_at": "2014-10-15T22:25:14Z", "history_created_at": "2014-10-15T22:25:14Z", "created_at": "2014-10-15T22:25:14Z", "longitude": -80.93346194, "assigned_to": null, "created_by_id": "4f1efa091441405373300445"}, {"vertical_accuracy": null, "updated_at": "2014-10-15T22:30:12Z", "course": null, "assigned_to_id": null, "updated_by_id": "4f1efa091441404373000445", "form_version": 2, "speed": null, "id": "b88edefd-d6d4-4d8b-a45e-495f3541d93a", "form_id": "50a1e558-47fd-476b-915d-89a02dd40247", "history_changed_by_id": "4f1efa071441405373000446", "altitude": null, "created_by": "Jason Sanford", "form_values": {"dc0e": "23"}, "client_created_at": "2014-10-15T22:25:14Z", "version": 2, "latitude": 35.5550349, "project_id": null, "status": null, "history_changed_by": "Jason Sanford", "updated_by": "Jason Sanford", "horizontal_accuracy": null, "history_id": "1e6fce5d-b9ae-4265-813f-1b30446faecf", "history_change_type": "u", "client_updated_at": "2014-10-15T22:25:14Z", "history_created_at": "2014-10-15T22:30:12Z", "created_at": "2014-10-15T22:25:14Z", "longitude": -80.93346194, "assigned_to": null, "created_by_id": "3f1efa091441405373600445"}], "per_page": 20000}',
            status=200)

        record_history = self.fulcrum_api.records.history('b88edefd-d6d5-4d8b-a45e-495f3541d94a')
        self.assertIsInstance(record_history, dict)
        self.assertEqual(len(record_history['records']), 2)
