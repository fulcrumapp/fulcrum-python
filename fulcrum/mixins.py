from fulcrum.utils import is_string, generate_uuid

class Findable(object):
    def find(self, id):
        api_resp = self.client.call('get', '{0}/{1}'.format(self.path, id))
        return api_resp


class Deleteable(object):
    def delete(self, id):
        self.client.call('delete', '{0}/{1}'.format(self.path, id))


class Createable(object):
    def create(self, obj):
        api_resp = self.client.call('post', self.path, data=obj, extra_headers={'Content-Type': 'application/json'})
        return api_resp


class Searchable(object):
    def search(self, url_params=None):
        api_resp = self.client.call('get', self.path, url_params=url_params)
        return api_resp


class Updateable(object):
    def update(self, id, obj):
        api_resp = self.client.call('put', '{0}/{1}'.format(self.path, id), data=obj, extra_headers={'Content-Type': 'application/json'})
        return api_resp


class Media(object):
    def media(self, id, size='original'):
        if size == 'original':
            path = '{}/{}.{}'.format(self.path, id, self.ext)
        else:
            if not size in self.sizes:
                raise ValueError('Size {} not supported'.format(size))
            path = '{}/{}/{}.{}'.format(self.path, id, size, self.ext)

        api_resp = self.client.call('get', path, json_content=False)
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


class MediaCreateable(object):
    def create(self, media_or_path, content_type=None, access_key=None):
        if is_string(media_or_path):
            media = open(media_or_path, 'rb')
        else:
            media = media_or_path

        data = {
            '{}[access_key]'.format(self.media_form_field_name): access_key or generate_uuid()
        }

        files = {
            '{}[file]'.format(self.media_form_field_name): (media.name, media, content_type or self.default_content_type)
        }

        api_resp = self.call('post', self.path + self.media_upload_path, data=data, files=files)
        return api_resp
