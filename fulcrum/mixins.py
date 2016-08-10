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

class Downloadable(object):
    def get_original(self, id):
        api_resp = self.call('get', '{}/{}.{}'.format(self.path, id, self.dl_ext), json_content=False)
        return api_resp
    def get_size(self, id, size):
        if not size in self.dl_sizes:
            raise ValueError('Size {} not supported'.format(size))
        api_resp = self.call('get', '{}/{}/{}.{}'.format(self.path, id, size, self.dl_ext), json_content=False)
        return api_resp
