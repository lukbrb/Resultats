import pyablo
import numpy as np
import matplotlib.pyplot as plt
import os
import json

from dataclasses import dataclass

DATA_TO_PLOT = "wb_total_pressure_bugfix"
@dataclass
class PlotParams:
    directory: str
    snapshot: str | None
    main_file: str | None
    plot_series: bool
    fields: list[str]
    NLabel_X: int
    NLabel_Y: int

    @classmethod
    def load_json(cls, plot_name:str, filepath: str = "plot_params.json") -> 'PlotParams':
        with open(filepath, 'r') as f:
            data = json.load(f)
        params = data.get(plot_name, {})
        
        return cls(
            directory=params.get('directory', ''),
            snapshot=params.get('snapshot', None),
            main_file=params.get('main_file', ''),
            plot_series=params.get('plot_series', False),
            fields=params.get('fields', []),
            NLabel_X=params.get('NLabel_X', 1),
            NLabel_Y=params.get('NLabel_Y', 1)
        )

params = PlotParams.load_json(DATA_TO_PLOT)

r = pyablo.XdmfReader()
filename = params.snapshot if params.snapshot else params.main_file
path = os.path.join(params.directory, filename)

fields = params.fields
NLABEL_X = params.NLabel_X
NLABEL_Y = params.NLabel_Y

assert NLABEL_X * NLABEL_Y == len(fields)

if not os.path.exists(path):
    print("File not found:", filename)
    exit(1)

all_iterations = r.readTimeSeries(path)

if not params.plot_series:
    all_iterations = [all_iterations[-1]]

y  = np.linspace(0.01, 0.99, 100)
xz = np.ones_like(y) * 0.5
line = np.stack((xz.T, y.T, xz.T)).T


for snapshot_name in all_iterations:
    file_path = os.path.join(params.directory, snapshot_name)
    s = r.readSnapshot(file_path)
# s.print()

    print("Plotting file:", os.path.join(params.directory, file_path))
    fig, ax = plt.subplots(NLABEL_X, NLABEL_Y, sharex=True, figsize=(10,10))
    fig.supxlabel('y')
    fig.suptitle(f'Field profiles along line x=0.5, z=0.5 at time {s.getTime():.2f}')

    for i in range(NLABEL_X):
        for j in range(NLABEL_Y):
            idx = i * NLABEL_Y + j
            field = fields[idx]
            ax[i, j].plot(y, s.probeQuantity(line, field), '-.', label=f'{field}')
            ax[i, j].set_ylabel(field)

    fig.tight_layout()
    plt.legend()
    plt.savefig("imgs/plot_" + snapshot_name.replace('.xmf', '.png'))
    plt.close(fig)

