from fulcrum.mixins import Findable, Deleteable, Createable, Searchable, Updateable, Media, Track
from . import BaseAPI


class Forms(BaseAPI, Findable, Deleteable, Createable, Searchable, Updateable):
    path = 'forms'


class Records(BaseAPI, Findable, Deleteable, Createable, Searchable, Updateable):
    path = 'records'

    def history(self, id):
        api_resp = api_resp = self.call('get', '{0}/{1}/history'.format(self.path, id))
        return api_resp

class Webhooks(BaseAPI, Findable, Deleteable, Createable, Searchable, Updateable):
    path = 'webhooks'


class Photos(BaseAPI, Findable, Searchable, Media):
    path = 'photos'
    ext = 'jpg'
    sizes = ['thumbnail', 'large']


class Signatures(BaseAPI, Findable, Searchable, Media):
    path = 'signatures'
    ext = 'png'
    sizes = ['thumbnail', 'large']


class Videos(BaseAPI, Findable, Searchable, Media, Track):
    path = 'videos'
    ext = 'mp4'
    sizes = ['small', 'medium']


class Audio(BaseAPI, Findable, Searchable, Media, Track):
    path = 'audio'
    ext = 'mp4'
    sizes = []


class Memberships(BaseAPI, Searchable):
    path = 'memberships'


class Roles(BaseAPI, Searchable):
    path = 'roles'


class ChoiceLists(BaseAPI, Findable, Deleteable, Createable, Searchable, Updateable):
    path = 'choice_lists'


class ClassificationSets(BaseAPI, Findable, Deleteable, Createable, Searchable, Updateable):
    path = 'classification_sets'


class Projects(BaseAPI, Findable, Deleteable, Createable, Searchable, Updateable):
    path = 'projects'


class Changesets(BaseAPI, Findable, Createable, Searchable, Updateable):
    path = 'changesets'

    def close(self, id):
        api_resp = api_resp = self.call('put', '{0}/{1}/close'.format(self.path, id))
        return api_resp


class ChildRecords(BaseAPI, Searchable):
    path = 'child_records'
