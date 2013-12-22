import requests

from .exceptions import InvalidAPIVersionException, NotFoundException, UnauthorizedException

supported_versions = [2]


class APIConfig(object):
    uri_root = 'https://api.fulcrumapp.com/api/'

    def __init__(self, key, version=2):
        if version not in supported_versions:
            raise InvalidAPIVersionException

        self.key = key
        self.api_root = '{0}v{1}'.format(self.uri_root, version)


class BaseAPI(object):
    exception_map = {
        401: UnauthorizedException,
        404: NotFoundException,
    }

    def call(self, method, path):
        full_path = self.api_config.api_root + path
        headers = {'X-ApiToken': self.api_config.key}
        
        resp = getattr(requests, method)(full_path, headers=headers)
        
        if resp.status_code in self.exception_map:
            raise self.exception_map[resp.status_code]
        #print resp
        #print resp.content
        if method == 'get':
            return resp.json()


class Form(BaseAPI):
    def __init__(self, api_config):
        self.api_config = api_config

    def all(self):
        api_resp = self.call('get', '/forms')
        return api_resp

    def find(self, id):
        api_resp = self.call('get', '/forms/{0}'.format(id))
        return api_resp

    def delete(self, id):
        self.call('delete', '/forms/{0}'.format(id))
