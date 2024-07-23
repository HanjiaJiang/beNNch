import os
import sys
import glob
import yaml

from analysis_helper import shell, load
from plot_all_quad import plot_all_quad
from plot_phases_quad import plot_phases_quad

import matplotlib.pyplot as plt
plt.rcParams.update({'font.size': 18})

# Load analysis configurations
with open('../config/analysis_config.yaml') as analysis_config_file:
    config = yaml.load(analysis_config_file, Loader=yaml.FullLoader)

# Load data
# first
jube_id_1 = str(sys.argv[1])
path_1 = os.path.join(config['jube_outpath'], jube_id_1.zfill(6))
timer_file_1=os.path.join(path_1, "timer_file.csv")
# analyse and save plot raw data to .csv
shell(
    f"module load JUBE; jube analyse {config['jube_outpath']} --id {jube_id_1};"
    + f" jube result {config['jube_outpath']} --id {jube_id_1} > "
    + timer_file_1)

# second
jube_id_2 = str(sys.argv[2])
path_2 = os.path.join(config['jube_outpath'], jube_id_2.zfill(6))
timer_file_2=os.path.join(path_2, "timer_file.csv")
shell(
    f"module load JUBE; jube analyse {config['jube_outpath']} --id {jube_id_2};"
    + f" jube result {config['jube_outpath']} --id {jube_id_2} > "
    + timer_file_2)

# third
jube_id_3 = str(sys.argv[3])
path_3 = os.path.join(config['jube_outpath'], jube_id_3.zfill(6))
timer_file_3=os.path.join(path_3, "timer_file.csv")
shell(
    f"module load JUBE; jube analyse {config['jube_outpath']} --id {jube_id_3};"
    + f" jube result {config['jube_outpath']} --id {jube_id_3} > "
    + timer_file_3)

# fourth
jube_id_4 = str(sys.argv[4])
path_4 = os.path.join(config['jube_outpath'], jube_id_4.zfill(6))
timer_file_4=os.path.join(path_4, "timer_file.csv")
shell(
    f"module load JUBE; jube analyse {config['jube_outpath']} --id {jube_id_4};"
    + f" jube result {config['jube_outpath']} --id {jube_id_4} > "
    + timer_file_4)

# Labels
try:
    label_1 = str(sys.argv[5])
    label_2 = str(sys.argv[6])
    label_3 = str(sys.argv[7])
    label_4 = str(sys.argv[8])
except:
    label_1 = "Sparse"
    label_2 = "Synchronous"
    label_3 = "Surrogate"
    label_4 = "No-SIC"

# X axis: "nodes" or "nvp"
# This is for the x-axis labeling: "Number of nodes" or "Number of threads"
# Use "nvp" for "Number of threads" (nvp strong scaling case)
try:
    x_axis_label = "num_nvp" if str(sys.argv[9]) == "nvp" else "num_nodes"
except:
    x_axis_label = "num_nodes"

# take the job and cpu info from first bench job, assuming all nodes are equal
bench_path = glob.glob(os.path.join(path_1, '*_bench/work'))
bench_path.sort()
cpu_info = load(os.path.join(bench_path[0], 'cpu.json'))
job_info = load(os.path.join(bench_path[0], 'job.json'))

# Strong or weak scaling (if not given, get it from job_info)
# This is for the "Network size" labeling for weak scaling cases
try:
    strength = job_info['scaling_type']
except:
    strength = 'strong'

if x_axis_label == "num_nvp":
    cons_ylims = (-0.25, 5.25)
    prop_ylims = (-5.0, 105.0)
    conn_ylims=(3990000, 4010000),
    spk_ylims = (-0.5, 10.5)
    rtf_ylims = (-0.5, 10.5)
elif strength == "strong":
    cons_ylims = (-0.5, 8.5)
#    cons_ylims = (-0.25, 5.25)
#    cons_ylims = (-0.2, 3.2)
#    cons_ylims = (-0.25, 5.25)
    prop_ylims = (-1.0, 36.0)
    spk_ylims = (2.85, 3.15)
#    spk_ylims = (-0.5, 10.5)
    rtf_ylims = (-0.2, 3.7)
else:
#    cons_ylims = (-0.5, 8.5)
#    cons_ylims = (-0.1, 2.1)
    cons_ylims = (-2.0, 57.0)
#    cons_ylims = (-2.0, 52.0)
    prop_ylims = (-2.0, 62.0)
#    prop_ylims = (-2.0, 52.0)
    spk_ylims = (2.85, 3.15)
#    spk_ylims = (-0.5, 10.5)
    rtf_ylims = (-0.2, 6.2)

plot_tsodyks = True
if plot_tsodyks:
    conn_plotted = "tsodyks_synapse"
    if strength == "weak":
        conn_ylims = (None, None)
    else:
        conn_ylims = (13990000, 14010000)
else:
    conn_plotted = "sic_connection"
    if strength == "weak":
        conn_ylims = (None, None)
    else:
        conn_ylims = (3990000, 4010000)

plot_all_quad(
    timer_file_1=timer_file_1,
    timer_file_2=timer_file_2,
    timer_file_3=timer_file_3,
    timer_file_4=timer_file_4,
    save_path=path_1,
    scaling_strength=strength,
    x_axis=x_axis_label,
    cons_ylims = cons_ylims,
    prop_ylims = prop_ylims,
    conn_ylims=conn_ylims,
    spk_ylims = spk_ylims,
    label_1=label_1,
    label_2=label_2,
    label_3=label_3,
    label_4=label_4,
    conn_plotted=conn_plotted,
)

plot_phases_quad(
    timer_file_1=timer_file_1,
    timer_file_2=timer_file_2,
    timer_file_3=timer_file_3,
    timer_file_4=timer_file_4,
    save_path=path_1,
    scaling_strength=strength,
    x_axis=x_axis_label,
    rtf_ylims=rtf_ylims,
    label_1=label_1,
    label_2=label_2,
    label_3=label_3,
    label_4=label_4,
)
