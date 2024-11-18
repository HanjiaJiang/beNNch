# This script do plotting only and does not need JUBE
import os
import sys
import glob
import yaml
import csv

from analysis_helper import load
from plot_major import plot_major
from plot_phases import plot_phases
from plot_separate import plot_separate

import matplotlib.pyplot as plt
plt.rcParams.update({'font.size': 15})

def plot():
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

    # Set save path to the first data path
    save_path = data_paths[0]

    # Get labels
    labels = sys.argv[5:9]

    # The strength is 'strong' or 'weak'; get this information from job.json
    bench_path = glob.glob(os.path.join(save_path, '*_bench/work'))
    bench_path.sort()
    job_info = load(os.path.join(bench_path[0], 'job.json'))
    strength = job_info['scaling_type']

    # Set ylims for the real-time factor of state propagation plot
    if strength == "strong":
        rtf_ylims = (-0.1, 2.6)
    else:
        if "Sparse" in labels or "Bernoulli" in labels:
            rtf_ylims = (-0.1, 3.6)
        else:
            rtf_ylims = (-0.1, 6.1)

    # Plot major data: network creation time, network connection time, state propagation time
    plot_major(
        timer_files,
        labels,
        save_path,
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
            save_path,
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
         save_path,
         strength,
         ['time_update_factor', 'spike_ccd_factor', 'secondary_gd_factor', 'others_factor'],
         colors=['#004488','#994455','#997700','#6699cc'],
         file_postfix='rtf',
         ylabel_prefix='RTF of ',
        )

if __name__ == '__main__':
    plot()
