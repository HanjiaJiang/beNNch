###############################################################################
# Import all necessary modules for simulation and plotting.

import os
import sys
import random

import nest
import numpy as np
import pandas as pd

import plots

###############################################################################
# Set simulation parameters.

sim_params = {
    "in_silico": False, # will load the in silico parameters if true
    "dt": 0.1,  # simulation resolution in ms
    "pre_sim_time": 100.0,  # pre-simulation time in ms (data not recorded)
    "sim_time": 100.0,  # simulation time in ms
    "N_analysis": 100,  # number of samples for analysis
    "n_threads": int(sys.argv[1]) if len(sys.argv) > 1 else os.cpu_count(),  # number of threads for NEST
    "seed": 1,  # seed for the random module
    "scale": 1, # scale of the model
}

###############################################################################
# Set network parameters.

model = "sparse" # "sparse" or "synchronous"

network_params = {
    "N_ex": 8000,  # number of excitatory neurons
    "N_in": 2000,  # number of inhibitory neurons
    "N_astro": 10000,  # number of astrocytes
    "CE": 1000,
    "CI": 1000,
    "p_third_if_primary": 0.5,  # probability of each created neuron-neuron connection to be paired with one astrocyte
    "pool_size": 10,  # astrocyte pool size for each target neuron
    "pool_type": "random",  # astrocyte pool will be chosen randomly for each target neuron
    "poisson_rate": 2000,  # Poisson input rate for neurons
    "scale": 1,
}

syn_params = {
    "w_a2n": 0.01,  # weight of astrocyte-to-neuron connection
    "w_e": 1.0,  # weight of excitatory connection in nS
    "w_i": -4.0,  # weight of inhibitory connection in nS
    "d_e": 2.0,  # delay of excitatory connection in ms
    "d_i": 1.0 if model == "sparse" else 2.0,  # delay of inhibitory connection in ms
}

###############################################################################
# Set astrocyte parameters.

astrocyte_model = "astrocyte_lr_1994"
astrocyte_params = {
    "delta_IP3": 0.5,  # Parameter determining the increase in astrocytic IP3 concentration induced by synaptic input
    "tau_IP3": 2.0,  # Time constant of the exponential decay of astrocytic IP3
}

###############################################################################
# Set neuron parameters.

neuron_model = "aeif_cond_alpha_astro"
tau_syn_ex = 2.0
tau_syn_in = 4.0 if model == "sparse" else 2.0

neuron_params_ex = {
    "tau_syn_ex": tau_syn_ex,  # excitatory synaptic time constant in ms
    "tau_syn_in": tau_syn_in,  # inhibitory synaptic time constant in ms
}

neuron_params_in = {
    "tau_syn_ex": tau_syn_ex,  # excitatory synaptic time constant in ms
    "tau_syn_in": tau_syn_in,  # inhibitory synaptic time constant in ms
}

###############################################################################
# This function creates the nodes and build the network. The astrocytes only
# respond to excitatory synaptic inputs; therefore, only the excitatory
# neuron-neuron connections are paired with the astrocytes. The
# TripartiteConnect() function and the "tripartite_bernoulli_with_pool" rule
# are used to create the connectivity of the network.


def create_astro_network(scale=1.0):
    """Create nodes for a neuron-astrocyte network."""
    print("Creating nodes ...")
    assert scale >= 1.0, "scale must be >= 1.0"
    nodes_ex = nest.Create(neuron_model, int(network_params["N_ex"] * scale), params=neuron_params_ex)
    nodes_in = nest.Create(neuron_model, int(network_params["N_in"] * scale), params=neuron_params_in)
    nodes_astro = nest.Create(astrocyte_model, int(network_params["N_astro"] * scale), params=astrocyte_params)
    nodes_noise = nest.Create("poisson_generator", params={"rate": network_params["poisson_rate"]})
    return nodes_ex, nodes_in, nodes_astro, nodes_noise


def connect_astro_network(nodes_ex, nodes_in, nodes_astro, nodes_noise, scale=1.0):
    """Connect the nodes in a neuron-astrocyte network.
    The astrocytes are paired with excitatory connections only.
    """
    print("Connecting Poisson generator ...")
    assert scale >= 1.0, "scale must be >= 1.0"
    nest.Connect(nodes_noise, nodes_ex + nodes_in, syn_spec={"weight": syn_params["w_e"]})
    print("Connecting neurons and astrocytes ...")
    # excitatory connections are paired with astrocytes
    # conn_spec and syn_spec according to the "tripartite_bernoulli_with_pool" rule
    conn_params_e = {"rule": "fixed_outdegree", "outdegree": network_params["CE"]}
    conn_params_astro = {
        "rule": "third_factor_bernoulli_with_pool",
        "p": network_params["p_third_if_primary"],
        "pool_size": network_params["pool_size"],
        "pool_type": network_params["pool_type"],
    }
    syn_params_e = {
        "primary": {
            "synapse_model": "tsodyks_synapse",
            "weight": syn_params["w_e"],
            "tau_psc": tau_syn_ex,
            "delay": syn_params["d_e"],
        },
        "third_in": {
            "synapse_model": "tsodyks_synapse",
            "weight": syn_params["w_e"],
            "tau_psc": tau_syn_ex,
            "delay": syn_params["d_e"],
        },
        "third_out": {"synapse_model": "sic_connection", "weight": syn_params["w_a2n"]},
    }
    nest.TripartiteConnect(
        nodes_ex,
        nodes_ex + nodes_in,
        nodes_astro,
        conn_spec=conn_params_e,
        third_factor_conn_spec=conn_params_astro,
        syn_specs=syn_params_e,
    )
    # inhibitory connections are not paired with astrocytes
    conn_params_i = {"rule": "fixed_outdegree", "outdegree": network_params["CI"]}
    syn_params_i = {
        "synapse_model": "tsodyks_synapse",
        "weight": syn_params["w_i"],
        "tau_psc": tau_syn_in,
        "delay": syn_params["d_i"],
    }
    nest.Connect(nodes_in, nodes_ex + nodes_in, conn_params_i, syn_params_i)

