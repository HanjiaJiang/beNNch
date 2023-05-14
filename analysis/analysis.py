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
from plot_helper import plot

with open('../config/analysis_config.yaml') as analysis_config_file:
    config = yaml.load(analysis_config_file, Loader=yaml.FullLoader)

# Astrocyte
jube_id = str(sys.argv[1])
base_path = os.path.join(config['jube_outpath'], jube_id.zfill(6))
uuidgen_hash = shell_return('uuidgen')
shell(
    f"module load JUBE; jube analyse {config['jube_outpath']} --id {jube_id};"
    + f" jube result {config['jube_outpath']} --id {jube_id} > "
    + os.path.join(base_path, uuidgen_hash + ".csv"))

# Control
jube_id_ctrl = str(sys.argv[2])
ctrl_path = os.path.join(config['jube_outpath'], jube_id_ctrl.zfill(6))
uuidgen_hash_ctrl = shell_return('uuidgen')
shell(
    f"module load JUBE; jube analyse {config['jube_outpath']} --id {jube_id_ctrl};"
    + f" jube result {config['jube_outpath']} --id {jube_id_ctrl} > "
    + os.path.join(ctrl_path, uuidgen_hash_ctrl + ".csv"))

# Strong or weak scaling
strength = str(sys.argv[3])

# take the job and cpu info from first bench job, assuming all nodes are equal
bench_path = glob.glob(os.path.join(base_path, '*_bench/work'))
bench_path.sort()

cpu_info = load(os.path.join(bench_path[0], 'cpu.json'))
job_info = load(os.path.join(bench_path[0], 'job.json'))

"""
git_annex(cpu_info=cpu_info,
          job_info=job_info,
          uuidgen_hash=uuidgen_hash,
          base_path=base_path)
"""

timer_file=os.path.join(
        config['jube_outpath'], jube_id.zfill(6), uuidgen_hash + ".csv")

timer_file_ctrl=os.path.join(
        config['jube_outpath'], jube_id_ctrl.zfill(6), uuidgen_hash_ctrl + ".csv")

plot(
    scaling_type=config['scaling_type'],
    timer_hash=uuidgen_hash,
    timer_file=timer_file,
    save_path=os.path.join(config['jube_outpath'], jube_id.zfill(6)),
    scaling_strength=strength,
    timer_file_ctrl=timer_file_ctrl,
)
