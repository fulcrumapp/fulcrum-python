import json
import logging

import requests

from .exceptions import InvalidAPIVersionException, NotFoundException, UnauthorizedException, InvalidObjectException
from .validators import FormValidator

supported_versions = [2]


class APIConfig(object):
    uri_root = 'https://api.fulcrumapp.com/api/'

    def __init__(self, key, version=2):
        if version not in supported_versions:
            raise InvalidAPIVersionException

        self.key = key
        self.api_root = '{0}v{1}'.format(self.uri_root, version)


class BaseAPI(object):
    http_exception_map = {
        401: UnauthorizedException,
        404: NotFoundException,
    }

    def __init__(self, api_config):
        self.api_config = api_config

    def all(self):
        api_resp = self.call('get', self.path)
        return api_resp

    def create(self, obj):
        if hasattr(self, 'validator_class'):
            self.validator = self.validator_class(obj)
            print 'validator valid?: %s' % self.validator.valid
            if not self.validator.valid:
                raise InvalidObjectException(self.validator)
        api_resp = self.call('post', self.path, data=obj, extra_headers={'Content-Type': 'application/json'})
        return api_resp


    def delete(self, id):
        self.call('delete', '{0}/{1}'.format(self.path, id))

    def find(self, id):
        api_resp = self.call('get', '{0}/{1}'.format(self.path, id))
        return api_resp

    def call(self, method, path, data=None, extra_headers=None):
        full_path = self.api_config.api_root + path
        headers = {'X-ApiToken': self.api_config.key}
        if extra_headers is not None:
            headers.update(extra_headers)
        
        kwargs = {'headers': headers}

        if data is not None:
            kwargs['data'] = json.dumps(data)

        resp = getattr(requests, method)(full_path, **kwargs)
        
        if resp.status_code in self.http_exception_map:
            raise self.http_exception_map[resp.status_code]
        #print resp
        #print resp.content
        if method != 'delete':
            return resp.json()


class Form(BaseAPI):
    path = '/forms'
    validator_class = FormValidator