###############################################################################
# This function creates recording devices and connects them to the network.

def create_devices(exc, inh, astro):
    # create devices (multimeter default resolution = 1 ms)
    sr = nest.Create("spike_recorder")
    mm_neuron = nest.Create("multimeter", params={"record_from": ["I_SIC"]})
    mm_astro = nest.Create("multimeter", params={"record_from": ["IP3", "Ca_astro"]})
    # connect devices
    sampled_neurons = (exc + inh).tolist()
    astro_list = astro.tolist()
    assert len(sampled_neurons) > sim_params["N_analysis"], "Number of neurons not enough for N_analysis!"
    assert len(astro_list) > sim_params["N_analysis"], "Number of astrocytes not enough for N_analysis!"
    # connect all neurons to the spike recorder
    nest.Connect(sampled_neurons, sr)
    # connect N_analysis neurons and astrocytes to the multimeters
    sampled_neurons = sorted(random.sample(sampled_neurons, sim_params["N_analysis"]))
    sampled_astrocytes = sorted(random.sample(astro_list, sim_params["N_analysis"]))
    nest.Connect(mm_neuron, sampled_neurons)
    nest.Connect(mm_astro, sampled_astrocytes)
    return sr, mm_neuron, mm_astro

###############################################################################
# This function calculates the average neuronal firing rate

def calc_fr(events, n_neurons, start, end):
    mask = (events["times"]>=start)&(events["times"]<end)
    fr = 1000*len(events["times"][mask])/((end-start)*n_neurons)
    return fr

###############################################################################
# This function calculates the pairwise spike count correlations. For each pair
# of neurons, the correlation coefficient (Pearson's r) of their spike count
# histograms is calculated. The result of all pairs are returned.

def get_corr(hlist):
    coef_list = []
    n_pair_pass = 0
    n_pair_fail = 0
    for i, hist1 in enumerate(hlist):
        idxs = list(range(i + 1, len(hlist)))
        for j in idxs:
            hist2 = hlist[j]
            if np.sum(hist1) != 0 and np.sum(hist2) != 0:
                coef = np.corrcoef(hist1, hist2)[0, 1]
                coef_list.append(coef)
                n_pair_pass += 1
            else:
                n_pair_fail += 1
    if n_pair_fail > 0:
        print(f"n_pair_fail = {n_pair_fail}!")

    return coef_list, n_pair_pass, n_pair_fail


###############################################################################
# This function calculates the synchrony of neuronal firings.
# Histograms of spike counts of all neurons are obtained to evaluate local and
# global synchrony. The local synchrony is evaluated with average pairwise spike
# count correlation, and the global synchrony is evaluated with the variance of
# average spike count/average of variance of individual spike count.

def calc_synchrony(neuron_spikes, n_neurons, start, end, binwidth=10):
    # get data
    mask = (neuron_spikes["times"] >= start)&(neuron_spikes["times"] < end)
    senders = neuron_spikes["senders"][mask]
    times = neuron_spikes["times"][mask]
    rate = 1000 * len(senders) / ((end - start) * n_neurons)
    # sample neurons
    list_senders = list(set(senders))
    n_for_sync = len(list_senders)
    # make spike count histograms of individual neurons
    bins = np.arange(start, end + 0.1, binwidth)  # time bins
    hists = [np.histogram(times[senders == x], bins)[0].tolist() for x in set(senders)]
    # make spiking histogram of all sampled neurons
    hist_global = (np.histogram(times, bins)[0] / len(set(senders))).tolist()
    # calculate local and global synchrony
    coefs, n_pair_pass, n_pair_fail = get_corr(hists)  # local
    gsync = np.var(hist_global) / np.mean(np.var(hists, axis=1))  # global
    return rate, coefs, gsync, n_for_sync

###############################################################################
# This is the main function to run the simulation with.

