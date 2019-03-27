import unittest
import httpretty

from fulcrum import create_authorization
from tests import api_root


class CreateAuthorizationTest(unittest.TestCase):
    @httpretty.activate
    def test_valid(self):
        httpretty.register_uri(httpretty.POST, api_root + '/authorizations',
            body='{"authorization": {"id": "abc-123", "token": "ab6c6266b3ef7bd204def18f8d54c837e84421acd7744d32d84966e0c260830b57de50be21ffd9b5", "token_last_8": "21ffd9b5", "note": "a note"}}',
            status=200)
        api_resp = create_authorization('dude@email.com', 'bad_password', 'def-456', 'a note')
        self.assertIsInstance(api_resp, dict)
        self.assertTrue(api_resp['authorization']['id'] == 'abc-123')

    @httpretty.activate
    def test_valid_with_timeout_user_id(self):
        httpretty.register_uri(httpretty.POST, api_root + '/authorizations',
            body='{"authorization": {"id": "abc-123", "token": "ab6c6266b3ef7bd204def18f8d54c837e84421acd7744d32d84966e0c260830b57de50be21ffd9b5", "token_last_8": "21ffd9b5", "note": "a note", "user_id": "987-zxy"}}',
            status=200)
        api_resp = create_authorization('dude@email.com', 'bad_password', 'def-456', 'a note', 3600, '987-zxy')
        self.assertIsInstance(api_resp, dict)
        self.assertTrue(api_resp['authorization']['user_id'] == '987-zxy')

    @httpretty.activate
    def test_bad_timeout(self):
        httpretty.register_uri(httpretty.POST, api_root + '/authorizations',
            body='{"authorization": {"id": "abc-123", "token": "ab6c6266b3ef7bd204def18f8d54c837e84421acd7744d32d84966e0c260830b57de50be21ffd9b5", "token_last_8": "21ffd9b5", "note": "a note"}}',
            status=200)
        try:
          create_authorization('dude@email.com', 'bad_password', 'def-456', 'a note', 888.76)
        except ValueError as exc:
          self.assertIsInstance(exc, ValueError)
          self.assertEqual(str(exc), 'timeout must be an integer.')

    @httpretty.activate
    def test_bad_user_id(self):
        httpretty.register_uri(httpretty.POST, api_root + '/authorizations',
            body='{"authorization": {"id": "abc-123", "token": "ab6c6266b3ef7bd204def18f8d54c837e84421acd7744d32d84966e0c260830b57de50be21ffd9b5", "token_last_8": "21ffd9b5", "note": "a note"}}',
            status=200)
        try:
          create_authorization('dude@email.com', 'bad_password', 'def-456', 'a note', 888, 7)
        except ValueError as exc:
          self.assertIsInstance(exc, ValueError)
          self.assertEqual(str(exc), 'user_id must be a string.')
