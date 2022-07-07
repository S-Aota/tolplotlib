import os

class measurement_data(object):
    def __init__(self, path):
        self.path = path
        self.label, self.extension = os.path.splitext(os.path.basename(path))

def unwrap_args(default, args_dict, i):
    for key, value in args_dict.items():
        if hasattr(value, "__getitem__") and (not isinstance(value, str)):
            default[key] = value[i]
        else:
            default[key] = value