def run():
    print(network_params)
    print(neuron_params_ex)

    # set NEST configuration
    nest.ResetKernel()
    nest.resolution = sim_params["dt"]
    nest.local_num_threads = sim_params["n_threads"]
    nest.print_time = True

    # use random seed for reproducible sampling
    random.seed(sim_params["seed"])

    # get short names
    pre_sim_time = sim_params["pre_sim_time"]
    sim_time = sim_params["sim_time"]

    # create and connect network and devices
    print("Creating network and devices ...")
    nodes_ex, nodes_in, nodes_astro, nodes_noise = create_astro_network(scale=sim_params["scale"])
    connect_astro_network(nodes_ex, nodes_in, nodes_astro, nodes_noise, scale=sim_params["scale"])
    sr, mm_neuron, mm_astro = create_devices(nodes_ex, nodes_in, nodes_astro)

    # run pre-simulation
    print("Running pre-simulation ...")
    nest.Simulate(pre_sim_time)

    # run simulation
    print("Running simulation ...")
    nest.Simulate(sim_time)

    # calculate average SIC in neurons
    I_SIC = np.mean(mm_neuron.events["I_SIC"][mm_neuron.events["times"]>=pre_sim_time])

    # get spiking data of all neurons and calculate average firing rate
    events = sr.events
    neurons = (nodes_ex + nodes_in).tolist()
    rate_network = calc_fr(events, len(neurons), pre_sim_time, pre_sim_time+sim_time)
    print(f"Network average neuronal firing rate = {rate_network:.2f}")

    # create plots
    plots.plot_benchmark_model(len(neurons), events, mm_astro.events, mm_neuron.events, model)

    # get spiking data of the first n_neurons_plot neurons for the raster plot and histogram
    #events_raster = {}
    #n_neurons_plot = 100
    #mask_raster = np.isin(events["senders"], neurons[:n_neurons_plot])
    #for key in ["times", "senders"]:
    #    events_raster[key] = events[key][mask_raster]
    #plots.plot_benchmark_model(n_neurons_plot, events_raster, mm_astro.events, mm_neuron.events, model)

    # synchrony analysis
    events_analysis = {}
    # filter by time
    mask_time = (events["times"]>=pre_sim_time)&(events["times"]<pre_sim_time+sim_time)
    for key in ["times", "senders"]:
        events_analysis[key] = events[key][mask_time]
    # sample (N_analysis) spiking neurons
    neurons_analysis = random.sample(list(set(events_analysis["senders"])), sim_params["N_analysis"])
    mask_neuron = np.isin(events_analysis["senders"], neurons_analysis)
    for key in ["times", "senders"]:
        events_analysis[key] = events_analysis[key][mask_neuron]
    # calculate and report synchrony
    rate, coefs, gsync, n_for_sync = calc_synchrony(
        events_analysis, sim_params["N_analysis"], pre_sim_time, pre_sim_time + sim_time
    )
    lsync, lsync_std = np.mean(coefs), np.std(coefs)
    print(f"Local synchrony = {lsync:.3f}+-{lsync_std:.3f}")
    print(f"Global synchrony = {gsync:.3f}")
    print(f"Firing rate of sampled neurons = {rate:.2f} spikes/s")
    print(f"(n = {n_for_sync} for synchrony analysis)")

    # save results
    data = {}
    data.update(sim_params)
    data.update(network_params)
    data.update(syn_params)
    for key, value in data.items():
        data[key] = [value]
    data["fr"] = [rate_network]
    data["lsync"] = [lsync]
    data["gsync"] = [gsync]
    data["n_for_sync"] = [n_for_sync]
    data["I_SIC"] = [I_SIC]
    df = pd.DataFrame(data)
    df.to_csv(f"{model}.csv", index=False)

    # plot n2a histogram
    n_n2a_hist = 100
    astro_conns = nest.GetConnections(nodes_ex, nodes_astro[:n_n2a_hist])
    astro_targets = astro_conns.get("target")
    plots.plot_conn_hist(astro_targets, subject="n2a", save_path=model, xlabel="Number of n2a connections of an astrocyte", ylabel="Number of cases", title="Fixed-outdegree")

    # plot n2a histogram
    n_a2n_hist = 100
    a2n_conns = nest.GetConnections(nodes_astro, nodes_ex[:n_a2n_hist])
    a2n_targets = a2n_conns.get("target")
    plots.plot_conn_hist(a2n_targets, subject="a2n", save_path=model, xlabel="Number of a2n connections of a neuron", ylabel="Number of cases", title="Fixed-outdegree")

    # plot n2n histogram
    n_n2n_hist = 100
    n2n_conns = nest.GetConnections(nodes_ex, nodes_ex[:n_n2n_hist])
    n2n_targets = n2n_conns.get("target")
    plots.plot_conn_hist(n2n_targets, subject="n2n", save_path=model, xlabel="Number of n2n connections of a neuron", ylabel="Number of cases", title="Fixed-outdegree")

###############################################################################
# Run the script.

os.system(f"mkdir -p {model}")
os.system(f"cp *.py {model}")
orig_stdout = sys.stdout
f = open(f'{model}/out.txt', 'w')
sys.stdout = f
run()
sys.stdout = orig_stdout
f.close()
