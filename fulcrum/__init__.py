from .api import APIConfig, Forms, Records, Webhooks

__version__ = '0.0.1'


class Fulcrum(object):
    def __init__(self, key, version=2):
        api_config = APIConfig(key=key, version=version)
        self.forms = Forms(api_config=api_config)
        self.records = Records(api_config=api_config)
        self.webhooks = Webhooks(api_config=api_config)
