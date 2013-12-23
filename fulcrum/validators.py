class BaseValidator(object):
    def __init__(self, obj):
        self.data = obj
        self.errors = {}
        self.validate()

    def add_error(self, key, data_name, error):
        if key in self.errors:
            if data_name in self.errors[key]:
                self.errors[key][data_name].append(error)
            else:
                self.errors[key][data_name] = [error]
        else:
            self.errors[key] = {}
            self.errors[key][data_name] = [error]

    @property
    def valid(self):
        return len(self.errors) == 0

    def __repr__(self):
        if len(self.errors):
            printable_errors = []
            for key in self.errors:
                for data_name in self.errors[key]:
                    for error in self.errors[key][data_name]:
                        error_sentence = '{0} {1} {2}.'.format(key, data_name, error)
                        printable_errors.append(error_sentence)
            return ' '.join(printable_errors)



class FormValidator(BaseValidator):
    def validate(self):
        if not 'dog' in self.data:
            self.add_error('dog', 'must', 'exist')