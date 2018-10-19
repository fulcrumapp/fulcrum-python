from fulcrum.api import Client
from fulcrum.api.endpoints import (Forms, Records, Webhooks, Photos,
                                   Memberships, Roles, ChoiceLists, Signatures,
                                   ClassificationSets, Projects, Videos, Audio,
                                   Changesets, ChildRecords)

__version__ = '1.8.0'


class Fulcrum(object):
    def __init__(self, key, uri='https://api.fulcrumapp.com'):
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

    def query(self, sql, format = 'json'):
        obj = {'q': sql, 'format': format}
        kwargs = {
            'data': obj,
            'extra_headers': {'Content-Type': 'application/json'}
        }

        kwargs['json_content'] = False if format == 'csv' else True

        api_resp = self.client.call('post', 'query', **kwargs)
        return api_resp
