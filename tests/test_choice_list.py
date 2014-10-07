import httpretty

from tests import FulcrumTestCase


class ChoiceListTest(FulcrumTestCase):
    @httpretty.activate
    def test_search(self):
        httpretty.register_uri(httpretty.GET, self.api_root + '/choice_lists',
            body='{"choice_lists": [{"id": 1},{"id": 2}], "total_count": 2, "current_page": 1, "total_pages": 1, "per_page": 20000}',
            status=200)

        choice_lists = self.fulcrum_api.choice_lists.search()
        self.assertIsInstance(choice_lists, dict)
        self.assertEqual(len(choice_lists['choice_lists']), 2)

    @httpretty.activate
    def test_find(self):
        httpretty.register_uri(httpretty.GET, self.api_root + '/choice_lists/5b656cd8-f3ef-43e9-8d22-84d015052778',
            body='{"id": "5b656cd8-f3ef-43e9-8d22-84d015052778"}',
            status=200)
        choice_list = self.fulcrum_api.choice_lists.find('5b656cd8-f3ef-43e9-8d22-84d015052778')
        self.assertIsInstance(choice_list, dict)
        self.assertEqual(choice_list['id'], '5b656cd8-f3ef-43e9-8d22-84d015052778')

    @httpretty.activate
    def test_delete(self):
        httpretty.register_uri(httpretty.DELETE, self.api_root + '/choice_lists/5b656cd8-f3ef-43e9-8d22-84d015052778', status=200)
        self.fulcrum_api.choice_lists.delete('5b656cd8-f3ef-43e9-8d22-84d015052778')

    @httpretty.activate
    def test_create(self):
        httpretty.register_uri(httpretty.POST, self.api_root + '/choice_lists',
            body='{"choice_list": {"id": 1}}',
            status=200)
        choice_list = self.fulcrum_api.choice_lists.create({'choice_list': {'id': '1'}})
        self.assertIsInstance(choice_list, dict)
        self.assertTrue(choice_list['choice_list']['id'] == 1)

    @httpretty.activate
    def test_update(self):
        httpretty.register_uri(httpretty.PUT, self.api_root + '/choice_lists/abc-123',
            body='{"choice_list": {"id": "abc-123"}}',
            status=200)
        choice_list = self.fulcrum_api.choice_lists.update('abc-123', {'choice_list': {'id': 'abc-123', 'name': 'Whatever'}})
        self.assertIsInstance(choice_list, dict)
        self.assertTrue(choice_list['choice_list']['id'] == 'abc-123')
