from fulcrum.api import Client
from fulcrum.api.endpoints import (Forms, Records, Webhooks, Photos,
                                   Memberships, Roles, ChoiceLists, Signatures,
                                   ClassificationSets, Projects, Videos, Audio,
                                   Changesets, ChildRecords, AuditLogs, Layers,
                                   Authorizations)
from fulcrum.utils import is_string

__version__ = '1.12.0'

default_uri = 'https://api.fulcrumapp.com'


def create_authorization(email, password, organization_id, note,
                         timeout=None, user_id=None):
    if timeout is not None and not isinstance(timeout, int):
        raise ValueError('timeout must be an integer.')

    if user_id is not None and not is_string(user_id):
        raise ValueError('user_id must be a string.')

    auth = (email, password)
    client = Client(None, default_uri)
    data = {
        'authorization': {
            'organization_id': organization_id,
            'note': note,
            'timeout': timeout,
            'user_id': user_id
        }
    }
    api_resp = client.call('post', 'authorizations', auth=auth, data=data,
                           extra_headers={'Content-Type': 'application/json'})
    return api_resp


def get_user(email, password):
    auth = (email, password)
    client = Client(None, default_uri)
    api_resp = client.call('get', 'users', auth=auth)
    return api_resp


class Fulcrum(object):
    def __init__(self, key, uri=default_uri):
        self.client = Client(key=key, uri=uri)

        self.forms = Forms(client=self.client)
        self.records = Records(client=self.client)
        self.webhooks = Webhooks(client=self.client)
        self.photos = Photos(client=self.client)
        self.signatures = Signatures(client=self.client)
        self.memberships = Memberships(client=self.client)
        self.roles = Roles(client=self.client)
        self.choice_lists = ChoiceLists(client=self.client)
        self.classification_sets = ClassificationSets(client=self.client)
        self.projects = Projects(client=self.client)
        self.videos = Videos(client=self.client)
        self.audio = Audio(client=self.client)
        self.changesets = Changesets(client=self.client)
        self.child_records = ChildRecords(client=self.client)
        self.audit_logs = AuditLogs(client=self.client)
        self.layers = Layers(client=self.client)
        self.authorizations = Authorizations(client=self.client)

    def query(self, sql, format = 'json'):
        obj = {'q': sql, 'format': format}
        kwargs = {
            'data': obj,
            'extra_headers': {'Content-Type': 'application/json'}
        }

        kwargs['json_content'] = False if format == 'csv' else True

        api_resp = self.client.call('post', 'query', **kwargs)
        return api_resp
