# fulcrum-python

[![Build Status](https://api.travis-ci.org/fulcrumapp/fulcrum-python.png)](https://travis-ci.org/fulcrumapp/fulcrum-python)&nbsp;[![PyPI version](https://img.shields.io/pypi/v/fulcrum.svg)](https://pypi.python.org/pypi/fulcrum/)

A library for working with [Fulcrum API](https://learn.fulcrumapp.com/dev/rest/intro/)

## Installation

Install via pip:

    pip install fulcrum

or from local sources:

    python setup.py install

## Dependencies

Just one - [Requests](http://docs.python-requests.org/en/latest/) takes care of our HTTP chatting, and is automatically installed when using the steps above.

## Supported Resources and Methods

| Resource            | Methods                              |
|---------------------|--------------------------------------|
| Forms               | find, search, create, update, delete |
| Records             | find, search, create, update, delete |
| Photos              | find, search, media, create          |
| Signatures          | find, search, media, create          |
| Projects            | find, search, create, update, delete |
| Changesets          | find, search, create, update, close  |
| Choice Lists        | find, search, create, update, delete |
| Classification Sets | find, search, create, update, delete |
| Webhooks            | find, search, create, update, delete |
| Layers              | find, search, create, update, delete |
| Videos              | find, search, media, track, create   |
| Audio               | find, search, media, track, create   |
| Memberships         | search                               |
| Roles               | search                               |
| Audit Logs          | search, find                         |

## Usage

Create a fulcrum client with your API key.

```python
from fulcrum import Fulcrum
fulcrum = Fulcrum(key='super-secret-key')
```

Various methods are available for each of the resources. Results are returned as python-equivalent dicts of the JSON returned from the API. Check the [Fulcrum API Docs](https://learn.fulcrumapp.com/dev/rest/intro) for examples of returned objects.

## Forms

### fulcrum.forms.find(id)

### fulcrum.forms.search(url_params)

### fulcrum.forms.create(form)

### fulcrum.forms.update(id, form)

### fulcrum.forms.delete(id)

## Records

### fulcrum.records.find(id)

### fulcrum.records.search(url_params)

### fulcrum.records.create(record)

### fulcrum.records.update(id, record)

### fulcrum.records.delete(id)

## Photos

### fulcrum.photos.find(id)

### fulcrum.photos.search(url_params)

### fulcrum.photos.media(id, size)

### fulcrum.photos.create(media_or_path, content_type='image/jpeg', access_key=None)

## Signatures

### fulcrum.signatures.find(id)

### fulcrum.signatures.search(url_params)

### fulcrum.signatures.media(id, size)

### fulcrum.signatures.create(media_or_path, content_type='image/png', access_key=None)

## Videos

### fulcrum.videos.find(id)

### fulcrum.videos.search(url_params)

### fulcrum.videos.media(id, size)

### fulcrum.videos.track(id, format)

### fulcrum.videos.create(media_or_path, content_type='video/mp4', access_key=None)

## Audio

### fulcrum.audio.find(id)

### fulcrum.audio.search(url_params)

### fulcrum.audio.media(id, size)

### fulcrum.audio.track(id, format)

### fulcrum.audio.create(media_or_path, content_type='audio/mp3', access_key=None)

## Projects

### fulcrum.projects.find(id)

### fulcrum.projects.search(url_params)

### fulcrum.projects.create(form)

### fulcrum.projects.update(id, form)

### fulcrum.projects.delete(id)

## Choice Lists

### fulcrum.choice_lists.find(id)

### fulcrum.choice_lists.search(url_params)

### fulcrum.choice_lists.create(form)

### fulcrum.choice_lists.update(id, form)

### fulcrum.choice_lists.delete(id)

## Classification Sets

### fulcrum.classification_sets.find(id)

### fulcrum.classification_sets.search(url_params)

### fulcrum.classification_sets.create(form)

### fulcrum.classification_sets.update(id, form)

### fulcrum.classification_sets.delete(id)

## Webhooks

### fulcrum.webhooks.find(id)

### fulcrum.webhooks.search(url_params)

### fulcrum.webhooks.create(form)

### fulcrum.webhooks.update(id, form)

### fulcrum.webhooks.delete(id)

## Layers

### fulcrum.layers.find(id)

### fulcrum.layers.search(url_params)

### fulcrum.layers.create(form)

### fulcrum.layers.update(id, form)

### fulcrum.layers.delete(id)

## Changesets

### fulcrum.changesets.find(id)

### fulcrum.changesets.search(url_params)

### fulcrum.changesets.create(form)

### fulcrum.changesets.update(id, form)

### fulcrum.changesets.close(id)

## Memberships

### fulcrum.memberships.search(url_params)

## Roles

### fulcrum.roles.search(url_params)

## Common Methods

### Find

Finds a single resource. The single parameter is a resource id.

```python
form = fulcrum.forms.find('5b656cd8-f3ef-43e9-8d22-84d015052778')
print(form['form']['name'])  # Denver Street Food
```

### Search

Search for resources. The single parameter is `url_params` which should be passed as a dict, and will be properly url encoded. These will vary depending on the resource, but [pagination parameters](https://learn.fulcrumapp.com/dev/rest/intro#notes) are always accepted.

```python
records = fulcrum.records.search(url_params={'form_id': 'a1cb3ac7-146f-491a-a4a2-47737fb12074'})
print(len(records['records']))  # 9
print(records['records'][0]['id'])  # c90b0edf-0299-42df-bed4-524446d63f40
```

### Create

Create an object. The single parameter is a dict representation of a JSON object that will be POSTed to the API. Check the [Fulcrum API Docs](https://learn.fulcrumapp.com/dev/rest/intro/) for examples of resource objects.

```python
a_record = {
    'record': {
        'form_values': {
            'cbaf': 'A field value'
        },
        'form_id': 'a1cb3ac7-146f-491a-a4a2-47737fb12074'
    }
}
record = fulcrum.records.create(a_record)
print(record['record']['id'])  # e58e80a8-9376-4a31-8e31-3cba95af0b4b
```

### Update

Update an object. Parameters are an id, and dict representation of the JSON object that will be updated.

```python
an_updated_record = {
    'record': {
        'form_values': {
            'cbaf': 'An updated field value'
        },
        'form_id': 'a1cb3ac7-146f-491a-a4a2-47737fb12074'
    }
}
record = fulcrum.records.update('e58e80a8-9376-4a31-8e31-3cba95af0b4b', an_updated_record)
print(record['record']['form_values']['cbaf'])  # An updated field value
```

### Delete

Delete a resource. Delete returns `None` on success and raises `fulcrum.exceptions.NotFoundException` if the API returns a 404 (no resource found).

```python
fulcrum.records.delete('e58e80a8-9376-4a31-8e31-3cba95af0b4b')  # Returns None (assuming the record is found and deleted)
fulcrum.records.delete('a-bogus-resource-id')  # Raises fulcrum.exceptions.NotFoundException
```

### Media Method

The Fulcrum API endpoints that support media download have an extra `media`
method that will fetch the raw media.

The `size` options are:

| Resource            | Sizes                                |
|---------------------|--------------------------------------|
| Photos              | 'original', 'thumbnail', and 'large' |
| Signatures          | 'original', 'thumbnail', and 'large' |
| Videos              | 'original', 'small', and 'medium'    |
| Audio               | 'original'                           |

```python
photo = fulcrum.photos.media(id, size='original')
```

Skip the `size` parameter and get the default, original photo. Save it to disk.

```python
photo = fulcrum.photos.media('e58e80a8-9376-4a31-8e31-3cba95af0b4b')
with open('photo_original.jpg', 'wb') as f:
    f.write(photo)
```

Get the thumbnail instead.

```python
photo = fulcrum.photos.media('e58e80a8-9376-4a31-8e31-3cba95af0b4b', 'thumbnail')
with open('photo_thumb.jpg', 'wb') as f:
    f.write(photo)
```

Do the same with videos.

```python
video = fulcrum.videos.media('45f85af9-65d1-4356-b8d1-6e713e926c22', 'small')
with open('video_small.mp4', 'wb') as f:
    f.write(video)
```

### Track Method

The audio and video endpoints have an extra `track` method that will fetch a
track associated with the recording in multiple formats: `json` (default),
`geojson`, `gpx`, and `kml`.

Get the default json track output for an audio recording.

```python
track = fulcrum.audio.track('f0eb217d-3d4b-4ade-81b7-bac63788f396')
with open('track.json', 'w') as f:
    f.write(track)
```

Get a KML representation of a video track.

```python
track = fulcrum.videos.track('45f85af9-65d1-4356-b8d1-6e713e926c22', 'kml')
with open('track.kml', 'w') as f:
    f.write(track)
```

### Media Creation

Photos, videos, audio, and signatures can also be created. A single argument is
required: A path to the file, or a file object (via `open('file_name.ext')`).

```python
photo_path = 'door.jpg'
photo_resp = fulcrum.photos.create(photo_path)

video = open('video.mp4', 'rb')
video_resp = fulcrum.videos.create(video)
```

You can specifiy the file content type if you have a file type different than
the default.

```python
image_path = 'site_plan.png'
resp = fulcrum.photos.create(image_path, content_type='image/png')
```

IDs (access keys) are created automatically for new media objects, but you can
specify your own too.

```python
access_key = 'a743718b-8e62-484b-bbf3-600f5055a636'
audio_path = 'audio_recording.mp3'

resp = fulcrum.audio.create(audio_path, access_key=access_key)
```

### Query API

The client object has a `query` method that can be used to access the [Query API](https://learn.fulcrumapp.com/dev/query/intro). The arguments are a SQL string, and an optional format. The default format is `'json'`. Other formats are `'csv'` or `'geojson'`.

```python
# Get JSON, the default format.
as_json = fulcrum.query('SELECT * FROM Expenses LIMIT 1;')
print(as_json)
# {'fields': [{'name': '_record_id', 'type': 'string'}], 'time': 0.01, 'date': 1539895212724}

# CSV is cool too.
as_csv = fulcrum.query('SELECT * FROM Expenses LIMIT 1;', 'csv')
print(as_csv)
# '_record_id,_project_id,_assigned_to_id\nabc,123,def\n'

# Or get some GeoJSON.
as_geojson = fulcrum.query('SELECT * FROM Expenses LIMIT 1;', 'geojson')
print(as_geojson)
# {'type': 'FeatureCollection', 'features': [{'type': 'Feature', 'properties': {'_record_id': 'abc', '_project_id': '123'}, 'geometry': {'type': 'Point', 'coordinates': [-82.63707, 27.77102]}}]}
```

## Examples

https://github.com/fulcrumapp/fulcrum-python/wiki/Examples

## Hacking

Set up a virtual environment and source it:

    python -m venv my_venv
    source my_env/bin/activate

Install dependencies:

    python setup.py install

## Testing

You'll need some additional things to run tests, so:

    pip install -r test_requirements.txt

Run the tests:

    nosetests

You can get coverage too.

    nosetests --with-coverage --cover-package fulcrum

View coverage.

    nosetests --with-coverage --cover-package fulcrum --cover-html

## Publishing

Bump the version in `setup.py` *and* `__init__.py`:

```python
# setup.py
setup(
    name='fulcrum',  
    version='1.10.0',  # The next version
    ...
)
```

```python
# __init__.py
__version__ = '1.10.0' # The next version
```

Commit the changes above, tag, and push:

   git commit -am "Bump to version 1.10.0"
   git tag -a v1.10.0 -m "version 1.10.0"
   git push && git push --tags

Install the twine dependency:

    pip install twine

Then, package it up and upload:

    python setup.py sdist
    twine upload dist/*
