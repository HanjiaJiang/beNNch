# This script generate the single timer file for plotting and needs JUBE
import os
import sys
import yaml

from analysis_helper import shell, load

# Load analysis configurations
config_file_name = '../config/analysis_config.yaml'
with open(config_file_name) as analysis_config_file:
    config = yaml.load(analysis_config_file, Loader=yaml.FullLoader)

# Load data
data_paths, timer_files = [], []
for i in range(1, len(sys.argv)):
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


