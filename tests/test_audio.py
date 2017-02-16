import httpretty

from tests import FulcrumTestCase


class AudioTest(FulcrumTestCase):
    @httpretty.activate
    def test_search(self):
        httpretty.register_uri(httpretty.GET, self.api_root + '/audio',
            body='{"audio": [{"id": 1},{"id": 2}], "total_count": 2, "current_page": 1, "total_pages": 1, "per_page": 20000}',
            status=200)

        audio = self.fulcrum_api.audio.search()
        self.assertIsInstance(audio, dict)
        self.assertEqual(len(audio['audio']), 2)

    @httpretty.activate
    def test_find(self):
        httpretty.register_uri(httpretty.GET, self.api_root + '/audio/5b656cd8-f3ef-43e9-8d22-84d015052778',
            body='{"id": "5b656cd8-f3ef-43e9-8d22-84d015052778"}',
            status=200)
        audio = self.fulcrum_api.audio.find('5b656cd8-f3ef-43e9-8d22-84d015052778')
        self.assertIsInstance(audio, dict)
        self.assertEqual(audio['id'], '5b656cd8-f3ef-43e9-8d22-84d015052778')
