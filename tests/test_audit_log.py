import httpretty

from fulcrum.exceptions import NotFoundException, InternalServerErrorException

from tests import FulcrumTestCase
from tests.valid_objects import form as valid_form


class AuditLogTest(FulcrumTestCase):
    @httpretty.activate
    def test_all(self):
        httpretty.register_uri(httpretty.GET, self.api_root + '/audit_logs',
            body='{"audit_logs":[{"source_type":"authorization","source_id":"ec4a410f-0b76-4a65-ba58-b97eed023351","action":"create","description":"Levar Burton created API token Fulcrum Query Utility","data":{"note":"Fulcrum Query Utility","token_last_8":"f816b890","user_id":"reading-rainbow","user":"Levar Burton"},"ip":"1.1.1.1","user_agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36","location":"Austin, Texas, United States","latitude":30.3085,"longitude":-97.6849,"admin_area":"TX","country":"US","locality":"Austin","postal_code":"78723","id":"def-456","created_at":"2019-01-16T15:14:58Z","updated_at":"2019-01-16T15:14:58Z","actor":"Levar Burton","actor_id":"8a11c2b4-79fc-4503-85e4-056671c41e6f","time":"2019-01-16T15:14:58Z"},{"source_type":"choice_list","source_id":"1c0b0ea3-66cd-4b69-9fe7-20a9e9f07556","action":"create","description":"Levar Burton created choice list New Choice List","data":null,"ip":"1.1.1.1","user_agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36","location":"Tampa, Florida, United States","latitude":27.9987,"longitude":-82.5156,"admin_area":"FL","country":"US","locality":"Tampa","postal_code":"33614","id":"ghi-789","created_at":"2019-01-22T16:11:15Z","updated_at":"2019-01-22T16:11:15Z","actor":"Levar Burton","actor_id":"094ed10f-cd99-4a58-9b4b-65ab5b31b791","time":"2019-01-22T16:11:15Z"}],"current_page":1,"total_pages":30,"total_count":60,"per_page":2}',
            status=200)

        audit_logs = self.fulcrum_api.audit_logs.search()
        self.assertIsInstance(audit_logs, dict)
        self.assertEqual(len(audit_logs['audit_logs']), 2)
        self.assertEqual(audit_logs['audit_logs'][0]['id'], 'def-456')
        self.assertEqual(audit_logs['audit_logs'][1]['id'], 'ghi-789')

    @httpretty.activate
    def test_find(self):
        httpretty.register_uri(httpretty.GET, self.api_root + '/audit_logs/abc-123',
            body='{"audit_log":{"source_type":"form","source_id":"zxy-987","action":"update","description":"Jason Sanford updated app GeoBooze - Changed:[Section:actions - YesNoField:post_to_slack];[RecordLinkField:beer_type];","data":null,"ip":"1.1.1.1","user_agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36","location":"Ashburn, Virginia, United States","latitude":39.0481,"longitude":-77.4728,"admin_area":"VA","country":"US","locality":"Ashburn","postal_code":"20149","id":"abc-123","created_at":"2019-01-10T17:29:16Z","updated_at":"2019-01-10T17:29:16Z","actor":"George Costanza","actor_id":"abc123","time":"2019-01-10T17:29:16Z"}}',
            status=200)
        audit_log = self.fulcrum_api.audit_logs.find('abc-123')
        self.assertIsInstance(audit_log, dict)
        self.assertEqual(audit_log['audit_log']['id'], 'abc-123')

