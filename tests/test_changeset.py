import httpretty

from tests import FulcrumTestCase


class ChangesetTest(FulcrumTestCase):
    @httpretty.activate
    def test_search(self):
        httpretty.register_uri(httpretty.GET, self.api_root + '/changesets',
            body='{"changesets": [{"id": 1},{"id": 2}], "total_count": 2, "current_page": 1, "total_pages": 1, "per_page": 20000}',
            status=200)

        changesets = self.fulcrum_api.changesets.search()
        self.assertIsInstance(changesets, dict)
        self.assertEqual(len(changesets['changesets']), 2)

    @httpretty.activate
    def test_find(self):
        httpretty.register_uri(httpretty.GET, self.api_root + '/changesets/5b656cd8-f3ef-43e9-8d22-84d015052778',
            body='{"id": "5b656cd8-f3ef-43e9-8d22-84d015052778"}',
            status=200)
        changeset = self.fulcrum_api.changesets.find('5b656cd8-f3ef-43e9-8d22-84d015052778')
        self.assertIsInstance(changeset, dict)
        self.assertEqual(changeset['id'], '5b656cd8-f3ef-43e9-8d22-84d015052778')

    @httpretty.activate
    def test_create(self):
        httpretty.register_uri(httpretty.POST, self.api_root + '/changesets',
            body='{"changeset": {"id": 1}}',
            status=200)
        changeset = self.fulcrum_api.changesets.create({'changeset': {'id': '1'}})
        self.assertIsInstance(changeset, dict)
        self.assertTrue(changeset['changeset']['id'] == 1)

    @httpretty.activate
    def test_update(self):
        httpretty.register_uri(httpretty.PUT, self.api_root + '/changesets/abc-123',
            body='{"changeset": {"id": "abc-123"}}',
            status=200)
        changeset = self.fulcrum_api.changesets.update('abc-123', {'changeset': {'id': 'abc-123', 'name': 'Whatever'}})
        self.assertIsInstance(changeset, dict)
        self.assertTrue(changeset['changeset']['id'] == 'abc-123')

    @httpretty.activate
    def test_close(self):
        httpretty.register_uri(httpretty.PUT, self.api_root + '/changesets/abc-123/close',
            status=200)
        self.fulcrum_api.changesets.close('abc-123')