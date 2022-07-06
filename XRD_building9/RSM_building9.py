from common.measurement_data import measurement_data
import numpy as np

class RSM_building9(measurement_data):
    def __init__(self, path):
        super().__init__(path, "reciprocalspacemap")
        assert self.extension == "csv"

        data = np.loadtxt(path , skiprows=2, delimiter=',')
        

