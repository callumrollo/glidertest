import pytest
from glidertest import fetchers, tools, plots, utilities
import matplotlib.pyplot as plt
import numpy as np
import matplotlib
from ioos_qc import qartod

matplotlib.use('agg')  # use agg backend to prevent creating plot windows during tests


def test_plots(start_prof=0, end_prof=100):
    ds = fetchers.load_sample_dataset()
    ds = ds.drop_vars(['DENSITY'])
    fig, ax = plots.plot_basic_vars(ds, start_prof=start_prof, end_prof=end_prof)
    assert ax[0].get_ylabel() == 'Depth (m)'
    assert ax[0].get_xlabel() == f'{utilities.plotting_labels("TEMP")} \n({utilities.plotting_units(ds,"TEMP")})'

