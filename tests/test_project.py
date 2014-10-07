import httpretty

from tests import FulcrumTestCase


class ProjectTest(FulcrumTestCase):
    @httpretty.activate
    def test_search(self):
        httpretty.register_uri(httpretty.GET, self.api_root + '/projects',
            body='{"projects": [{"id": 1},{"id": 2}], "total_count": 2, "current_page": 1, "total_pages": 1, "per_page": 20000}',
            status=200)

        projects = self.fulcrum_api.projects.search()
        self.assertIsInstance(projects, dict)
        self.assertEqual(len(projects['projects']), 2)
