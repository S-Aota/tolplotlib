from common.measurement_data import measurement_data
import xml.etree.ElementTree as ET
import numpy as np
import matplotlib
import json

class Omega2Theta_data(measurement_data):
    def __init__(self, path):
        super().__init__(path)
        assert self.extension == "xrdxml"

        tree = ET.parse(path)
        prefix = "{http://www.xrdml.com/XRDMeasurement/1.7}"
        datapoint = tree.getroot().find(prefix+"xrdMeasurement").find(prefix+"scan").find(prefix+"dataPoints")
        xs = float(datapoint[0][0].text)
        xe = float(datapoint[0][1].text)

        self.count = np.array(list(map(int, datapoint[8].text.split())))
        self.theta2 = np.linspace(xs, xe, len(self.count))

class Omega2Theta(object):
    def __init__(self, *datas: Omega2Theta_data):
        self.datas = datas
        self.settings = json.load(open("xrd_config.json"))["Omega2Theta"]

    def plot_data(self, ax, axes_option,**kwargs):
        axes_option = self.settings["axes_option"].update(axes_option)
        plot_options = self.settings["plot_option"].update(kwargs)
        ax.set_xlabel(axes_option["xlabels"][axes_option["xunit"]])
        ax.set_ylabel(axes_option["ylabels"][axes_option["yunit"]])

        if axes_option["xunit"] == "2theta":
            fx =  lambda data: (data.theta2, data.count)
        elif axes_option["xunit"] == "omega":
            fx = lambda data: (data.theta2 / 2., data.count)
        else:
            raise ValueError("'axmode' must be 'auto', 'x', 'y,' or 'xy'")

        for i, data in enumerate(self.datas):
            plot_options = self.settings["plot_option"]
            ax.plot(*fx(data), **plot_options)


class ReciprocalSpaceMap(measurement_data):
    def __init__(self, path):
        super().__init__(path, "reciprocalspacemap")
        assert self.extension == "xrdxml"

        tree = ET.parse(path)
        datapoint = tree.getroot()
        counts = []
        theta2 = []
        omega = []
        for d in datapoint.iter("{http://www.xrdml.com/XRDMeasurement/1.7}scan"):
            c = list(map(int, d[-1][-1].text.split()))
            counts.append(c)
            theta2.append(np.linspace(float(d[-1][0][0].text), float(d[-1][0][1].text), len(c)))
            omega.append(np.linspace(float(d[-1][1][0].text), float(d[-1][1][1].text), len(c)))
        self.counts = np.stack(counts, axis=0)
        theta2 = np.stack(theta2, axis=0) / 180 * np.pi 
        omega = np.stack(omega, axis=0) / 180 * np.pi 
        self.phi = np.pi / 2 - theta2 / 2 + omega
        
        self.r = 2 * np.sin(theta2/2) * k_nolm
        self.x = self.r * np.cos(self.phi)
        self.y = self.r * np.sin(self.phi)

    def plot_args(self, cmin, cmax, **kwargs):
        default_kwargs = json.load(open("xrd_config.json"))["ReciprocalSpaseMap"]
        default_kwargs.update(kwargs)
        kwargs['norm'] = matplotlib.colors.Normalize(vmin=cmin, vmax=cmax)
        return [self.x, self.y, np.log(self.counts)], default_kwargs
