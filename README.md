# fulcrum-python

[![Build Status](https://api.travis-ci.org/fulcrumapp/fulcrum-python.png)](https://travis-ci.org/fulcrumapp/fulcrum-python)&nbsp;[![PyPI version](https://img.shields.io/pypi/v/fulcrum.svg)](https://pypi.python.org/pypi/fulcrum/)

A library for working with [Fulcrum API](http://developer.fulcrumapp.com/api/intro/)

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
| Videos              | find, search, media, track, create   |
| Audio               | find, search, media, track, create   |
| Memberships         | search                               |
| Roles               | search                               |

## Usage

Create a fulcrum client with your API key.

```python
from fulcrum import Fulcrum
fulcrum = Fulcrum(key='super-secret-key')
```

Various methods are available for each of the resources. Results are returned as python-equivalent dicts of the JSON returned from the API. Check the [Fulcrum API Docs](http://www.fulcrumapp.com/developers/api/) for examples of returned objects.

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

Search for resources. The single parameter is `url_params` which should be passed as a dict, and will be properly url encoded. These will vary depending on the resource, but [pagination parameters](http://www.fulcrumapp.com/developers/api/introduction/#notes) are always accepted.

```python
records = fulcrum.records.search(url_params={'form_id': 'a1cb3ac7-146f-491a-a4a2-47737fb12074'})
print(len(records['records']))  # 9
print(records['records'][0]['id'])  # c90b0edf-0299-42df-bed4-524446d63f40
```

### Create

Create an object. The single parameter is a dict representation of a JSON object that will be POSTed to the API. Check the [Fulcrum API Docs](http://www.fulcrumapp.com/developers/api/) for examples of resource objects.

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
with open('photo_original.jpg', 'w') as f:
    f.write(photo)
```

Get the thumbnail instead.

```python
photo = fulcrum.photos.media('e58e80a8-9376-4a31-8e31-3cba95af0b4b', 'thumbnail')
with open('photo_thumb.jpg', 'w') as f:
    f.write(photo)
```

Do the same with videos.

```python
video = fulcrum.videos.media('45f85af9-65d1-4356-b8d1-6e713e926c22', 'small')
with open('video_small.mp4', 'w') as f:
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

## Examples

### Downloading Videos for a Form

Below is an example of downloading the first 3 videos and tracks for a form. You
could change the code below to download all videos and tracks for a form if
needed.

```python
from fulcrum import Fulcrum

api_key = 'your_api_key'

fulcrum = Fulcrum(key=api_key)

videos = fulcrum.videos.search({'page': 1, 'per_page': 3, 'form_id': '4a3f0a6d-c1d3-4805-9aab-7cdd39d58e5f'})

for video in videos['videos']:
    id = video['access_key']

    media = fulcrum.videos.media(id, 'small')
    track = fulcrum.videos.track(id, 'geojson')

    with open('{}_small.mp4'.format(id), 'w') as f:
        f.write(media)

    with open('{}.geojson'.format(id), 'w') as f:
          f.write(track)
```

### Updating Records via CSV File

Below is an example of looping through items in a csv file, finding the fulcrum record via its id, and updating the record with new values for a couple of fields.

```python
import csv

from fulcrum import Fulcrum
from fulcrum.exceptions import NotFoundException

api_key = 'your_api_key'
fulcrum = Fulcrum(key=api_key)
record_updates = csv.reader(open('record_updates.csv'), delimiter=',')

price_field_key = '9d69'
quantity_field_key = '1299'

"""
Assuming your csv file looks something like

record_id,price,quantity
abc-123,34.58,3
def-987,27.50,2
"""

# Skip the file header in csv (record_id,price,quantity)
next(record_updates, None)

# Loop through rows in csv
for row in record_updates:
    record_id = row[0]
    price = row[1]
    quantity = row[2]

    # Try to fetch an existing record, but continue looping if not found
    try:
        data = fulcrum.records.find(record_id)
    except NotFoundException:
        print('No record found with id ' + record_id)
        continue

    # Update fields with csv values
    data['record']['form_values'][price_field_key] = price
    data['record']['form_values'][quantity_field_key] = quantity

    # Send updates back to Fulcrum
    updated_record = fulcrum.records.update(record_id, data)
    print('record ' + record_id + ' successfully updated!')
```

### Updating a Record to add Repeatables

Below is an example of fetching an existing record, adding some "repeatable records" to the parent record, and updating the record.

```python
from fulcrum import Fulcrum
from fulcrum.exceptions import NotFoundException
# Import uuid module for generating repeatable IDs
import uuid

api_key = 'your-api-key'
fulcrum = Fulcrum(key=api_key)

# Find the record you want to update
record = fulcrum.records.find('a190b99c-be00-4793-a4b0-669fa9773c0c')

# Build an array of repeatable objects
repeatables = [{
  'id': str(uuid.uuid4()),
  'geometry': {
    'type': 'Point',
    'coordinates': [-82.6388836, 27.7707606]
  },
  'form_values': {
    'e8e3': '360 Central Ave'
  }
}, {
  'id': str(uuid.uuid4()),
  'geometry': {
    'type': 'Point',
    'coordinates': [-82.637812, 27.772983]
  },
  'form_values': {
    'e8e3': 'Williams Park'
  }
}]

# Add array to repeatable field
record['record']['form_values']['4501'] = repeatables

# Update the record
updated_record = fulcrum.records.update('a190b99c-be00-4793-a4b0-669fa9773c0c', record)
print('record successfully updated!')
```

## Testing

You'll need some additional things to run tests, so:

    pip install -r test_requirements.txt

Run the tests:

    nosetests

You can get coverage too.

    nosetests --with-coverage --cover-package fulcrum

View coverage.

    coverage html
