import os
import pickle

import matplotlib
matplotlib.rcParams["font.size"] = 13
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.gridspec as gridspec

def plot_astro_dynamics(axe_ip3, events, start=0.0, xlims=(None, None), ylims_ip3=(None, None), ylims_calcium=(None, None)):
    # astrocyte data
    mask = events["times"] > start
    ip3 = events["IP3"][mask]
    calcium = events["Ca_astro"][mask]
    times = events["times"][mask]
    times_set = list(set(times))
    ip3_means = np.array([np.mean(ip3[times == t]) for t in times_set])
    ip3_sds = np.array([np.std(ip3[times == t]) for t in times_set])
    calcium_means = np.array([np.mean(calcium[times == t]) for t in times_set])
    calcium_sds = np.array([np.std(calcium[times == t]) for t in times_set])
    tab_blue = "tab:blue"
    pale_blue = "#D1E5F0"
    tab_green = "tab:green"
    pale_green = "#D9F0D3"
    # astrocytic IP3
    axe_ip3.set_ylabel(r"[IP$_{3}]$ ($\mu$M)")
    axe_ip3.tick_params(axis="y", labelcolor=tab_blue)
    axe_ip3.fill_between(
        times_set, ip3_means + ip3_sds, ip3_means - ip3_sds, linewidth=0.0, color=pale_blue
    )
    axe_ip3.plot(times_set, ip3_means, linewidth=1.5, color=tab_blue)
    axe_ip3.patch.set_visible(False)
    axe_ip3.set_xlim(xlims)
    axe_ip3.set_ylim(ylims_ip3)
    # astrocytic calcium
    axe_calcium = axe_ip3.get_figure().add_axes(axe_ip3.get_position())
    axe_calcium.set_ylabel(r"[Ca$^{2+}]$ ($\mu$M)", rotation=270, labelpad=20)
    axe_calcium.set_yticks([0.0, 0.5, 1.0])
    axe_calcium.tick_params(axis="y", labelcolor=tab_green)
    axe_calcium.fill_between(
        times_set, calcium_means + calcium_sds, calcium_means - calcium_sds, linewidth=0.0, color=pale_green)
    axe_calcium.plot(times_set, calcium_means, linewidth=1.5, color=tab_green)
    axe_calcium.yaxis.tick_right()
    axe_calcium.yaxis.set_label_position("right")
    axe_calcium.patch.set_visible(False)
    axe_calcium.set_xlim(xlims)
    axe_calcium.set_ylim(ylims_calcium)
    axe_calcium.spines[["left", "top", "bottom"]].set_visible(False)

def plot_neuro_sic(axe, events, start=0.0, xlims=(None, None), ylims=(None, None)):
    # neuron data
    mask = events["times"] > start
    sic = events["I_SIC"][mask]
    times = events["times"][mask]
    times_set = list(set(times))
    sic_means = np.array([np.mean(sic[times == t]) for t in times_set])
    sic_sds = np.array([np.std(sic[times == t]) for t in times_set])
    tab_purple = "tab:purple"
    pale_purple = "#E7D4E8"
    # neuron plot
    #axe.set_xlabel("Time (ms)")
    axe.set_ylabel(r"$I_\mathrm{SIC}$ (pA)")
    axe.fill_between(
        times_set, sic_means + sic_sds, sic_means - sic_sds, linewidth=0.0, color=pale_purple
    )
    axe.plot(times_set, sic_means, linewidth=1.5, color=tab_purple)
    axe.set_xlim(xlims)
    axe.set_ylim(ylims)

def filter_by_n(events, n_neurons, first_neuron=0):
    # get spiking data of the first n_neurons neurons for the raster plot
    events_raster = {}
    mask_raster = np.isin(events["senders"], np.arange(first_neuron, first_neuron + n_neurons))
    for key in ["times", "senders"]:
        events_raster[key] = events[key][mask_raster]
    return events_raster

def plot_raster(axe, events, xlims=(None, None), ylims=(None, None), n_neurons=100):
    # prepare data
    ts = events["times"]
    neurons = events["senders"]
    # filter
    events_raster = filter_by_n(events, n_neurons)
    # raster plot
    axe.plot(events_raster["times"], events_raster["senders"], ".k", markersize=2)
    axe.set_ylabel("Neurons")
    axe.set_xlim(xlims)
    axe.set_ylim(ylims)

