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

import numpy as np
import bennchplot as bp
from matplotlib import pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.transforms as mtransforms


def plot(scaling_type, timer_hash, timer_file, save_path, scaling_strength, timer_file_ctrl):

    if scaling_type == 'nodes':
        args = {
            'data_file': timer_file,
            'x_axis': ['num_nodes'],
            'time_scaling': 1e3,
            'ctrl_file': timer_file_ctrl,
        }

        # Instantiate class
        B = bp.Plot(**args)

        # Plotting
        widths = [1, 1]
        heights = [3, 1]
        fig = plt.figure(figsize=(12, 6), constrained_layout=True)
        spec = gridspec.GridSpec(ncols=2, nrows=2, figure=fig,
                                 width_ratios=widths,
                                 height_ratios=heights)

        ax1 = fig.add_subplot(spec[0, 0])
        ax_spk = fig.add_subplot(spec[1, 0]) # total spike/s
        ax2 = fig.add_subplot(spec[0, 1])
        ax3 = fig.add_subplot(spec[1, 1])

        if scaling_strength == 'weak':
            xlabel = 'Number of compute nodes; Scale of model'
            ax1_twin = ax1.twiny() # top axis for network_size
            ax2_twin = ax2.twiny() # top axis for network_size
        else:
            xlabel = 'Number of compute nodes'

#        trans = mtransforms.ScaledTranslation(-20 /
#                                              72, 7 / 72, fig.dpi_scale_trans)
#        ax1.text(0.0, 1.0, 'A', transform=ax1.transAxes + trans,
#                 fontsize='medium', va='bottom', fontweight='bold')
#        ax_spk.text(0.0, 1.0, 'B', transform=ax2.transAxes + trans,
#                 fontsize='medium', va='bottom', fontweight='bold')
#        ax2.text(0.0, 1.0, 'C', transform=ax2.transAxes + trans,
#                 fontsize='medium', va='bottom', fontweight='bold')
#        ax3.text(0.0, 1.0, 'D', transform=ax3.transAxes + trans,
#                 fontsize='medium', va='bottom', fontweight='bold')

        # Network construction + State propagation
        B.plot_fractions(axis=ax1,
                         fill_variables=[
                             'wall_time_create+wall_time_connect',
                             'wall_time_sim', ],
                         interpolate=True,
                         step=None,
                         error=True,
                         control=True)
        B.plot_fractions(axis=ax1,
                         fill_variables=[
                             'wall_time_create+wall_time_connect',
                             'wall_time_sim', ],
                         interpolate=True,
                         step=None,
                         error=True,
                         line=True,
                         label_tail=' (astrocyte)')

        # Total spike count
        B.plot_main(quantities=['total_spike_count_per_s'], axis=ax_spk, error=True, control=True, line_color='gray')
        B.plot_main(quantities=['total_spike_count_per_s'], axis=ax_spk, error=True, line_color='k')

        # State propagation
        B.plot_main(quantities=['sim_factor'], axis=ax2, error=True, control=True, label='State propagation (control)', line_color='gray')
        B.plot_main(quantities=['sim_factor'], axis=ax2, error=True, label='State propagation (astrocyte)', line_color='k')
        B.plot_fractions(axis=ax2,
                         fill_variables=[
                             'phase_update_factor',
                             'phase_collocate_factor',
                             'phase_communicate_factor',
                             'phase_deliver_factor'
                         ],
                         label_tail=' (astrocyte)')
        B.plot_fractions(axis=ax3,
                         fill_variables=[
                             'frac_phase_update',
                             'frac_phase_collocate',
                             'frac_phase_communicate',
                             'frac_phase_deliver'
                         ])

        ax1.set_ylabel(r'$T_{\mathrm{wall}}$ [s] for $T_{\mathrm{model}} =$'
                       + f'{np.unique(B.df_data.model_time_sim.values)[0]} s')
        ax_spk.set_xlabel(xlabel)
        ax_spk.set_ylabel('Total spikes/s')
        ax2.set_ylabel(r'real-time factor $T_{\mathrm{wall}}/$'
                       r'$T_{\mathrm{model}}$')
        ax3.set_xlabel(xlabel)
        ax3.set_ylabel(r'relative $T_{\mathrm{wall}}$ [%]')

        ax1.legend()
        ax2.legend()
        handles1, labels1 = ax1.get_legend_handles_labels()
        handles2, labels2 = ax2.get_legend_handles_labels()

        ax1.legend(handles1[::-1], labels1[::-1])
        ax2.legend(handles2[::-1], labels2[::-1], loc='upper right')

        ax_spk.set_ylim(bottom=0)
        ax3.set_ylim(0, 100)

        N_size_labels = B.df_data['network_size'].values.astype(int) - 1 # minus 1 poisson generator
        if scaling_strength == 'weak':
            ax1_twin.set_xticks(ax1.get_xticks())
            ax1_twin.set_xticklabels(N_size_labels)
            ax1_twin.set_xlabel('Network size (number of cells)')
            ax1_twin.set_xlim(ax1.get_xlim())
            ax2_twin.set_xticks(ax2.get_xticks())
            ax2_twin.set_xticklabels(N_size_labels)
            ax2_twin.set_xlabel('Network size (number of cells)')
            ax2_twin.set_xlim(ax2.get_xlim())

        ax1.set_xticklabels([])
        ax2.set_xticklabels([])
        ax_spk.set_xticks(ax1.get_xticks())

#        for ax in [ax1, ax2, ax3]:
#            ax.margins(x=0)
#        for ax in [ax1, ax2, ax_spk]:
#            B.simple_axis(ax)

        plt.savefig(f'{save_path}/{timer_hash}.png', dpi=400)

    elif scaling_type == 'threads':

        args = {
            'data_file': timer_file,
            'x_axis': ['num_nvp'],
            'time_scaling': 1e3
        }

        # Instantiate class
        B = bp.Plot(**args)

        # Plotting
        widths = [1]
        heights = [3, 1]
        fig = plt.figure(figsize=(6, 6), constrained_layout=True)
        spec = gridspec.GridSpec(ncols=1, nrows=2, figure=fig,
                                 width_ratios=widths,
                                 height_ratios=heights)

        ax1 = fig.add_subplot(spec[0, :])
        ax2 = fig.add_subplot(spec[1, :])

        B.plot_main(quantities=['sim_factor'], axis=ax1, log=(False, True))
        B.plot_fractions(axis=ax2,
                         fill_variables=[
                             'frac_phase_update',
                             'frac_phase_collocate',
                             'frac_phase_communicate',
                             'frac_phase_deliver'
                         ],
                         )

        ax1.set_ylabel(r'real-time factor $T_{\mathrm{wall}}/$'
                       r'$T_{\mathrm{model}}$')
        ax1.set_xlabel('number of vps')
        ax2.set_ylabel(r'$T_{\mathrm{wall}}$ [%]')
        B.merge_legends(ax1, ax2)

        plt.savefig(f'{save_path}/{timer_hash}.png', dpi=600)
