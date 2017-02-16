from fulcrum.api import APIConfig
from fulcrum.api.endpoints import (Forms, Records, Webhooks, Photos,
                                   Memberships, Roles, ChoiceLists, Signatures,
                                   ClassificationSets, Projects, Videos, Audio,
                                   Changesets, ChildRecords)

__version__ = '1.4.3'


class Fulcrum(object):
    def __init__(self, key, uri='https://api.fulcrumapp.com'):
        api_config = APIConfig(key=key, uri=uri)
        self.forms = Forms(api_config=api_config)
        self.records = Records(api_config=api_config)
        self.webhooks = Webhooks(api_config=api_config)
        self.photos = Photos(api_config=api_config)
        self.signatures = Signatures(api_config=api_config)
        self.memberships = Memberships(api_config=api_config)
        self.roles = Roles(api_config=api_config)
        self.choice_lists = ChoiceLists(api_config=api_config)
        self.classification_sets = ClassificationSets(api_config=api_config)
        self.projects = Projects(api_config=api_config)
        self.videos = Videos(api_config=api_config)
        self.audio = Audio(api_config=api_config)
        self.changesets = Changesets(api_config=api_config)
        self.child_records = ChildRecords(api_config=api_config)
