import os
import sys
import json
import glob
import yaml

from plot_major import plot_major
from plot_phases import plot_phases

import matplotlib.pyplot as plt
plt.rcParams.update({'font.size': 15})

def plot(jube_ids, labels):
    # Load analysis configurations
    config_file_name = '../config/analysis_config.yaml'
    assert os.path.isfile(config_file_name), 'Configuration file not found!'
    with open(config_file_name) as analysis_config_file:
        config = yaml.load(analysis_config_file, Loader=yaml.FullLoader)

    # Get benchmark data paths
    data_paths, timer_files = [], []
    for jube_id in jube_ids:
        path_i = os.path.join(config['jube_outpath'], jube_id.zfill(6))
        data_paths.append(path_i)
        timer_files.append(os.path.join(path_i, "timer_file.csv"))

    # Benchmark strength is 'strong' or 'weak'; get this information from job.json
    bench_path = glob.glob(os.path.join(data_paths[0], '*_bench/work'))
    bench_path.sort()
    with open(os.path.join(bench_path[0], 'job.json'), 'r') as f:
        job_info = json.load(f)
    strength = job_info['scaling_type']

    # Set save path
    save_path = 'results_' + '_'.join([x.replace(' ','').replace('-','').replace('_','') for x in labels]) + '_' + strength
    os.system(f'mkdir -p {save_path}')

    # Set ylims for the real-time factor of state propagation plot
    if strength == "strong":
        ylims_rtf = (-0.1, 2.6)
    else:
        if "Sparse" in labels or "Bernoulli" in labels:
            ylims_rtf = (-0.1, 3.6)
        else:
            ylims_rtf = (-0.1, 6.1)

    # Plot major timer data
    print('Plotting major timer data ...')
    plot_major(
        timer_files,
        labels,
        save_path,
        strength,
    )

    # Plot four phases in state propagation
    print('Plotting phase data ...')
    for (detail, fontsize) in [(False, 'small'), (True, 'x-small')]:
        plot_phases(
            timer_files,
            labels,
            save_path,
            strength,
            ylims_rtf=ylims_rtf,
            detail=detail,
            legend_fontsize=fontsize,
        )

if __name__ == '__main__':
    # Input 1 to 4: JUBE benchmark IDs
    # Input 5 to 8: labels (model names)
    plot(sys.argv[1:5], sys.argv[5:9])
