# This script do plotting only and does not need JUBE
import os
import sys
import glob
import yaml
import csv

from analysis_helper import load
from plot_phases import plot_phases
from plot_major import plot_major, plot_conn_fr
from plot_separate import plot_separate

import matplotlib.pyplot as plt
plt.rcParams.update({'font.size': 15})

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

# Strong or weak scaling (if not given, get it from job_info)
# This is for the "Network size" labeling for weak scaling cases
bench_path = glob.glob(os.path.join(data_paths[0], '*_bench/work'))
bench_path.sort()
job_info = load(os.path.join(bench_path[0], 'job.json'))
try:
    strength = job_info['scaling_type']
except:
    strength = 'strong'

# ylims
if strength == "strong":
    rtf_ylims = (-0.1, 2.6)
else:
    if "Sparse" in labels or "Bernoulli" in labels:
        rtf_ylims = (-0.1, 3.6)
    else:
        rtf_ylims = (-0.1, 6.1)

# plot major data
plot_major(
    timer_files,
    labels,
    data_paths[0],
    strength,
    colors=['#004488','#994455','#997700','#6699cc'],
    styles=['-', '--', ':', ':'],
    lw=3,
)

# plot phases
for (detail, fontsize) in [(False, 'small'), (True, 'x-small')]:
    plot_phases(
        timer_files,
        labels,
        data_paths[0],
        strength,
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
     ['time_update_factor', 'spike_ccd_factor', 'secondary_gd_factor', 'others_factor'],
     colors=['#004488','#994455','#997700','#6699cc'],
     file_postfix='rtf',
     ylabel_prefix='RTF of ',
    )

