from common.measurement_data import measurement_data
import numpy as np

class Squid(measurement_data):
    def __init__(self, path, axes=None):
        super().__init__(path, "squid")
        assert self.extension == "dat"

        if (self.title.find("MH") != -1) or (axes == "MH"):
            self.mode = "MH"
        elif self.title.find("MT") != -1 or (axes == "MT"):
            self.mode = "MT"
        else:
            raise ValueError("The loading mode can't be specified from the input file")
        if self.mode == "MH":
            col = [3,4]
        else: # MT
            col = [2,4]
        data = np.loadtxt(path , skiprows=36, delimiter=',', usecols=col)
        self.data = data.T
        if data.size < 8:
            raise ValueError("the data is empty")
        self.para = False
        self.axmode = "auto"
        self.update_axes()
        self.tesla = 0.

    def update_axes(self):
        if self.axmode == "auto":
            self.range = self.auto_range(self.data[0]) + self.auto_range(self.data[1])
        elif self.axmode == "x":
            yarr = self.data[1][(self.data[0] >= self.range[0]) & (self.data[0] <= self.range[1])]
            self.range = self.range[:2] + self.auto_range(yarr)
        elif self.axmode == "y":
            xarr = self.data[0][(self.data[1] >= self.range[2]) & (self.data[1] <= self.range[3])]
            self.range = self.auto_range(xarr) + self.range[:2]
        elif self.axmode == "xy":
            pass
        else:
            raise ValueError("'axmode' must be 'auto', 'x', 'y,' or 'xy'")

        symax = format(self.range[3], '.1E')
        yexp = int(symax[symax.find('E') + 1:])
        self.yexp = yexp if (yexp < -1 or yexp > 3) else 0
        sxmax = format(self.range[1], '.1E')
        xexp = int(sxmax[sxmax.find('E') + 1:])
        self.xexp = xexp if (xexp < -1 or xexp > 3) else 0