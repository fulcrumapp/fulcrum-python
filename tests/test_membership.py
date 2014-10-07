import httpretty

from tests import FulcrumTestCase


class MembershipTest(FulcrumTestCase):
    @httpretty.activate
    def test_search(self):
        httpretty.register_uri(httpretty.GET, self.api_root + '/memberships',
            body='{"memberships": [{"id": 1},{"id": 2}], "total_count": 2, "current_page": 1, "total_pages": 1, "per_page": 20000}',
            status=200)

        memberships = self.fulcrum_api.memberships.search()
        self.assertIsInstance(memberships, dict)
        self.assertEqual(len(memberships['memberships']), 2)
