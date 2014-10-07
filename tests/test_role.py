import httpretty

from tests import FulcrumTestCase


class RoleTest(FulcrumTestCase):
    @httpretty.activate
    def test_search(self):
        httpretty.register_uri(httpretty.GET, self.api_root + '/roles',
            body='{"roles": [{"id": 1},{"id": 2}], "total_count": 2, "current_page": 1, "total_pages": 1, "per_page": 20000}',
            status=200)

        roles = self.fulcrum_api.roles.search()
        self.assertIsInstance(roles, dict)
        self.assertEqual(len(roles['roles']), 2)
