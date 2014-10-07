import httpretty

from tests import FulcrumTestCase


class ClassificationSetTest(FulcrumTestCase):
    @httpretty.activate
    def test_search(self):
        httpretty.register_uri(httpretty.GET, self.api_root + '/classification_sets',
            body='{"classification_sets": [{"id": 1},{"id": 2}], "total_count": 2, "current_page": 1, "total_pages": 1, "per_page": 20000}',
            status=200)

        classification_sets = self.fulcrum_api.classification_sets.search()
        self.assertIsInstance(classification_sets, dict)
        self.assertEqual(len(classification_sets['classification_sets']), 2)

    @httpretty.activate
    def test_find(self):
        httpretty.register_uri(httpretty.GET, self.api_root + '/classification_sets/5b656cd8-f3ef-43e9-8d22-84d015052778',
            body='{"id": "5b656cd8-f3ef-43e9-8d22-84d015052778"}',
            status=200)
        classification_set = self.fulcrum_api.classification_sets.find('5b656cd8-f3ef-43e9-8d22-84d015052778')
        self.assertIsInstance(classification_set, dict)
        self.assertEqual(classification_set['id'], '5b656cd8-f3ef-43e9-8d22-84d015052778')

    @httpretty.activate
    def test_delete(self):
        httpretty.register_uri(httpretty.DELETE, self.api_root + '/classification_sets/5b656cd8-f3ef-43e9-8d22-84d015052778', status=200)
        self.fulcrum_api.classification_sets.delete('5b656cd8-f3ef-43e9-8d22-84d015052778')

    @httpretty.activate
    def test_create(self):
        httpretty.register_uri(httpretty.POST, self.api_root + '/classification_sets',
            body='{"classification_set": {"id": 1}}',
            status=200)
        classification_set = self.fulcrum_api.classification_sets.create({'classification_set': {'id': '1'}})
        self.assertIsInstance(classification_set, dict)
        self.assertTrue(classification_set['classification_set']['id'] == 1)

    @httpretty.activate
    def test_update(self):
        httpretty.register_uri(httpretty.PUT, self.api_root + '/classification_sets/abc-123',
            body='{"classification_set": {"id": "abc-123"}}',
            status=200)
        classification_set = self.fulcrum_api.classification_sets.update('abc-123', {'classification_set': {'id': 'abc-123', 'name': 'Whatever'}})
        self.assertIsInstance(classification_set, dict)
        self.assertTrue(classification_set['classification_set']['id'] == 'abc-123')
