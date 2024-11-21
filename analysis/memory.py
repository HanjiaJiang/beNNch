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

def pivot_df(df, columns, index, values):
    df_mean = df.groupby([columns, index]).mean().reset_index()
    df_std = df.groupby([columns, index]).std().reset_index()
    df_mean_table = df_mean.pivot(columns=columns, index=index, values=values)
    df_std_table = df_std.pivot(columns=columns, index=index, values=values)
    df_mean_table.to_csv(f'{values}_mean.csv')
    df_std_table.to_csv(f'{values}_std.csv')


# concatenate and save results
def concat_df(file_list, output_file, labels_list, compare_memory=False):
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
    if compare_memory and 'network_memory' in df_all:
        df_all['memory_network_minus_base'] = df_all['network_memory'] - df_all['base_memory']
        df_all['memory_init_minus_network'] = df_all['init_memory'] - df_all['network_memory']
        df_all['memory_total_minus_init'] = df_all['total_memory'] - df_all['init_memory']
        pivot_df(df_all, 'num_nodes', 'model', 'memory_network_minus_base')
        pivot_df(df_all, 'num_nodes', 'model', 'memory_init_minus_network')
        pivot_df(df_all, 'num_nodes', 'model', 'memory_total_minus_init')

output_csv = os.path.join(data_paths[0], "df_all.csv")
concat_df(timer_files, output_csv, labels)
