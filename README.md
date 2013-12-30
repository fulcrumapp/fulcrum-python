# fulcrum-python

[![Build Status](https://api.travis-ci.org/JasonSanford/fulcrum-python.png)](https://travis-ci.org/JasonSanford/fulcrum-python)&nbsp;[![Coverage Status](https://coveralls.io/repos/JasonSanford/fulcrum-python/badge.png?branch=master)](https://coveralls.io/r/JasonSanford/fulcrum-python?branch=master)

A library for working with [Fulcrum API](http://fulcrumapp.com/developers/api/)

## Status

This is a work in progress:

- [x] Forms
- [x] Records
- [ ] Webhooks
- [ ] Photos
- [ ] Classification Sets
- [ ] Choice Lists

## Installation

Install via pip:

    pip install fulcrum

or from local sources:

    python setup.py install

## Dependencies

Just one - [Requests](http://docs.python-requests.org/en/latest/) takes care of our HTTP chatting, and is automatically installed when using the steps above.

## Usage

### Forms

Get All Forms:

    from fulcrum import Fulcrum
    fulcrum = Fulcrum(key='super-secret-key')
    forms = fulcrum.form.all()

All returns a dict containing forms and pagination info:

    {
        'forms': [
            {
                'name': 'Denver Street Food',
                'id': '5b656cd8-f3ef-43e9-8d22-84d015052778',
                ...
            }
        ],
        'total_count': 3,
        'current_page': 1,
        'total_pages': 1,
        'per_page': 20000
    }

Create a Form:

    form = {
        'form': {
            'created_at': '2013-12-17T23:11:01Z',
            'record_count': 5,
            'name': 'Denver Street Food',
            'description': 'Food Carts and Trucks in Denver',
            'elements': [
                {
                    'default_value': None,
                    'data_name': 'name',
                    'description': 'The name of that food joint',
                    'label': 'Name',
                    'type': 'TextField'
                },
            ]
        }
    }
    created = fulcrum.form.create(form)

Get a Single Form:

    form = fulcrum.form.find('5b656cd8-f3ef-43e9-8d22-84d015052778')

Find returns a dict containing a form and raises `fulcrum.exceptions.NotFoundException` if the API returns a 404 (no form found).

    {
        'form': {
            'name': 'Denver Street Food',
            'description': 'Food Carts and Trucks in Denver',
            'bounding_box': [39.573714899036, -105.016159263187, 39.75146857094, -104.992259675735],
            'elements': [
                {
                    'data_name': 'name',
                    'description': 'The name of that food joint',
                    'label': 'Name',
                    'key': '4c0e',
                    'type': 'TextField',
                    ...
                }
            ],
            'id': '5b656cd8-f3ef-43e9-8d22-84d015052778'
        }
    }

Delete a Form:

    fulcrum.form.delete('5b656cd8-f3ef-43e9-8d22-84d015052778')

Delete returns `None` on success and raises `fulcrum.exceptions.NotFoundException` if the API returns a 404 (no form found).

Update a Form:

    form = fulcrum.form.find('0552ca09-c521-4e48-b46c-9114e866ce06')
    form['form']['name'] = 'A better name for this form'
    new_form = fulcrum.form.update('0552ca09-c521-4e48-b46c-9114e866ce06', form)

Update returns a dict containing the updated form and raises `fulcrum.exceptions.NotFoundException` if the API returns a 404 (no form found).

### Records

Get All Records

    from fulcrum import Fulcrum
    fulcrum = Fulcrum(key='super-secret-key')
    records = fulcrum.record.all()

All returns a dict containing forms and pagination info. In this case we're returning records from all forms, probably not something you'd want to do.

    {
        'per_page': 20000,
        'total_count': 16,
        'current_page': 1,
        'total_pages': 1,
        'records': [
            {
                'latitude': 39.6554223960635,
                'longitude': -105.000037243688,
                'altitude': 1629.0,
                'id': 'db3eff40-9b7b-4a37-baaa-c10891d1c2ec',
                'form_id': '49fd15ed-b24b-42ea-a0d5-2293276ec27e',
                'created_by': 'Jason Sanford',
                'form_values': {
                    '93d8': 'Englewood',
                    '0e7b': {
                        'choice_values': ['C', 'D'],
                        'other_values': []
                    }
                }
            },
            ...
        ]
    }

#### URL Parameters

Set URL parameters defined in the [Fulcrum Docs](http://fulcrumapp.com/developers/api/records/#query-params) to filter data for more accurate results. Supported parameters are `form_id`, `bounding_box`, `updated_since`, `project_id`, `page`, `per_page`. Below are a few examples.

Get records from a specific form:

    records = fulcrum.record.all(params={'form_id': '5b656cd8-f3ef-43e9-8d22-84d015052778'})

Get records within a bounding box:

    params = {
        'form_id': '5b656cd8-f3ef-43e9-8d22-84d015052778',
        'bounding_box': '39.55729,-105.05414,39.58931,-104.98273'
    }
    records = fulcrum.record.all(params=params)

Create a record:

    record = {
        'record': {
            'latitude': 39.6554223960635,
            'longitude': -105.000037243688,
            'altitude': 1629.0,
            'id': 'db3eff40-9b7b-4a37-baaa-c10891d1c2ec',
            'form_id': '49fd15ed-b24b-42ea-a0d5-2293276ec27e',
            'created_by': 'Jason Sanford',
            'form_values': {
                '93d8': 'Englewood',
                '0e7b': {
                    'choice_values': ['C', 'D'],
                    'other_values': []
                }
            }
        }
    }
    created_record = fulcrum.record.create(record)

Get a specific record:

    record = fulcrum.record.find('7465ddd4-3c8c-4c47-ac73-7963c076955a')

Update the record:

    record['record']['latitude'], record['record']['longitude'] = 0, 0
    record['record']['form_id'] = '5b656cd8-f3ef-43e9-8d22-84d015052778'
    fulcrum.record.update(record['record']['id'], record)

Delete the record:

    fulcrum.record.delete(record['record']['id'])

## Testing

You'll need some additional things to run tests, so:

    pip install -r test_requirements.txt

Run the tests:

    nosetests

You can get coverage too.

    nosetests --with-coverage

View coverage.

    coverage html