def plot_hist(axe, events, n_neurons, binwidth=20, xlims=(None, None), ylims=(None, None)):
    # prepare data and figure
    ts = events["times"]
    neurons = events["senders"]
    # histogram
    bins = np.arange(np.amin(ts), np.amax(ts), float(binwidth)).tolist()
    hist, _ = np.histogram(ts, bins=bins)
    heights = 1000 * hist / (binwidth * n_neurons)
    axe.bar(bins[:-1], heights, width=binwidth, color="k", edgecolor="k")
    # axe.set_xlabel("Time (ms)")
    axe.set_ylabel("Firing rate\n(spikes/s)")
    axe.set_xlim(xlims)
    axe.set_ylim(ylims)
    axe.set_ylim(top=round(axe.get_ylim()[1]))

def set_broken_axes(axe, axe_top, ylims, bottom_frac=0.8, broken_frac=0.05):
    """This functions sets broken axes for extremely large values."""
    pos = axe.get_position()
    # set the axes on bottom (the original one)
    axe.set_position([pos.x0, pos.y0, pos.width, pos.height*bottom_frac])
    axe.set_ylim((ylims[0], (ylims[1]-ylims[0])*bottom_frac))
    axe.spines.top.set_visible(False)
    # set the axes on top
    ylims_ = axe_top.get_ylim()
    axe_top.set_position(
        [pos.x0, pos.y0+pos.height*(bottom_frac+broken_frac), pos.width, pos.height*(1-bottom_frac-broken_frac)])
    axe_top.set_ylabel(None)
    axe_top.set_xticks([])
    axe_top.set_yticks([ylims_[1]])
    axe_top.set_ylim((ylims_[1] - (ylims_[1] - ylims_[0])*(1-bottom_frac-broken_frac), ylims_[1]))
    axe_top.spines.bottom.set_visible(False)
    axe_top.patch.set_visible(False)
    # define the "slash strike" marker
    d = 0.1  # proportion of vertical to horizontal extent of the slanted line
    kwargs = dict(marker=[(-1, -d), (1, d)], markersize=12,
                  linestyle="none", color='k', mec='k', mew=1, clip_on=False)
    # slash strike at the bottom left of the top panel
    axe_top.plot([0], [0], transform=axe_top.transAxes, **kwargs)
    # slash strike at the top left of the bottom panel
    axe.plot([0], [1], transform=axe.transAxes, **kwargs)
    axe.yaxis.set_label_coords(-0.15, 0.5/bottom_frac, transform=axe.transAxes)
    # vertical segment to cover the gap between top and bottom panel on the right side
    axe_top.plot(
        [1, 1], [0, -0.5], 'k', linewidth=matplotlib.rcParams['axes.linewidth'], transform=axe_top.transAxes,
        clip_on=False)

