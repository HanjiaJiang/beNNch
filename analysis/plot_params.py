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

light = tol_colors.tol_cset('light')

color_params = {
    'time_simulate': light.pink,
    'time_update': light.pink,
    'time_update_factor': light.pink,
    'time_update_frac': light.pink,
    'spike_ccd_factor': light.light_yellow,
    'spike_ccd_frac': light.light_yellow,
    'time_collocate_spike_data': light.orange,
    'time_collocate_spike_data_factor': light.orange,
    'time_collocate_spike_data_frac': light.orange,
    'time_communicate_spike_data': light.light_yellow,
    'time_communicate_spike_data_factor': light.light_yellow,
    'time_communicate_spike_data_frac': light.light_yellow,
    'time_deliver_spike_data': light.pale_grey,
    'time_deliver_spike_data_factor': light.pale_grey,
    'time_deliver_spike_data_frac': light.pale_grey,
    'secondary_gd_factor': light.mint,
    'secondary_gd_frac': light.mint,
    'time_gather_secondary_data': light.mint,
    'time_gather_secondary_data_factor': light.mint,
    'time_gather_secondary_data_frac': light.mint,
    'time_deliver_secondary_data': light.light_blue,
    'time_deliver_secondary_data_factor': light.light_blue,
    'time_deliver_secondary_data_frac': light.light_blue,
    'others_factor': light.light_cyan,
    'others_frac': light.light_cyan,
}

label_params = {
    'threads_per_node': 'Number of threads\nper node',
    'tasks_per_node': 'Number of\nMPI processes\nper node',
    'num_nodes': 'Number of Nodes',
    'time_construct': 'Network construction',
    'time_simulate': 'State propagation',
    'time_update': 'Update',
    'time_update_factor': 'Update',
    'time_update_frac': 'Update',
    'spike_ccd_factor': 'Spike CCD',
    'spike_ccd_frac': 'Spike CCD',
    'time_collocate_spike_data': 'Spike\nCollocation',
    'time_collocate_spike_data_factor': 'Spike\nCollocation',
    'time_collocate_spike_data_frac': 'Spike\nCollocation',
    'time_communicate_spike_data': 'Spike\nCommunication',
    'time_communicate_spike_data_factor': 'Spike\nCommunication',
    'time_communicate_spike_data_frac': 'Spike\nCommunication',
    'time_deliver_spike_data': 'Spike\nDelivery',
    'time_deliver_spike_data_factor': 'Spike\nDelivery',
    'time_deliver_spike_data_frac': 'Spike\nDelivery',
    'secondary_gd_factor': 'SIC GD',
    'secondary_gd_frac': 'SIC GD',
    'time_gather_secondary_data': 'SIC\nGathering',
    'time_gather_secondary_data_factor': 'SIC\nGathering',
    'time_gather_secondary_data_frac': 'SIC\nGathering',
    'time_deliver_secondary_data': 'SIC\nDelivery',
    'time_deliver_secondary_data_factor': 'SIC\nDelivery',
    'time_deliver_secondary_data_frac': 'SIC\nDelivery',
    'others_factor': 'Other',
    'others_frac': 'Other',
}
