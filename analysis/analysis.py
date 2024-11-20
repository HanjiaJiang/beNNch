import os
import sys
import yaml

from analysis_helper import shell, load

def analyse(jube_ids, config_file_name):
    # Load analysis configurations
    with open(config_file_name) as analysis_config_file:
        config = yaml.load(analysis_config_file, Loader=yaml.FullLoader)
    # Iterate through benchmark paths by ID
    for i, jube_id_i in enumerate(jube_ids):
        path_i = os.path.join(config['jube_outpath'], jube_id_i.zfill(6))
        timer_file_i = os.path.join(path_i, "timer_file.csv")
        # Analyse and collect data to .csv
        if not os.path.isfile(timer_file_i):
            print(f"Loading {timer_file_i} ...")
            shell(
                f"module load JUBE; jube analyse {config['jube_outpath']} --id {jube_id_i};"
                + f" jube result {config['jube_outpath']} --id {jube_id_i} > "
                + timer_file_i)

if __name__ == "__main__":
    # Input is JUBE benchmark IDs
    analyse(sys.argv[1:], '../config/analysis_config.yaml')
