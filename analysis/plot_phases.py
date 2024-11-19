import os

import numpy as np
import bennchplot as bp
from matplotlib import pyplot as plt
import matplotlib.gridspec as gridspec

def plot_phases(
         timer_files,
         labels,
         save_path,
         scaling_strength,
         x_axis='num_nodes',
         rtf_ylims=(-0.1, 5.1),
         detail=False,
         reverse_phases=False,
         ignore_others=False,
         legend_fontsize='small',
         plot_relative=False,
         ):

    # Set x axis type and label
    x_axis = x_axis if x_axis == 'num_nvp' else 'num_nodes'
    if x_axis == 'num_nvp':
        xlabel = 'Number of VPs'
    else:
        xlabel = 'Number of\ncompute nodes'

    # Create figure according to valid file count
    fcount = sum(1 for timer_file in timer_files if os.path.isfile(timer_file))
    widths = [1]*fcount
    heights = [4, 1] if plot_relative else [1]
    figsize = (2+1.5*fcount, 4)
    fig = plt.figure(figsize=figsize)
    nrows = 2 if plot_relative else 1
    spec = gridspec.GridSpec(ncols=fcount, nrows=nrows, figure=fig,
                             width_ratios=widths,
                             height_ratios=heights)

    # Set phase labels
    # if detail = True, include detailed phases
    if detail:
        phases = [
            'time_update_factor',
            'time_collocate_spike_data_factor',
            'time_communicate_spike_data_factor',
            'time_deliver_spike_data_factor',
            'time_gather_secondary_data_factor',
            'time_deliver_secondary_data_factor',
            'others_factor',
        ]
        fractions=[
            'time_update_frac',
            'time_collocate_spike_data_frac',
            'time_communicate_spike_data_frac',
            'time_deliver_spike_data_frac',
            'time_gather_secondary_data_frac',
            'time_deliver_secondary_data_frac',
            'others_frac',
        ]
    else:
        phases = [
            'time_update_factor',
            'spike_ccd_factor',
            'secondary_gd_factor',
            'others_factor',
        ]
        fractions = [
            'time_update_frac',
            'spike_ccd_frac',
            'secondary_gd_frac',
            'others_frac',
        ]

    # Reverse phase order if specified
    if reverse_phases:
        phases.reverse()
        fractions.reverse()

    # Skip the 'other' phase if specified
    if ignore_others:
        phases.remove('others_factor')
        fractions.remove('others_frac')

    # Iterate through files to create corresponding plots
    for i, timer_file in enumerate(timer_files):
        if not os.path.isfile(timer_file):
            break
        args = {
            'data_file': timer_file,
            'x_axis': [x_axis],
            'time_scaling': 1e3,
        }

        # Create plot object
        B = bp.Plot(**args)

        # Create axis object
        ax_rtf = fig.add_subplot(spec[0, i])
        if i == 0:
            ax_rtf.set_ylabel('Real-time factor')

        # Create relative real-time factor plot if specified
        if plot_relative:
            ax_frac = fig.add_subplot(spec[1, i])
            ax_frac.set_xlabel(xlabel)
            ax_frac.set_ylim(-10.0, 110.0)
            B.plot_fractions(axis=ax_frac, fill_variables=fractions)
            if i == 0:
                ax_frac.set_ylabel('Relative\nreal-time\nfactor (%)')
        else:
            ax_rtf.set_xlabel(xlabel)

        # panel title
        label_i = labels[i].replace(" ", "\n", 1).replace("=", "=\n", 1)
        ax_rtf.set_title(label_i, pad=20, fontsize='medium')

        # Plot phases of state propagation in terms of real-time factor
        B.plot_fractions(axis=ax_rtf, fill_variables=phases)
        ax_rtf.set_ylim(rtf_ylims)

        # if weak scaling, create twin axes for network size
        if scaling_strength == 'weak':
            df_tmp = B.df_data
            assert 'N_ex' in df_tmp and 'N_in' in df_tmp, 'plot_phases(): N_ex or N_in not in data!'
            N_sizes = (df_tmp['N_ex'].values + df_tmp['N_in'].values + df_tmp['N_astro'].values).astype(int)
            xticklabels = [np.format_float_scientific(x, trim='-', exp_digits=1).replace("+", "") for x in N_sizes]
            ax_rtf_twin = ax_rtf.twiny()
            ax_rtf_twin.set_xticks(ax_rtf.get_xticks().flatten())
            ax_rtf_twin.set_xticklabels(xticklabels, fontsize='small')
            ax_rtf_twin.set_xlabel('Network size', fontsize='small')
            ax_rtf_twin.set_xlim(ax_rtf.get_xlim())

    plt.tight_layout()
    pname = "plot_phases_detail" if detail else "plot_phases"
    plt.savefig(f'{save_path}/{pname}.png', dpi=400)
    plt.savefig(f'{save_path}/{pname}.eps', format='eps', dpi=400)
    plt.close()

    # Make legend (separate image file)
    fig, ax_legend = plt.subplots(figsize=(2, 4))
    phases_legend = phases if reverse_phases else phases[::-1]
    for i, phase in enumerate(phases_legend):
        ax_legend.fill_between(
            [],
            [],
            [],
            label=B.label_params[phase],
            facecolor=B.color_params[phase],
            linewidth=0.5,
            edgecolor='#444444')
    ax_legend.legend(
        frameon=False, fontsize=legend_fontsize, bbox_to_anchor=[0.45, 0.5], loc='center',
        ncol=1, labelspacing=1)
    for side in ['left', 'right', 'top', 'bottom']:
        ax_legend.spines[side].set_visible(False)
    ax_legend.set_axis_off()
    lname = "legend_phases_detail" if detail else "legend_phases"
    plt.savefig(f'{save_path}/{lname}.png', dpi=400)
    plt.savefig(f'{save_path}/{lname}.eps', dpi=400)
    plt.close()
