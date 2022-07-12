import numpy as np
from matplotlib import rcParams, colors, ticker
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import math

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

def plot(*data, cmap="jet", cmin=1, cmax=5, figsize=(12, 10)):
    cmin, cmax = float(cmin), float(cmax)
    cmap = cm.jet.copy()
    cmap.set_under(cmap(0))
    fig, ax = plt.subplots(figsize=figsize)
    label = np.arange(math.ceil(cmin), math.floor(cmax))
    for d in data:
        cs = ax.contourf(d[0], d[1], np.log10(d[2]), levels=100, cmap=cmap, norm=colors.Normalize(vmin=cmin, vmax=cmax))
    ax.set_aspect('equal')
    labeltick = [r"$10^{" +str(l) + "}$" for l in label]
    cbar = fig.colorbar(cs, ticks=label)
    cbar.ax.set_ylim(cmin ,cmax+1e-5)
    cbar.ax.set_yticklabels(labeltick)
    plt.xlabel(r"$\mathrm{Q_{xy}}\times 10000$ (rlu)")
    plt.ylabel(r"$\mathrm{Q_z}\times 10000$ (rlu)")
    cbar.outline.set_visible(False)