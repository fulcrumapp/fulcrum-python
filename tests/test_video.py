import httpretty

from tests import FulcrumTestCase


class VideoTest(FulcrumTestCase):
    @httpretty.activate
    def test_search(self):
        httpretty.register_uri(httpretty.GET, self.api_root + '/videos',
            body='{"videos": [{"id": 1},{"id": 2}], "total_count": 2, "current_page": 1, "total_pages": 1, "per_page": 20000}',
            status=200)

        videos = self.fulcrum_api.videos.search()
        self.assertIsInstance(videos, dict)
        self.assertEqual(len(videos['videos']), 2)

    @httpretty.activate
    def test_find(self):
        httpretty.register_uri(httpretty.GET, self.api_root + '/videos/5b656cd8-f3ef-43e9-8d22-84d015052778',
            body='{"id": "5b656cd8-f3ef-43e9-8d22-84d015052778"}',
            status=200)
        video = self.fulcrum_api.videos.find('5b656cd8-f3ef-43e9-8d22-84d015052778')
        self.assertIsInstance(video, dict)
        self.assertEqual(video['id'], '5b656cd8-f3ef-43e9-8d22-84d015052778')
