"""
beNNch - Unified execution, collection, analysis and
comparison of neural network simulation benchmarks.
Copyright (C) 2021 Forschungszentrum Juelich GmbH, INM-6

This program is free software: you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation, either version 3 of the License, or (at your option) any later
version.
This program is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
PARTICULAR PURPOSE. See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with
this program. If not, see <https://www.gnu.org/licenses/>.

SPDX-License-Identifier: GPL-3.0-or-later
"""

import os
import sys
import glob
import yaml

from analysis_helper import shell, shell_return, load, git_annex
from plot_astro import plot

# Load analysis configurations
with open('../config/analysis_config.yaml') as analysis_config_file:
    config = yaml.load(analysis_config_file, Loader=yaml.FullLoader)

# Astrocyte data
jube_id = str(sys.argv[1])
base_path = os.path.join(config['jube_outpath'], jube_id.zfill(6))
uuidgen_hash = shell_return('uuidgen')
timer_file=os.path.join(base_path, uuidgen_hash + ".csv")
# analyse and save plot raw data to .csv
shell(
    f"module load JUBE; jube analyse {config['jube_outpath']} --id {jube_id};"
    + f" jube result {config['jube_outpath']} --id {jube_id} > "
    + timer_file)

# Control data
jube_id_ctrl = str(sys.argv[2])
ctrl_path = os.path.join(config['jube_outpath'], jube_id_ctrl.zfill(6))
uuidgen_hash_ctrl = shell_return('uuidgen')
timer_file_ctrl=os.path.join(ctrl_path, uuidgen_hash_ctrl + ".csv")
shell(
    f"module load JUBE; jube analyse {config['jube_outpath']} --id {jube_id_ctrl};"
    + f" jube result {config['jube_outpath']} --id {jube_id_ctrl} > "
    + timer_file_ctrl)

# X axis: "nodes" or "nvp"
# This is for the x-axis labeling: "Number of nodes" or "Number of virtual processes"
# Use "nvp" for "Number of virtual processes" (nvp strong scaling case)
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
    strength = str(sys.argv[4])
except:
    strength = job_info['scaling_type']

# Commit results with git annex; not using now
"""
git_annex(cpu_info=cpu_info,
          job_info=job_info,
          uuidgen_hash=uuidgen_hash,
          base_path=base_path)
"""

plabel = 'A' if int(jube_id) < 2 else 'B'

if x_axis_label == "num_nvp":
    cons_ylims = (1.9, 4.1)
    prop_ylims = (-1.0, 101.0)
    spk_ylims = (-1000.0, 101000.0)
    rt_ylims = (-0.5, 10.5)
elif strength == "strong":
    cons_ylims = (1.9, 4.1)
    prop_ylims = (-1.0, 36.0)
    spk_ylims = (-1000.0, 101000.0)
    rt_ylims = (-0.2, 3.7)
else:
    cons_ylims = (-1.0, 101.0)
    prop_ylims = (-1.0, 101.0)
    spk_ylims = (-10000.0, 510000.0)
    rt_ylims = (-0.5, 12.5)

plot(
    timer_hash=uuidgen_hash,
    timer_file=timer_file,
    save_path=base_path,
    scaling_strength=strength,
    timer_file_ctrl=timer_file_ctrl,
    x_axis=x_axis_label,
    plabel=plabel,
    cons_ylims = cons_ylims,
    prop_ylims = prop_ylims,
    spk_ylims = spk_ylims,
    rt_ylims = rt_ylims
)
