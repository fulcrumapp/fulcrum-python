import json

import requests

from fulcrum.exceptions import NotFoundException, UnauthorizedException, InternalServerErrorException


class APIConfig(object):
    def __init__(self, key, uri):
        self.key = key
        self.api_root = '{0}/api/v2/'.format(uri)


class BaseAPI(object):
    http_exception_map = {
        401: UnauthorizedException,
        404: NotFoundException,
        500: InternalServerErrorException,
    }

    def __init__(self, api_config):
        self.api_config = api_config

    def call(self, method, path, data=None, extra_headers=None, url_params=None):
        full_path = self.api_config.api_root + path
        headers = {
            'X-ApiToken': self.api_config.key,
            'Accept': 'application/json'
        }
        if extra_headers is not None:
            headers.update(extra_headers)

        kwargs = {'headers': headers}

        if data is not None:
            kwargs['data'] = json.dumps(data)

        if url_params is not None:
            kwargs['params'] = url_params

        resp = getattr(requests, method)(full_path, **kwargs)

        if resp.status_code in self.http_exception_map:
            raise self.http_exception_map[resp.status_code]

        if method == 'delete' or (method == 'put' and 'close' in path):
            # No body is returned for delete and close methods.
            return
        else:
            return resp.json()
