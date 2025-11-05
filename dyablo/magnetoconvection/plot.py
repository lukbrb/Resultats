import numpy as np
import matplotlib.pyplot as plt
import json

from pathlib import Path
from dataclasses import dataclass

import pyablo

from configparser import ConfigParser

config = ConfigParser(inline_comment_prefixes=('#',';'))
config.read('20251104_WB_hydro_with_mag/restart_WB_Hydro_and_Magneto_3660697.ini')

# Calculating domain size from the data
bx = config.getint('amr', 'bx')
by = config.getint('amr', 'by')
bz = config.getint('amr', 'bz')

lmin = config.getint('amr', 'level_min')
lmax = config.getint('amr', 'level_max')

if lmin != lmax:
    print('ERROR : This script only works for fixed grid runs')
    exit(1)

cor_x = config.getint('amr', 'coarse_oct_resolution_x')
cor_y = config.getint('amr', 'coarse_oct_resolution_y')
cor_z = config.getint('amr', 'coarse_oct_resolution_z')

xmin = config.getfloat('mesh', 'xmin')
xmax = config.getfloat('mesh', 'xmax')
zmin = config.getfloat('mesh', 'zmin')
zmax = config.getfloat('mesh', 'zmax')

Nx = bx*cor_x
Ny = by*cor_y
Nz = bz*cor_z

x = np.linspace(xmin, xmax, Nx)
y = np.linspace(xmin, xmax, Ny)
X, Y = np.meshgrid(x, y)

@dataclass
class PlotParams:
    directory: Path
    snapshot: Path | None
    main_file: Path | None
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

params = PlotParams.load_json("wb_no_correction")

r = pyablo.XdmfReader()
filename = Path(params.snapshot) if params.snapshot else Path(params.main_file)
path = params.directory / filename

fields = params.fields
NLABEL_X = params.NLabel_X
NLABEL_Y = params.NLabel_Y

assert NLABEL_X * NLABEL_Y == len(fields)

if not path.exists():
    print("File not found:", filename)
    exit(1)

all_iterations = r.readTimeSeries(str(path))

if not params.plot_series:
    all_iterations = [all_iterations[-1]]

y  = np.linspace(0.01, 0.99, 100)
xz = np.ones_like(y) * 0.5
line = np.stack((xz.T, y.T, xz.T)).T

for snapshot_name in all_iterations:
    s: pyablo.Snapshot
    file_path = params.directory / Path(snapshot_name)
    s = r.readSnapshot(str(file_path))
# s.print()

    print("Plotting file:", params.directory / file_path)
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

    rho = np.array(s.readAllFloat('rho')).reshape((Ny, Nx))
    vz = np.array(s.readAllFloat('rho_vz')).reshape((Ny, Nx))/rho

    rho_bar = np.average(rho, axis=1)
    rho_bar = np.tile(rho_bar, reps=(Nx, 1)).T
    rho_prime = rho - rho_bar
    Bx = np.array(s.readAllFloat('Bx')).reshape((Ny, Nx))
    By = np.array(s.readAllFloat('By')).reshape((Ny, Nx))
    Bz = np.array(s.readAllFloat('Bz')).reshape((Ny, Nx))
    # Bmag = np.sqrt(Bx**2 + By**2 + Bz**2)
    fig, ax = plt.subplots(2, 1, figsize=(10, 10))
    ax[0].imshow(rho_prime, cmap='bwr')
    ax[0].set_xlabel('x')
    ax[0].set_ylabel('y')
    ax[0].set_title(r'$\rho-\bar{\rho}$')

    ax[1].imshow(vz, cmap='bwr')
    ax[1].streamplot(X, Y, Bx, By, color='k', linewidth=0.5, density=2)
    ax[1].set_xlabel('x')
    ax[1].set_ylabel('y')
    ax[1].set_title(r'$v_z$')

    plt.tight_layout()
    plt.savefig("imgs/2D_rho_vz_" + snapshot_name.replace('.xmf', '.png'))
    plt.close(fig)
