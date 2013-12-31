import copy

from fulcrum.exceptions import InvalidObjectException

from tests import FulcrumTestCase
from tests.valid_objects import webhook as valid_webhook


class WebhookTest(FulcrumTestCase):
    def test_no_webhook(self):
        a_webhook = copy.deepcopy(valid_webhook)
        del a_webhook['webhook']
        try:
            self.fulcrum_api.webhook.create(a_webhook)
        except Exception as exc:
            self.assertIsInstance(exc, InvalidObjectException)
            self.assertEqual(str(exc), 'webhook must exist and not be empty.')

    def test_no_url(self):
        a_webhook = copy.deepcopy(valid_webhook)
        del a_webhook['webhook']['url']
        try:
            self.fulcrum_api.webhook.create(a_webhook)
        except Exception as exc:
            self.assertIsInstance(exc, InvalidObjectException)
            self.assertEqual(str(exc), 'webhook url must exist.')

    def test_active_not_a_bool(self):
        a_webhook = copy.deepcopy(valid_webhook)
        a_webhook['webhook']['active'] = 'lobster'
        try:
            self.fulcrum_api.webhook.create(a_webhook)
        except Exception as exc:
            self.assertIsInstance(exc, InvalidObjectException)
            self.assertEqual(str(exc), 'webhook active must be of type bool.')
