## fulcrum-python

[![Build Status](https://api.travis-ci.org/JasonSanford/fulcrum-python.png)](https://travis-ci.org/JasonSanford/fulcrum-python)&nbsp;[![Coverage Status](https://coveralls.io/repos/JasonSanford/fulcrum-python/badge.png?branch=master)](https://coveralls.io/r/JasonSanford/fulcrum-python?branch=master)

A library for working with [Fulcrum API](http://fulcrumapp.com/developers/api/)

### Status

This is a work in progress:

- [x] Forms
- [x] Records
- [ ] Webhooks
- [ ] Photos
- [ ] Classification Sets
- [ ] Choice Lists

### Testing

You'll need some additional things to run tests, so:

    pip install -r test_requirements.txt

Run the tests:

    nosetests

You can get coverage too.

    nosetests --with-coverage

View coverage.

    coverage html
