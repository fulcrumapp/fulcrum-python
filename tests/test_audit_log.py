import httpretty

from fulcrum.exceptions import NotFoundException, InternalServerErrorException

from tests import FulcrumTestCase
from tests.valid_objects import form as valid_form


class AuditLogTest(FulcrumTestCase):
    @httpretty.activate
    def test_all(self):
        httpretty.register_uri(httpretty.GET, self.api_root + '/audit_logs',
            body='{"audit_logs": [{"id": 1},{"id": 2}], "total_count": 2, "current_page": 1, "total_pages": 1, "per_page": 20000}',
            status=200)

        audit_logs = self.fulcrum_api.audit_logs.search()
        self.assertIsInstance(audit_logs, dict)
        self.assertEqual(len(audit_logs['audit_logs']), 2)

    @httpretty.activate
    def test_find(self):
        httpretty.register_uri(httpretty.GET, self.api_root + '/audit_logs/5b656cd8-f3ef-43e9-8d22-84d015052778',
            body='{"record_count": 4, "description": "Food Carts and Trucks in Denver", "id": "5b656cd8-f3ef-43e9-8d22-84d015052778"}',
            status=200)
        audit_log = self.fulcrum_api.audit_logs.find('5b656cd8-f3ef-43e9-8d22-84d015052778')
        self.assertIsInstance(audit_log, dict)
        self.assertEqual(audit_log['id'], '5b656cd8-f3ef-43e9-8d22-84d015052778')

    @httpretty.activate
    def test_find_not_found(self):
        httpretty.register_uri(httpretty.GET, self.api_root + '/audit_logs/lobster', status=404)
        try:
            self.fulcrum_api.audit_logs.find('lobster')
        except Exception as exc:
            self.assertIsInstance(exc, NotFoundException)