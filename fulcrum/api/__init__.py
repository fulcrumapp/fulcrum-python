import json

import requests

import fulcrum
from fulcrum.exceptions import NotFoundException, UnauthorizedException, InternalServerErrorException, RateLimitExceededException


class Client(object):
    http_exception_map = {
        401: UnauthorizedException,
        404: NotFoundException,
        429: RateLimitExceededException,
        500: InternalServerErrorException,
    }

    def __init__(self, key, uri):
        self.key = key
        self.api_root = '{0}/api/v2/'.format(uri)

    def call(self, method, path, data=None, extra_headers=None, url_params=None, json_content=True, files=None):
        full_path = self.api_root + path
        headers = {
            'X-ApiToken': self.key,
            'User-Agent': 'Fulcrum Python API Client, Version {}'.format(fulcrum.__version__),
        }

        if json_content:
            headers.update({'Accept': 'application/json'})

        if extra_headers is not None:
            headers.update(extra_headers)

        kwargs = {'headers': headers}

        if data is not None:
            if files:
                kwargs['data'] = data
            else:
                kwargs['data'] = json.dumps(data)

        if url_params is not None:
            kwargs['params'] = url_params

        if files is not None:
            kwargs['files'] = files

        resp = getattr(requests, method)(full_path, **kwargs)

        if resp.status_code in self.http_exception_map:
            raise self.http_exception_map[resp.status_code]

        if method == 'delete' or (method == 'put' and 'close' in path):
            # No body is returned for delete and close methods.
            return
        elif json_content:
            return resp.json()
        else:
            return resp.content


class BaseAPI(object):
    def __init__(self, client):
        self.client = client
