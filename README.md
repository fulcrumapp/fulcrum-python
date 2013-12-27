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

## Usage

### Forms

#### Get All Forms

    from fulcrum import Fulcrum

    fulcrum = Fulcrum(key='super-secret-key')

    forms = fulcrum.form.all()

Returns a dict containing forms and pagination info

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

#### Get a Sigle Form

    from fulcrum import Fulcrum

    fulcrum = Fulcrum(key='super-secret-key')

    form = fulcrum.form.find('5b656cd8-f3ef-43e9-8d22-84d015052778')

Returns a dict containing a form and raises `fulcrum.exceptions.NotFoundException` if the API returns a 404 (no form found)

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

#### Delete a Form

    from fulcrum import Fulcrum

    fulcrum = Fulcrum(key='super-secret-key')

    fulcrum.form.delete('5b656cd8-f3ef-43e9-8d22-84d015052778')

Returns `None` on success and raises `fulcrum.exceptions.NotFoundException` if the API returns a 404 (no form found)

#### Update a Form

    from fulcrum import Fulcrum

    fulcrum = Fulcrum(key='super-secret-key')

    form = fulcrum.form.find('0552ca09-c521-4e48-b46c-9114e866ce06')

    form['form']['name'] = 'A better name for this form'

    new_form = fulcrum.form.update('0552ca09-c521-4e48-b46c-9114e866ce06', form)

Returns a dict containing the updated form and raises `fulcrum.exceptions.NotFoundException` if the API returns a 404 (no form found)

## Testing

You'll need some additional things to run tests, so:

    pip install -r test_requirements.txt

Run the tests:

    nosetests

You can get coverage too.

    nosetests --with-coverage

View coverage.

    coverage html
