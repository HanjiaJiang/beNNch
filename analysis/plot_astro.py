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
plt.rcParams.update({'font.size': 14})

def plot(timer_hash,
         timer_file,
         save_path,
         scaling_strength,
         timer_file_ctrl,
         x_axis='num_nodes',
         plabel='',
         cons_ylims=(-1.0, 101.0),
         prop_ylims=(-1.0, 101.0),
         spk_ylims=(-10000.0, 2010000.0),
         rt_ylims=(-0.5, 12.5)):

    if True:
        if x_axis != 'num_nodes' and x_axis != 'num_nvp':
            x_axis = 'num_nodes'
        print(f'x axis: {x_axis}')
        args = {
            'data_file': timer_file,
            'x_axis': [x_axis],
            'time_scaling': 1e3,
            'ctrl_file': timer_file_ctrl,
        }

        # Instantiate class
        B = bp.Plot(**args)

        # Plotting
        widths = [1, 1]
        heights = [2, 2, 1]
        fig = plt.figure(figsize=(12, 6))
        spec = gridspec.GridSpec(ncols=2, nrows=3, figure=fig,
                                 width_ratios=widths,
                                 height_ratios=heights)

        ax_cons = fig.add_subplot(spec[0, 0])
        ax_prop = fig.add_subplot(spec[1, 0])
        ax_spk = fig.add_subplot(spec[2, 0]) # total spike/s
        ax_rt = fig.add_subplot(spec[0:2, 1])
        ax_rt_rel = fig.add_subplot(spec[2, 1])

        if scaling_strength == 'weak':
            ax_cons_twin = ax_cons.twiny() # top axis for network_size
            ax_rt_twin = ax_rt.twiny() # top axis for network_size

        if x_axis == 'num_nvp':
            xlabel = 'Number of threads per MPI task'
        else:
            xlabel = 'Number of compute nodes'

        trans = mtransforms.ScaledTranslation(-20 / 72, 7 / 72, fig.dpi_scale_trans)

        print('plotting timer data ...')

        # Network construction
#        print(B.df_data['wall_time_create+wall_time_connect'].values)
#        print(B.df_data['wall_time_create+wall_time_connect_std'].values)
#        print(B.df_data['wall_time_create_std'].values)
#        print(B.df_data['wall_time_connect_std'].values)
        B.plot_main(quantities=['wall_time_create+wall_time_connect'],
                    axis=ax_cons,
                    subject='astrocyte_lr_1994',
                    line_color='k')
        B.plot_main(quantities=['wall_time_create+wall_time_connect'],
                   axis=ax_cons,
                   control=True,
                   subject='astrocyte_surrogate',
                   line_color='gray')

        # State propagation
        B.plot_main(quantities=['wall_time_sim'],
                    axis=ax_prop,
                    subject='astrocyte_lr_1994',
                    line_color='k')
        B.plot_main(quantities=['wall_time_sim'],
                   axis=ax_prop,
                   control=True,
                   subject='astrocyte_surrogate',
                   line_color='gray')

        # Total spike count
        B.plot_main(quantities=['total_spike_count_per_s'],
                    axis=ax_spk,
                    subject='astrocyte_lr_1994',
                    line_color='k')
        B.plot_main(quantities=['total_spike_count_per_s'],
                    axis=ax_spk,
                    control=True,
                    subject='astrocyte_surrogate',
                    line_color='gray')


        print("plotting RTF ...")

        # RTF for state propagation
        B.plot_main(quantities=['sim_factor'],
                    axis=ax_rt,
                    control=True,
                    subject='State propagation (astrocyte_surrogate)',
                    line_color='gray')
        B.plot_main(quantities=['sim_factor'],
                    axis=ax_rt,
                    subject='State propagation (astrocyte_lr_1994)',
                    line_color='k')
        B.plot_fractions(axis=ax_rt,
                         fill_variables=[
                             'phase_update_factor',
                             'phase_ccd_factor',
                             'phase_others_factor',
                         ],
                         subject='astrocyte_lr_1994')
        B.plot_fractions(axis=ax_rt_rel,
                         fill_variables=[
                             'frac_phase_update',
                             'frac_phase_ccd',
                             'frac_phase_others',
                         ],
                         subject='astrocyte_lr_1994'
                         )

        ax_cons.set_ylabel('Network\nconstruction\ntime (s)')
        ax_prop.set_ylabel('State propagation\ntime (s) for\n'
                       r'$T_{\mathrm{model}} =$'
                       + f'{np.unique(B.df_data.model_time_sim.values)[0]} s')
        ax_spk.set_xlabel(xlabel)
        ax_spk.set_ylabel('Network total\nspikes/s')
        ax_rt.set_ylabel('Real-time factor')
        ax_rt_rel.set_xlabel(xlabel)
        ax_rt_rel.set_ylabel('relative\nreal-time\nfactor (%)')

        ax_cons.legend(fontsize='x-small', frameon=False)
        ax_rt.legend()
        # to reverse the order
        handles1, labels1 = ax_cons.get_legend_handles_labels()
        handles2, labels2 = ax_rt.get_legend_handles_labels()
