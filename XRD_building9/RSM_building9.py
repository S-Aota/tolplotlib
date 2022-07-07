from common.measurement_data import measurement_data
import numpy as np
from matplotlib import colors
import json

class RSM_building9(measurement_data):
    def __init__(self, path):
        super().__init__(path, "reciprocalspacemap")
        assert self.extension == "csv"

        self.data = np.loadtxt(path , skiprows=2, delimiter=',').T
        
    def plot_args(self, cmin, cmax, **kwargs):
        default_kwargs = json.load(open("xrd_config.json"))["ReciprocalSpaseMap"]
        default_kwargs.update(kwargs)
        kwargs['norm'] = colors.Normalize(vmin=cmin, vmax=cmax)
        return [self.data[0], self.data[1], np.log(self.data[2])], kwargs
