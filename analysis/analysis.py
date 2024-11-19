# This script generate the single timer file for plotting and needs JUBE
import os
import sys
import yaml

import pandas as pd

from analysis_helper import shell, load

def analyse(jube_ids, config_file_name):
    # load analysis configurations
    with open(config_file_name) as analysis_config_file:
        config = yaml.load(analysis_config_file, Loader=yaml.FullLoader)
    data_paths, df_all = [], None
    # iterate through benchmarks
    for i in range(len(jube_ids)):
        jube_id_i = str(jube_ids[i])
        path_i = os.path.join(config['jube_outpath'], jube_id_i.zfill(6))
        data_paths.append(path_i)
        timer_file_i = os.path.join(path_i, "timer_file.csv")
        # analyse and collect data to .csv
        if not os.path.isfile(timer_file_i):
            print(f"reload {timer_file_i} ...")
            shell(
                f"module load JUBE; jube analyse {config['jube_outpath']} --id {jube_id_i};"
                + f" jube result {config['jube_outpath']} --id {jube_id_i} > "
                + timer_file_i)

if __name__ == "__main__":
    # JUBE benchmark IDs
    jube_ids = sys.argv[1:]
    analyse(jube_ids, '../config/analysis_config.yaml')
