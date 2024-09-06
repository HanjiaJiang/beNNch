import os
import sys
import glob
import yaml
import csv

from analysis_helper import shell, load
from plot_all_quad import plot_all_quad
from plot_phases_quad import plot_phases_quad
from plot_thirdin import plot_thirdin
from plot_major import plot_major

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
    # analyse and save plot raw data to .csv
    if not os.path.isfile(timer_file_i):
        print(f"reload {timer_file_i} ...")
        shell(
            f"module load JUBE; jube analyse {config['jube_outpath']} --id {jube_id_i};"
            + f" jube result {config['jube_outpath']} --id {jube_id_i} > "
            + timer_file_i)

# Labels
try:
    labels = []
    for i in [5, 6, 7, 8]:
        labels.append(str(sys.argv[i]))
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
#cpu_info = load(os.path.join(bench_path[0], 'cpu.json'))
job_info = load(os.path.join(bench_path[0], 'job.json'))

# Strong or weak scaling (if not given, get it from job_info)
# This is for the "Network size" labeling for weak scaling cases
try:
    strength = job_info['scaling_type']
except:
    strength = 'strong'

# Plot layout
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

all_auto = True
if all_auto:
    cons_ylims = (0, None)
    conn_ylims = (None, None)
    prop_ylims = (0, None)
    spk_ylims = (None, None)

plot_major(
    timer_files,
    labels,
    data_paths[0],
    strength,
    x_axis=x_axis_label,
)

plot_phases_quad(
    timer_file_1=timer_files[0],
    timer_file_2=timer_files[1],
    timer_file_3=timer_files[2],
    timer_file_4=timer_files[3],
    save_path=data_paths[0],
    scaling_strength=strength,
    x_axis=x_axis_label,
    rtf_ylims=rtf_ylims,
    label_1=labels[0],
    label_2=labels[1],
    label_3=labels[2],
    label_4=labels[3],
    secondary=True,
    ignore_others=False,
)

# concatenate .csv files
def concatenate_csv_files(file_list, output_file):
    # Open the output file in write mode
    with open(output_file, 'w', newline='') as outfile:
        writer = csv.writer(outfile)

        # Variable to track if the header has been written
        header_written = False

        # Iterate through each file in the file list
        for file in file_list:
            with open(file, 'r') as infile:
                reader = csv.reader(infile)

                # Write the header only once
                if not header_written:
                    # Write the header (first row) from the first file
                    writer.writerow(next(reader))
                    header_written = True
                else:
                    # Skip the header for subsequent files
                    next(reader)

                # Write the remaining rows
                for row in reader:
                    writer.writerow(row)

output_csv = os.path.join(data_paths[0], "df_all.csv")

concatenate_csv_files(timer_files, output_csv)

plot_thirdin(
     timer_file_1=timer_files[0],
     save_path=data_paths[0],
     scaling_strength=strength,
     x_axis=x_axis_label,
     label_1=labels[0],
)
