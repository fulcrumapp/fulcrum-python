import sys
import uuid

def is_string(s):
    if sys.version_info[0] == 3:
        return isinstance(s, str)
    else:
        return isinstance(s, basestring)

def generate_uuid():
    return str(uuid.uuid4())