def make_panels_benchmark_model(
    n_neurons_hist_1, events_sr_1, events_astro_1, events_neuro_1,
    n_neurons_hist_2, events_sr_2, events_astro_2, events_neuro_2,
    save_path="makefig_benchmark_model", fig_width=6):
    """This function makes separate panels for the simulation data."""
    # create save folder
    os.system(f"mkdir -p {save_path}")
    # xlims for all panels
    xlims = (0, 11000.0)
    # different ylims for different panels
    ylims_hist_low, ylims_hist_high = (0.0, 25.0), (0.0, 150.0)
    ylims_ip3, ylims_calcium = (-0.01, 0.91), (-0.02, 2.02)
    ylims_sic = (-5.0, 155.0)
    # position of axes for all panels
    pos = [0.2, 0.2, 0.6, 0.7]
    # A = raster plot, sparse
    fig_a, axe_a = plt.subplots(1, 1, figsize=(fig_width, 3))
    axe_a.set_position(pos)
    plot_raster(axe_a, events_sr_1, xlims=xlims)
    plt.savefig(f"{save_path}/benchmark_model_A.eps", dpi=400)
    plt.savefig(f"{save_path}/benchmark_model_A.png", dpi=400)
    plt.close()
    # B = raster plot, synchronous
    fig_b, axe_b = plt.subplots(1, 1, figsize=(fig_width, 3))
    axe_b.set_position(pos)
    plot_raster(axe_b, events_sr_2, xlims=xlims)
    plt.savefig(f"{save_path}/benchmark_model_B.eps", dpi=400)
    plt.savefig(f"{save_path}/benchmark_model_B.png", dpi=400)
    plt.close()
    # C = firing rate histogram, sparse
    fig_c, axe_c = plt.subplots(1, 1, figsize=(fig_width, 1.5))
    axe_c.set_position(pos)
    plot_hist(axe_c, events_sr_1, n_neurons_hist_1, ylims=ylims_hist_low, xlims=xlims)
    axe_c.set_ylabel("Firing rate\n(spikes/s)")
    plt.savefig(f"{save_path}/benchmark_model_C.eps", dpi=400)
    plt.savefig(f"{save_path}/benchmark_model_C.png", dpi=400)
    plt.close()
    # D = firing rate histogram, synchronous
    fig_d, axe_d = plt.subplots(1, 1, figsize=(fig_width, 1.5))
    axe_d.set_position(pos)
    plot_hist(axe_d, events_sr_2, n_neurons_hist_2, ylims=ylims_hist_high, xlims=xlims)
    axe_top_d = fig_d.add_axes(axe_d.get_position())
    plot_hist(axe_top_d, events_sr_2, n_neurons_hist_2, xlims=xlims)
    set_broken_axes(axe_d, axe_top_d, ylims_hist_high)
    plt.savefig(f"{save_path}/benchmark_model_D.eps", dpi=400)
    plt.savefig(f"{save_path}/benchmark_model_D.png", dpi=400)
    plt.close()
    # E = astrocytic dynamics, sparse
    fig_e, axe_e = plt.subplots(1, 1, figsize=(fig_width, 3))
    axe_e.set_position(pos)
    plot_astro_dynamics(axe_e, events_astro_1, ylims_ip3=ylims_ip3, ylims_calcium=ylims_calcium, xlims=xlims)
    plt.savefig(f"{save_path}/benchmark_model_E.eps", dpi=400)
    plt.savefig(f"{save_path}/benchmark_model_E.png", dpi=400)
    plt.close()
    # F = astrocytic dynamics, synchronous
    fig_f, axe_f = plt.subplots(1, 1, figsize=(fig_width, 3))
    axe_f.set_position(pos)
    plot_astro_dynamics(axe_f, events_astro_2, ylims_ip3=ylims_ip3, ylims_calcium=ylims_calcium, xlims=xlims)
    plt.savefig(f"{save_path}/benchmark_model_F.eps", dpi=400)
    plt.savefig(f"{save_path}/benchmark_model_F.png", dpi=400)
    plt.close()
    # G = SIC, sparse
    fig_g, axe_g = plt.subplots(1, 1, figsize=(fig_width, 1.5))
    axe_g.set_position(pos)
    plot_neuro_sic(axe_g, events_neuro_1, ylims=ylims_sic, xlims=xlims)
    plt.savefig(f"{save_path}/benchmark_model_G.eps", dpi=400)
    plt.savefig(f"{save_path}/benchmark_model_G.png", dpi=400)
    plt.close()
    # H = SIC, synchronous
    fig_h, axe_h = plt.subplots(1, 1, figsize=(fig_width, 1.5))
    axe_h.set_position(pos)
    plot_neuro_sic(axe_h, events_neuro_2, ylims=ylims_sic, xlims=xlims)
    plt.savefig(f"{save_path}/benchmark_model_H.eps", dpi=400)
    plt.savefig(f"{save_path}/benchmark_model_H.png", dpi=400)
    plt.close()

if __name__ == "__main__":
    with open(f"Sparse/data.pkl", "rb") as f:
        a1, b1, c1, d1 = pickle.load(f)
    with open(f"Synchronous/data.pkl", "rb") as f:
        a2, b2, c2, d2 = pickle.load(f)
    make_panels_benchmark_model(a1, b1, c1, d1, a2, b2, c2, d2)
    print("Figure is done!")
