## fulcrum-python

<img src="https://api.travis-ci.org/JasonSanford/fulcrum-python.png">

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
