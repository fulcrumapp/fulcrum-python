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
        u'forms': [
            {
                u'name': u'Denver Street Food',
                u'id': u'5b656cd8-f3ef-43e9-8d22-84d015052778',
                ...
            }
        ],
        u'total_count': 3,
        u'current_page': 1,
        u'total_pages': 1,
        u'per_page': 20000
    }

#### Get a Sigle Form

    from fulcrum import Fulcrum

    fulcrum = Fulcrum(key='super-secret-key')

    form = fulcrum.form.find('5b656cd8-f3ef-43e9-8d22-84d015052778')

Returns a dict containing a form and raises `fulcrum.exceptions.NotFoundException` if the API returns a 404 (no form found)

    {
        u'form': {
            u'name': u'Denver Street Food',
            u'description': u'Food Carts and Trucks in Denver',
            u'bounding_box': [39.573714899036, -105.016159263187, 39.75146857094, -104.992259675735],
            u'elements': [
                {
                    u'data_name': u'name',
                    u'description': u'The name of that food joint',
                    u'label': u'Name',
                    u'key': u'4c0e',
                    u'type': u'TextField',
                    ...
                }
            ],
            u'id': u'5b656cd8-f3ef-43e9-8d22-84d015052778'
        }
    }

## Testing

You'll need some additional things to run tests, so:

    pip install -r test_requirements.txt

Run the tests:

    nosetests

You can get coverage too.

    nosetests --with-coverage

View coverage.

    coverage html
