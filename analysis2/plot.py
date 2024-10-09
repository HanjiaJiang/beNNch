# This script do plotting only and does not need JUBE
import os
import sys
import glob
import yaml
import csv

import pandas as pd

from analysis_helper import load
from plot_phases import plot_phases
from plot_major import plot_major, plot_conn_fr
from plot_separate import plot_separate

import matplotlib.pyplot as plt
plt.rcParams.update({'font.size': 16})

# Load analysis configurations
config_file_name = '../config/analysis_config.yaml'
with open(config_file_name) as analysis_config_file:
    config = yaml.load(analysis_config_file, Loader=yaml.FullLoader)

# Load data
data_paths, timer_files = [], []
for i in [1, 2, 3, 4]:
    jube_id_i = str(sys.argv[i])
    path_i = os.path.join(config['jube_outpath'], jube_id_i.zfill(6))
    data_paths.append(path_i)
    timer_file_i = os.path.join(path_i, "timer_file.csv")
    timer_files.append(timer_file_i)

# Labels
try:
    labels = []
    for i in [5, 6, 7, 8]:
        labels.append(str(sys.argv[i]).replace('#', '\n'))
except:
    labels = ['Sparse', 'Synchronous', 'Surrogate', 'No Tripartite']

# X axis: "nodes" or "nvp"
# This is for the x-axis labeling: "Number of nodes" or "Number of threads"
# Use "nvp" for "Number of threads" (nvp strong scaling case)
try:
    x_axis_label = "num_nvp" if str(sys.argv[9]) == "nvp" else "num_nodes"
except:
    x_axis_label = "num_nodes"

# take the job and cpu info from first bench job, assuming all nodes are equal
bench_path = glob.glob(os.path.join(data_paths[0], '*_bench/work'))
bench_path.sort()
job_info = load(os.path.join(bench_path[0], 'job.json'))

# Strong or weak scaling (if not given, get it from job_info)
# This is for the "Network size" labeling for weak scaling cases
try:
    strength = job_info['scaling_type']
except:
    strength = 'strong'

# ylims
if x_axis_label == "num_nvp":
    cons_ylims = (-0.01, 0.11)
    if "Fixed-outdegree" in labels:
        conn_ylims = (-0.1, 2.1)
    else:
        conn_ylims = (-0.02, 0.52)
    rtf_ylims = (-0.5, 10.5)
elif strength == "strong":
    cons_ylims = (-0.01, 0.11)
    if "Fixed-outdegree" in labels:
        conn_ylims = (-0.1, 2.1)
    else:
        conn_ylims = (-0.02, 0.52)
    prop_ylims = (-1, 41)
    rtf_ylims = (-0.1, 3.1)
else:
    cons_ylims = (-0.01, 0.11)
    if "Fixed-outdegree" in labels:
        conn_ylims = (-0.1, 4.6)
    else:
        conn_ylims = (-0.02, 0.52)
    if "Sparse" in labels or "Bernoulli" in labels:
        prop_ylims = (-1, 41)
        rtf_ylims = (-0.1, 4.1)
    else:
        prop_ylims = (-1, 61)
        rtf_ylims = (-0.1, 6.1)

# plot major data
plot_major(
    timer_files,
    labels,
    data_paths[0],
    strength,
    x_axis=x_axis_label,
    cons_ylims=cons_ylims,
    conn_ylims=conn_ylims,
    prop_ylims=prop_ylims,
)

# plot connection number and firing rate
plot_conn_fr(
    timer_files,
    data_paths[0],
    strength,
    x_axis=x_axis_label,
)

# plot phases
for (detail, fontsize) in [(False, 'small'), (True, 'x-small')]:
    plot_phases(
        timer_files,
        labels,
        data_paths[0],
        strength,
        x_axis=x_axis_label,
        rtf_ylims=rtf_ylims,
        detail=detail,
        ignore_others=False,
        legend_fontsize=fontsize,
    )

# plot RTF of phases separately
plot_separate(
     timer_files,
     labels,
     data_paths[0],
     strength,
     quantities=['time_update_factor', 'spike_ccd_factor', 'secondary_gd_factor', 'others_factor'],
     file_postfix='rtf',
     ylabel_prefix='RTF of ',
    )

# plot memory data
plot_separate(
     timer_files,
     labels,
     data_paths[0],
     strength,
     quantities=['base_memory', 'network_memory', 'init_memory', 'total_memory'],
     file_postfix='memory',
    )

# concatenate and save results
def concat_df(file_list, output_file, labels_list):
    df_all = None
    for i, file_name in enumerate(file_list):
        if not os.path.isfile(file_name):
            break
        df = pd.read_csv(file_name)
        df["model"] = labels_list[i]
        if df_all is None:
            df_all = df.copy()
        else:
            df_all = pd.concat((df_all, df))
    df_all.to_csv(output_csv, index=False)

output_csv = os.path.join(data_paths[0], "df_all.csv")
concat_df(timer_files, output_csv, labels)
