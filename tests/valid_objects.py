form = {
    'form': {
        'name': 'Fire Hydrants',
        'description': 'Locations of fire hydrants near my house',
        'elements': [
            {
                'key': 'a',
                'label': 'Hydrant ID',
                'data_name': 'hydrant_id',
                'type': 'TextField',
                'description': 'The ID of the fire hydrant',
                'required': True,
                'hidden': False,
                'disabled': False
            },
            {
                'key': 'b',
                'label': 'Year Manufactured',
                'data_name': 'year_manufactured',
                'type': 'TextField',
                'description': 'The four digit year the hydrant was manufactured',
                'required': False,
                'hidden': False,
                'disabled': False,
                'numeric': True
            },
            {
                'key': 'c',
                'label': 'Structural',
                'data_name': 'structural',
                'type': 'Section',
                'description': 'Structural information about the hydrant',
                'required': False,
                'hidden': False,
                'disabled': False,
                'elements': [
                    {
                        'key': 'd',
                        'label': 'Color',
                        'data_name': 'color',
                        'type': 'ChoiceField',
                        'description': 'The color of the fire hydrant',
                        'required': True,
                        'hidden': False,
                        'disabled': False,
                        'choices': [
                            {
                                'value': 'red',
                                'label': 'Red'
                            },
                            {
                                'value': 'yellow',
                                'label': 'Yellow'
                            },
                            {
                                'value': 'white',
                                'label': 'White'
                            }
                        ],
                        'allow_other': True
                    },
                    {
                        'key': 'e',
                        'label': 'Height',
                        'data_name': 'height',
                        'type': 'TextField',
                        'description': 'The hight of the fire hydrant in meters',
                        'required': True,
                        'hidden': False,
                        'disabled': False,
                        'numeric': True
                    },
                    {
                        'key': 'f',
                        'label': 'Type',
                        'data_name': 'type',
                        'type': 'ClassificationField',
                        'classification_set_id': 9999,
                        'description': 'The type of fire hydrant',
                        'required': False,
                        'hidden': False,
                        'disabled': False
                    }
                ]
            }
        ]
    }
}

webhook = {
    'webhook': {
        'url': 'http://google.com/hookit',
        'name': 'The very best webhook',
        'active': True
    }
}

record = {
    'record': {
        'latitude': 40.678,
        'longitude': -100.567,
        'form_id': 'abc-123',
        'form_values': {
            'height': 34,
            'bathrooms': 2.5,
        }
    }
}
