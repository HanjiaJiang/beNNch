import os
import sys
import glob
import yaml

from analysis_helper import shell, shell_return, load, git_annex
from plot_all import plot_all
from plot_phases import plot_phases

# Load analysis configurations
with open('../config/analysis_config.yaml') as analysis_config_file:
    config = yaml.load(analysis_config_file, Loader=yaml.FullLoader)

# Astrocyte data
jube_id = str(sys.argv[1])
base_path = os.path.join(config['jube_outpath'], jube_id.zfill(6))
uuidgen_hash = shell_return('uuidgen')
timer_file_astrocyte=os.path.join(base_path, "timer_file.csv")
#timer_file_astrocyte=os.path.join(base_path, uuidgen_hash + ".csv")
# analyse and save plot raw data to .csv
shell(
    f"module load JUBE; jube analyse {config['jube_outpath']} --id {jube_id};"
    + f" jube result {config['jube_outpath']} --id {jube_id} > "
    + timer_file_astrocyte)

# Control data
jube_id_ctrl = str(sys.argv[2])
ctrl_path = os.path.join(config['jube_outpath'], jube_id_ctrl.zfill(6))
uuidgen_hash_ctrl = shell_return('uuidgen')
timer_file_surrogate=os.path.join(ctrl_path, "timer_file.csv")
#timer_file_surrogate=os.path.join(ctrl_path, uuidgen_hash_ctrl + ".csv")
shell(
    f"module load JUBE; jube analyse {config['jube_outpath']} --id {jube_id_ctrl};"
    + f" jube result {config['jube_outpath']} --id {jube_id_ctrl} > "
    + timer_file_surrogate)

# X axis: "nodes" or "nvp"
# This is for the x-axis labeling: "Number of nodes" or "Number of threads"
# Use "nvp" for "Number of threads" (nvp strong scaling case)
try:
    tmp = str(sys.argv[3])
    x_axis_label = "num_nvp" if tmp == "nvp" else "num_nodes"
except:
    x_axis_label = "num_nodes"

# take the job and cpu info from first bench job, assuming all nodes are equal
bench_path = glob.glob(os.path.join(base_path, '*_bench/work'))
bench_path.sort()
cpu_info = load(os.path.join(bench_path[0], 'cpu.json'))
job_info = load(os.path.join(bench_path[0], 'job.json'))

# Strong or weak scaling (if not given, get it from job_info)
# This is for the "Network size" labeling for weak scaling cases
try:
    strength = job_info['scaling_type']
except:
    strength = 'strong'

# Data and control label
try:
    data_label = str(sys.argv[4])
    ctrl_label = str(sys.argv[5])
except:
    data_label = 'astrocyte_lr_1994'
    ctrl_label = 'astrocyte_surrogate'

if x_axis_label == "num_nvp":
    cons_ylims = (-0.25, 5.25)
    prop_ylims = (-1.0, 101.0)
    spk_ylims = (-0.5, 10.5)
    rtf_ylims = (-0.5, 10.5)
elif strength == "strong":
    cons_ylims = (-0.25, 5.25)
    prop_ylims = (-1.0, 36.0)
    spk_ylims = (-0.5, 10.5)
    rtf_ylims = (-0.2, 3.7)
else:
    cons_ylims = (-1.0, 101.0)
    prop_ylims = (-1.0, 101.0)
    spk_ylims = (-0.5, 10.5)
    rtf_ylims = (-0.2, 5.2)

plot_all(
    timer_hash=uuidgen_hash,
    timer_file_astrocyte=timer_file_astrocyte,
    timer_file_surrogate=timer_file_surrogate,
    save_path=base_path,
    scaling_strength=strength,
    x_axis=x_axis_label,
    cons_ylims = cons_ylims,
    prop_ylims = prop_ylims,
    spk_ylims = spk_ylims,
    data_label=data_label,
    ctrl_label=ctrl_label
)

plot_phases(
    timer_hash=uuidgen_hash,
    timer_file_astrocyte=timer_file_astrocyte,
    timer_file_surrogate=timer_file_surrogate,
    save_path=base_path,
    scaling_strength=strength,
    x_axis=x_axis_label,
    rtf_ylims=rtf_ylims,
    data_label=data_label,
    ctrl_label=ctrl_label
)
