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


def test_up_down_bias(v_res=1):
    ds = fetchers.load_sample_dataset()
    fig, ax = plt.subplots()
    plots.plot_updown_bias(ds, var='PSAL', v_res=1, ax=ax)
    df = tools.quant_updown_bias(ds, var='PSAL', v_res=v_res)
    lims = np.abs(df.dc)
    assert ax.get_xlim() == (-np.nanpercentile(lims, 99.5), np.nanpercentile(lims, 99.5))
    assert ax.get_ylim() == (df.depth.max() + 1, -df.depth.max() / 30)
    assert ax.get_xlabel() == f'{utilities.plotting_labels("PSAL")} ({utilities.plotting_units(ds,"PSAL")})'
    # check without passing axis
    new_fig, new_ax = plots.plot_updown_bias(ds, var='PSAL', v_res=1)
    assert new_ax.get_xlim() == (-np.nanpercentile(lims, 99.5), np.nanpercentile(lims, 99.5))
    assert new_ax.get_ylim() == (df.depth.max() + 1, -df.depth.max() / 30)
    assert new_ax.get_xlabel() == f'{utilities.plotting_labels("PSAL")} ({utilities.plotting_units(ds,"PSAL")})'


def test_chl(var1='CHLA', var2='BBP700'):
    ds = fetchers.load_sample_dataset()
    ax = plots.process_optics_assess(ds, var=var1)
    assert ax.get_ylabel() == f'{utilities.plotting_labels(var1)} ({utilities.plotting_units(ds,var1)})'
    ax = plots.process_optics_assess(ds, var=var2)
    assert ax.get_ylabel() == f'{utilities.plotting_labels(var2)} ({utilities.plotting_units(ds,var2)})'
    with pytest.raises(KeyError) as e:
        plots.process_optics_assess(ds, var='nonexistent_variable')


def test_quench_sequence(ylim=45):
    ds = fetchers.load_sample_dataset()
    if not "TIME" in ds.indexes.keys():
        ds = ds.set_xindex('TIME')
    fig, ax = plt.subplots()
    plots.plot_quench_assess(ds, 'CHLA', ax, ylim=ylim)
    assert ax.get_ylabel() == 'Depth (m)'
    assert ax.get_ylim() == (ylim, -ylim / 30)

    fig, ax = plots.plot_daynight_avg(ds, var='TEMP')
    assert ax.get_ylabel() == 'Depth (m)'
    assert ax.get_xlabel() == f'{utilities.plotting_labels("TEMP")} ({utilities.plotting_units(ds,"TEMP")})'


def test_temporal_drift(var='DOXY'):
    ds = fetchers.load_sample_dataset()
    fig, ax = plt.subplots(1, 2)
    plots.check_temporal_drift(ds, var, ax)
    assert ax[1].get_ylabel() == 'Depth (m)'
    assert ax[0].get_ylabel() == f'{utilities.plotting_labels(var)} ({utilities.plotting_units(ds, var)})'
    assert ax[1].get_xlim() == (np.nanpercentile(ds[var], 0.01), np.nanpercentile(ds[var], 99.99))
    plots.check_temporal_drift(ds, 'CHLA')


def test_profile_check():
    ds = fetchers.load_sample_dataset()
    tools.check_monotony(ds.PROFILE_NUMBER)
    fig, ax = plots.plot_prof_monotony(ds)
    assert ax[0].get_ylabel() == 'Profile number'
    assert ax[1].get_ylabel() == 'Depth (m)'
    duration = tools.compute_prof_duration(ds)
    rolling_mean, overtime = tools.find_outlier_duration(duration, rolling=20, std=2)
    fig, ax = plots.plot_outlier_duration(ds, rolling_mean, overtime, std=2)
    assert ax[0].get_ylabel() == 'Profile duration (min)'
    assert ax[0].get_xlabel() == 'Profile number'
    assert ax[1].get_ylabel() == 'Depth (m)'


def test_basic_statistics():
    ds = fetchers.load_sample_dataset()
    plots.plot_glider_track(ds)
    plots.plot_grid_spacing(ds)
    plots.plot_ts(ds)


