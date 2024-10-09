"""
beNNch-plot - standardized plotting routines for performance benchmarks.
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

"""
Default parameters for plotting
"""
import tol_colors

size_factor = 1.3
matplotlib_params = {
    'text.latex.preamble': ['\\usepackage{gensymb}'],
    'image.origin': 'lower',
    'image.interpolation': 'nearest',
    'axes.grid': False,
    'axes.labelsize': 15 * size_factor,
    'axes.titlesize': 19 * size_factor,
    'font.size': 16 * size_factor,
    'legend.fontsize': 11 * size_factor,
    'xtick.labelsize': 11 * size_factor,
    'ytick.labelsize': 11 * size_factor,
    'text.usetex': False,
}

additional_params = {
    'figsize_single': [6.1 * 1.5, 6.1],
    'figsize_double': [12.2, 6.1 * 1.1]
}

bright = tol_colors.tol_cset('bright')
vibrant = tol_colors.tol_cset('vibrant')
light = tol_colors.tol_cset('light')

color_params = {
    'wall_time_total': light.pale_grey,
    'sim_factor': light.pink,
    'phase_total_factor': light.orange,
    'time_simulate': light.pink,
    'time_construct': light.light_cyan,
    'time_update': light.orange,
    'time_communicate_spike_data': light.light_blue,
    'time_deliver_spike_data': light.mint,
    'time_collocate_spike_data': light.light_yellow,
    'time_update_frac': light.pink,
    'time_deliver_spike_data_frac': light.pale_grey,
    'time_communicate_spike_data_frac': light.light_yellow,
    'time_collocate_spike_data_frac': light.orange,
    'secondary_gd_frac': light.mint,
    'time_deliver_secondary_data_frac': light.light_blue,
    'time_gather_secondary_data_frac': light.mint,
    'spike_ccd_frac': light.light_yellow,
    'others_frac': light.light_cyan,
    'time_update_factor': light.pink,
    'time_deliver_spike_data_factor': light.pale_grey,
    'time_communicate_spike_data_factor': light.light_yellow,
    'time_collocate_spike_data_factor': light.orange,
    'secondary_gd_factor': light.mint,
    'spike_ccd_factor': light.light_yellow,
    'others_factor': light.light_cyan,
    'time_deliver_secondary_data_factor': light.light_blue,
    'time_gather_secondary_data_factor': light.mint,
    'total_memory': light.olive,
    'total_memory_per_node': light.pear,
    'time_construction_connect_third_inner_count': light.pink,
    'time_construction_connect_third_inner_max': light.orange,
    'time_construction_connect_third_inner_fill': light.light_yellow,
    'time_construction_connect_third_inner_communicate': light.mint,
    'time_construction_connect_third_inner_connect': light.light_blue,
}

label_params = {
    'threads_per_node': 'OMP threads',
    'tasks_per_node': 'MPI processes',
    'num_nodes': 'Nodes',
    'wall_time_total': 'Total',
    'time_communicate_prepare': 'Preparation',
    'wall_time_presim': 'Presimulation',
    'time_construction_create': 'Creation',
    'time_construction_connect': 'Connection',
    'time_simulate': 'State propagation',
    'wall_time_phase_total': 'All phases',
    'time_update': 'Update',
    'time_collocate_spike_data': 'Spike\nCollocation',
    'time_communicate_spike_data': 'Spike\nCommunication',
    'time_deliver_spike_data': 'Spike\nDelivery',
    'time_construct': 'Network construction',
    'max_memory': 'Memory',
    'sim_factor': 'State propagation',
    'time_update_frac': 'Update',
    'time_communicate_spike_data_frac': 'Spike\nCommunication',
    'time_deliver_spike_data_frac': 'Spike\nDelivery',
    'time_collocate_spike_data_frac': 'Spike\nCollocation',
    'secondary_gd_frac': 'SIC GD',
    'time_deliver_secondary_data_frac': 'Spike\nDelivery',
    'time_gather_secondary_data_frac': 'SIC\nGathering',
    'time_update_factor': 'Update',
    'time_communicate_spike_data_factor': 'Spike\nCommunication',
    'time_deliver_spike_data_factor': 'Spike\nDelivery',
    'time_collocate_spike_data_factor': 'Spike\nCollocation',
    'secondary_gd_factor': 'SIC GD',
    'time_deliver_secondary_data_factor': 'SIC\nDelivery',
    'time_gather_secondary_data_factor': 'SIC\nGathering',
    'phase_total_factor': 'All phases',
    'total_memory': 'Memory',
    'total_memory_per_node': 'Memory per node',
    'total_spike_count_per_s': 'Total spikes/s',
    'spike_ccd_factor': 'Spike CCD',
    'spike_ccd_frac': 'Spike CCD',
    'others_factor': 'Other',
    'others_frac': 'Other',
    'time_construction_connect_third_inner_count': 'Third inner count',
    'time_construction_connect_third_inner_max': 'Third inner max',
    'time_construction_connect_third_inner_fill': 'Third inner fill',
    'time_construction_connect_third_inner_communicate': 'Third inner communicate',
    'time_construction_connect_third_inner_connect': 'Third inner connect',
}
