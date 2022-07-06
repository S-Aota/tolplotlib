from common.measurement_data import measurement_data
import xml.etree.ElementTree as ET
import numpy as np

k_nolm = 1 / 0.1542e-9 / 1e10 * 1e4 # (/aa)

class Omega2Theta(measurement_data):
    def __init__(self, path):
        super().__init__(path, "omega2theta")
        assert self.extension == "xrdxml"

        tree = ET.parse(path)
        prefix = "{http://www.xrdml.com/XRDMeasurement/1.7}"
        datapoint = tree.getroot().find(prefix+"xrdMeasurement").find(prefix+"scan").find(prefix+"dataPoints")
        xs = float(datapoint[0][0].text)
        xe = float(datapoint[0][1].text)

        self.count = np.array(list(map(int, datapoint[8].text.split())))
        self.theta2 = np.linspace(xs, xe, len(self.count))

    def plot_args(self, ex, ey, **kwargs):
        return super().plot_args(self.theta2, self.count, ex, ey, **kwargs)

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
