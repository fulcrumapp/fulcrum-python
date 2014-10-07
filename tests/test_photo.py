import httpretty
from nose.tools import raises

from tests import FulcrumTestCase


class PhotoTest(FulcrumTestCase):
    @httpretty.activate
    def test_records_from_form_via_url_params(self):
        httpretty.register_uri(httpretty.GET, self.api_root + '/photos/abc-123',
            body='{"photo": {"id": "abc-123"}}',
            status=200)

        photo = self.fulcrum_api.photos.find('abc-123')
        self.assertIsInstance(photo, dict)
        self.assertEqual(photo['photo']['id'], 'abc-123')

    @raises(AttributeError)
    def test_missing_delete(self):
        self.fulcrum_api.photos.delete('abc-123')

    @raises(AttributeError)
    def test_missing_create(self):
        self.fulcrum_api.photos.create({'id': 'abc-123'})

    @raises(AttributeError)
    def test_missing_update(self):
        self.fulcrum_api.photos.update('abc-123', {'id': 'abc-123'})
