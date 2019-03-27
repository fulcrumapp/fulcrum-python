import unittest
import httpretty

from fulcrum import get_user
from tests import api_root


class GetUserTest(unittest.TestCase):
    @httpretty.activate
    def test_valid(self):
        httpretty.register_uri(httpretty.GET, api_root + '/users',
            body='{"user": {"id": 1, "email": "dude@email.com"}}',
            status=200)
        api_resp = get_user('dude@email.com', 'bad_password')
        self.assertIsInstance(api_resp, dict)
        self.assertTrue(api_resp['user']['email'] == 'dude@email.com')
