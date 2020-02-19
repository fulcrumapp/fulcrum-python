import httpretty

from fulcrum.exceptions import NotFoundException, InternalServerErrorException

from tests import FulcrumTestCase
from tests.valid_objects import form as valid_form


class FormTest(FulcrumTestCase):
    @httpretty.activate
    def test_all(self):
        httpretty.register_uri(httpretty.GET, self.api_root + '/forms',
            body='{"forms": [{"id": 1},{"id": 2}], "total_count": 2, "current_page": 1, "total_pages": 1, "per_page": 20000}',
            status=200)

        forms = self.fulcrum_api.forms.search()
        self.assertIsInstance(forms, dict)
        self.assertEqual(len(forms['forms']), 2)

    @httpretty.activate
    def test_find(self):
        httpretty.register_uri(httpretty.GET, self.api_root + '/forms/5b656cd8-f3ef-43e9-8d22-84d015052778',
            body='{"record_count": 4, "description": "Food Carts and Trucks in Denver", "id": "5b656cd8-f3ef-43e9-8d22-84d015052778"}',
            status=200)
        form = self.fulcrum_api.forms.find('5b656cd8-f3ef-43e9-8d22-84d015052778')
        self.assertIsInstance(form, dict)
        self.assertEqual(form['id'], '5b656cd8-f3ef-43e9-8d22-84d015052778')

    @httpretty.activate
    def test_find_not_found(self):
        httpretty.register_uri(httpretty.GET, self.api_root + '/forms/lobster', status=404)
        try:
            self.fulcrum_api.forms.find('lobster')
        except Exception as exc:
            self.assertIsInstance(exc, NotFoundException)

    @httpretty.activate
    def test_delete(self):
        httpretty.register_uri(httpretty.DELETE, self.api_root + '/forms/5b656cd8-f3ef-43e9-8d22-84d015052778', status=200)
        self.fulcrum_api.forms.delete('5b656cd8-f3ef-43e9-8d22-84d015052778')

    @httpretty.activate
    def test_create_500(self):
        httpretty.register_uri(httpretty.POST, self.api_root + '/forms', status=500)
        try:
            self.fulcrum_api.forms.create(valid_form)
        except Exception as exc:
            self.assertIsInstance(exc, InternalServerErrorException)

    @httpretty.activate
    def test_create_valid(self):
        httpretty.register_uri(httpretty.POST, self.api_root + '/forms',
            body='{"form": {"id": 1}}',
            status=200)
        form = self.fulcrum_api.forms.create(valid_form)
        self.assertIsInstance(form, dict)
        self.assertTrue(form['form']['id'] == 1)

    @httpretty.activate
    def test_update(self):
        httpretty.register_uri(httpretty.PUT, self.api_root + '/forms/abc-123',
            body='{"form": {"id": "abc-123"}}',
            status=200)
        form = self.fulcrum_api.forms.update('abc-123', valid_form)
        self.assertIsInstance(form, dict)
        self.assertTrue(form['form']['id'] == 'abc-123')

    @httpretty.activate
    def test_form_history(self):
        httpretty.register_uri(httpretty.GET, self.api_root + '/forms/58ae9115-0430-459e-a1b7-7ac46011e0ce/history',
            body='{"current_page":1,"total_pages":1,"total_count":2,"per_page":20000,"forms":[{"id":"58ae9115-0430-459e-a1b7-7ac46011e0ce","name":"Davey Form Test","description":null,"version":1,"bounding_box":null,"record_title_key":"570c","title_field_keys":["570c"],"status_field":{"type":"StatusField","label":"Status","key":"@status","data_name":"status","default_value":"","enabled":false,"read_only":false,"hidden":false,"description":"","choices":[],"required":false,"disabled":false,"default_previous_value":false},"auto_assign":false,"hidden_on_dashboard":false,"record_count":0,"geometry_types":["Point"],"geometry_required":false,"script":null,"projects_enabled":null,"assignment_enabled":null,"created_by":"David McNight","created_by_id":"6df3ac95-7307-4b46-9b4e-23e50ca45858","updated_by":"David McNight","updated_by_id":"6df3ac95-7307-4b46-9b4e-23e50ca45858","elements":[{"type":"TextField","key":"570c","label":"What is a form?","description":null,"required":false,"disabled":false,"hidden":false,"data_name":"what_is_a_form","default_value":null,"visible_conditions_type":null,"visible_conditions_behavior":"clear","visible_conditions":null,"required_conditions_type":null,"required_conditions":null,"numeric":false,"pattern":null,"pattern_description":null,"min_length":null,"max_length":null,"default_previous_value":false}],"created_at":"2020-02-03T15:56:01Z","updated_at":"2020-02-03T15:56:01Z"},{"id":"58ae9115-0430-459e-a1b7-7ac46011e0ce","name":"Davey Form Test","description":null,"version":2,"bounding_box":null,"record_title_key":"570c","title_field_keys":["570c"],"status_field":{"type":"StatusField","label":"Status","key":"@status","data_name":"status","default_value":"","enabled":false,"read_only":false,"hidden":false,"description":"","choices":[],"required":false,"disabled":false,"default_previous_value":false},"auto_assign":false,"hidden_on_dashboard":false,"record_count":0,"geometry_types":["Point"],"geometry_required":false,"script":null,"projects_enabled":null,"assignment_enabled":null,"created_by":"David McNight","created_by_id":"6df3ac95-7307-4b46-9b4e-23e50ca45858","updated_by":"David McNight","updated_by_id":"6df3ac95-7307-4b46-9b4e-23e50ca45858","elements":[{"type":"TextField","key":"570c","label":"What is a form?","description":null,"required":false,"disabled":false,"hidden":false,"data_name":"what_is_a_form","default_value":null,"visible_conditions_type":null,"visible_conditions_behavior":"clear","visible_conditions":null,"required_conditions_type":null,"required_conditions":null,"numeric":false,"pattern":null,"pattern_description":null,"min_length":null,"max_length":null,"default_previous_value":false},{"type":"TextField","key":"137a","label":"What is a good city?","description":null,"required":false,"disabled":false,"hidden":false,"data_name":"what_is_a_good_city","default_value":null,"visible_conditions_type":null,"visible_conditions_behavior":"clear","visible_conditions":null,"required_conditions_type":null,"required_conditions":null,"numeric":false,"pattern":null,"pattern_description":null,"min_length":null,"max_length":null,"default_previous_value":false}],"created_at":"2020-02-03T15:56:01Z","updated_at":"2020-02-03T15:56:48Z"}]}',
            status=200)

        form_history = self.fulcrum_api.forms.history('58ae9115-0430-459e-a1b7-7ac46011e0ce')
        self.assertIsInstance(form_history, dict)
        self.assertEqual(len(form_history['forms']), 2)

    @httpretty.activate
    def test_form_history_single_version(self):
        httpretty.register_uri(httpretty.GET, self.api_root + '/forms/58ae9115-0430-459e-a1b7-7ac46011e0ce/history?version=1',
            body='{"current_page":1,"total_pages":1,"total_count":1,"per_page":20000,"forms":[{"id":"58ae9115-0430-459e-a1b7-7ac46011e0ce","name":"Davey Form Test","description":null,"version":1,"bounding_box":null,"record_title_key":"570c","title_field_keys":["570c"],"status_field":{"type":"StatusField","label":"Status","key":"@status","data_name":"status","default_value":"","enabled":false,"read_only":false,"hidden":false,"description":"","choices":[],"required":false,"disabled":false,"default_previous_value":false},"auto_assign":false,"hidden_on_dashboard":false,"record_count":0,"geometry_types":["Point"],"geometry_required":false,"script":null,"projects_enabled":null,"assignment_enabled":null,"created_by":"David McNight","created_by_id":"6df3ac95-7307-4b46-9b4e-23e50ca45858","updated_by":"David McNight","updated_by_id":"6df3ac95-7307-4b46-9b4e-23e50ca45858","elements":[{"type":"TextField","key":"570c","label":"What is a form?","description":null,"required":false,"disabled":false,"hidden":false,"data_name":"what_is_a_form","default_value":null,"visible_conditions_type":null,"visible_conditions_behavior":"clear","visible_conditions":null,"required_conditions_type":null,"required_conditions":null,"numeric":false,"pattern":null,"pattern_description":null,"min_length":null,"max_length":null,"default_previous_value":false}],"created_at":"2020-02-03T15:56:01Z","updated_at":"2020-02-03T15:56:01Z"}]}',
            status=200,
            match_querystring=True)

        form_history = self.fulcrum_api.forms.history('58ae9115-0430-459e-a1b7-7ac46011e0ce', url_params={'version': 1})
        self.assertIsInstance(form_history, dict)
        self.assertEqual(len(form_history['forms']), 1)
