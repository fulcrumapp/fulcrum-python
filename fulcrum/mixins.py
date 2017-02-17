class Findable(object):
    def find(self, id):
        api_resp = self.call('get', '{0}/{1}'.format(self.path, id))
        return api_resp


class Deleteable(object):
    def delete(self, id):
        self.call('delete', '{0}/{1}'.format(self.path, id))


class Createable(object):
    def create(self, obj):
        api_resp = self.call('post', self.path, data=obj, extra_headers={'Content-Type': 'application/json'})
        return api_resp


class Searchable(object):
    def search(self, url_params=None):
        api_resp = self.call('get', self.path, url_params=url_params)
        return api_resp


class Updateable(object):
    def update(self, id, obj):
        api_resp = self.call('put', '{0}/{1}'.format(self.path, id), data=obj, extra_headers={'Content-Type': 'application/json'})
        return api_resp


class Media(object):
    def media(self, id, size='original'):
        if size == 'original':
            path = '{}/{}.{}'.format(self.path, id, self.ext)
        else:
            if not size in self.sizes:
                raise ValueError('Size {} not supported'.format(size))
            path = '{}/{}/{}.{}'.format(self.path, id, size, self.ext)

        api_resp = self.call('get', path, json_content=False)
        return api_resp


class Track(object):
    track_formats = {
        'json': 'json',
        'geojson': 'geojson',
        'gpx': 'gpx',
        'kml': 'kml',
        'geojson_points': 'geojson?type=points',
    }

    def track(self, id, format='json'):
        if not format in self.track_formats.keys():
            raise ValueError('Format {} not supported'.format(size))
        path = '{}/{}/track.{}'.format(self.path, id, self.track_formats[format])

        api_resp = self.call('get', path, json_content=False)
        return api_resp
