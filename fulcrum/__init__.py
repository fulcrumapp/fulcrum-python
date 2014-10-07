from .api import APIConfig, Forms, Records, Webhooks, Photos, Memberships, Roles, ChoiceLists

__version__ = '1.0.0'


class Fulcrum(object):
    def __init__(self, key, uri='https://api.fulcrumapp.com'):
        api_config = APIConfig(key=key, uri=uri)
        self.forms = Forms(api_config=api_config)
        self.records = Records(api_config=api_config)
        self.webhooks = Webhooks(api_config=api_config)
        self.photos = Photos(api_config=api_config)
        self.memberships = Memberships(api_config=api_config)
        self.roles = Roles(api_config=api_config)
        self.choice_lists = ChoiceLists(api_config=api_config)
