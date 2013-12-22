from .api import APIConfig, Form

__version__ = '0.0.1'


class Fulcrum(object):
    def __init__(self, key, version=2):
        api_config = APIConfig(key=key, version=version)
        self.form = Form(api_config=api_config)