#        ax_cons.legend(handles1[::-1], labels1[::-1], fontsize='x-small', frameon=False)
        ax_rt.legend(handles2[::-1], labels2[::-1], fontsize='x-small', frameon=False)

        ax_cons.set_ylim(cons_ylims)
        ax_prop.set_ylim(prop_ylims)
        ax_spk.set_ylim(spk_ylims)
        ax_rt.set_ylim(rt_ylims)
        ax_rt_rel.set_ylim(-5.0, 105.0)

        if x_axis == 'num_nvp':
            xticks = ax_cons.get_xticks().flatten()
            xticklabels = (xticks/8).astype(int)

            ax_cons.set_xticks(xticks)
            ax_cons.set_xticklabels(xticklabels)

            ax_prop.set_xticks(xticks)
            ax_prop.set_xticklabels(xticklabels)

            ax_spk.set_xticks(xticks)
            ax_spk.set_xticklabels(xticklabels)

            ax_rt.set_xticks(xticks)
            ax_rt.set_xticklabels(xticklabels)

            ax_rt_rel.set_xticks(xticks)
            ax_rt_rel.set_xticklabels(xticklabels)

        N_size_labels = B.df_data['network_size'].values.astype(int) - 1 # minus 1 poisson generator
        if scaling_strength == 'weak':
            ax_cons_twin.set_xticks(ax_cons.get_xticks().flatten())
            ax_cons_twin.set_xticklabels(N_size_labels.tolist())
            ax_cons_twin.set_xlabel('Network size (number of cells)')
            ax_cons_twin.set_xlim(ax_cons.get_xlim())
            ax_rt_twin.set_xticks(ax_rt.get_xticks())
            ax_rt_twin.set_xticklabels(N_size_labels)
            ax_rt_twin.set_xlabel('Network size (number of cells)')
            ax_rt_twin.set_xlim(ax_rt.get_xlim())

        fig.text(0.0, 1.0, plabel, ha='left', va='top', fontsize='x-large', fontweight='bold')

        plt.tight_layout()
        plt.savefig(f'{save_path}/{timer_hash}.png', dpi=400)

        df_data_mean = B.df_data.groupby(["num_nodes", "threads_per_task"]).mean().reset_index()
        df_ctrl_mean = B.df_ctrl.groupby(["num_nodes", "threads_per_task"]).mean().reset_index()

        df_rel_diff = (df_data_mean - df_ctrl_mean)/df_ctrl_mean
#        df_out = df_rel_diff[['num_nodes', 'threads_per_task', 'wall_time_sim']]
        df_rel_diff.to_csv(f"{save_path}/df_rel_diff.csv", index=False, float_format="%.3f")
