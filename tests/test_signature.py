import httpretty

from tests import FulcrumTestCase


class SignatureTest(FulcrumTestCase):
    @httpretty.activate
    def test_all(self):
        httpretty.register_uri(httpretty.GET, self.api_root + '/signatures',
            body='{"per_page": 20000, "total_count": 2, "signatures": [{"access_key": "86B51DB2", "uploaded": true, "form_id": "077da951", "url": "https://api.fulcrumapp.com/api/v2/signatures/8FC75D9873C2", "created_at": "2013-10-04T02:35:51Z", "updated_at": "2013-10-04T02:35:51Z", "stored": true, "processed": true, "content_type": "image/png", "file_size": 24177, "record_id": "efae1717"}, {"access_key": "D342A776", "uploaded": true, "form_id": "f65131d5fcfe", "url": "https://api.fulcrumapp.com/api/v2/signatures/17B68E234FAA", "created_at": "2013-10-04T02:36:55Z", "updated_at": "2013-10-04T02:36:55Z", "stored": true, "processed": true, "content_type": "image/png", "file_size": 34838, "record_id": "39f7eb9d9eb2"}], "total_pages": 1, "current_page": 1}',
            status=200)

        forms = self.fulcrum_api.signatures.search()
        self.assertIsInstance(forms, dict)
        self.assertEqual(len(forms['signatures']), 2)
