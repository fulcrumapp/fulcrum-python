import httpretty

from tests import FulcrumTestCase
from tests.valid_objects import webhook as valid_webhook


class WebhookTest(FulcrumTestCase):
    @httpretty.activate
    def test_create_valid(self):
        httpretty.register_uri(httpretty.POST, self.api_root + '/webhooks',
            body='{"webhook": {"id": 1}}',
            status=200)
        form = self.fulcrum_api.webhook.create(valid_webhook)
        self.assertIsInstance(form, dict)
        self.assertTrue(form['webhook']['id'] == 1)