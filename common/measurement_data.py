import os

class measurement_data(object):
    def __init__(self, path, mode, label=None):
        self.path = path
        self.mode = mode
        self.label, self.extension = os.path.splitext(os.path.basename(path))
        if label:
            self.label = label

    def plot_args(self, x, y, ex, ey, **kwargs):
        return [x / 10 ** ex, y / 10 ** ey], kwargs
        