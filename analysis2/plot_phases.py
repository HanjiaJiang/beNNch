import os

import numpy as np
import bennchplot as bp
from matplotlib import pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.transforms as mtransforms

def plot_phases(
         timer_files,
         labels,
         save_path,
         scaling_strength,
         x_axis='num_nodes',
         rtf_ylims=(-0.5, 12.5),
         detail=True,
         reverse_phases=False,
         ignore_others=True,
         legend_fontsize='small',
         ):

    x_axis = x_axis if x_axis == 'num_nvp' else 'num_nodes'

    if x_axis == 'num_nvp':
        xlabel = 'Number of threads'
    else:
        xlabel = 'Number of\ncompute nodes'

    # File count
    fcount = 0
    for timer_file in timer_files:
        if os.path.isfile(timer_file):
            fcount += 1
        else:
            continue


    # Plotting
    widths = [1]*fcount
    heights = [4, 1]
    figsize = (2+2*fcount, 8)
    fig = plt.figure(figsize=figsize)
    spec = gridspec.GridSpec(ncols=fcount, nrows=2, figure=fig,
                             width_ratios=widths,
                             height_ratios=heights)

    # phase labels
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
    if reverse_phases:
        phases.reverse()
        fractions.reverse()
    if ignore_others:
        phases.remove('others_factor')
        fractions.remove('others_frac')

    Bs = []
    axs_rtf = []
    axs_frac = []
    trans = mtransforms.ScaledTranslation(-20 / 72, 7 / 72, fig.dpi_scale_trans)
    for i, timer_file in enumerate(timer_files):
        if not os.path.isfile(timer_file):
            break
        args = {
            'data_file': timer_file,
            'x_axis': [x_axis],
            'time_scaling': 1e3,
        }

        # Instantiate class
        B = bp.Plot(**args)
        Bs.append(B)

        # create axe object
        ax_rtf = fig.add_subplot(spec[0, i])
        ax_frac = fig.add_subplot(spec[1, i])
        axs_rtf.append(ax_rtf)
        axs_frac.append(ax_frac)

        # panel title
        label_i = labels[i].replace("-", "-\n", 1).replace("=", "=\n", 1)
        ax_rtf.set_title(label_i, pad=20, fontsize='medium', fontweight='bold')

        # RTF for state propagation
        Bs[i].plot_fractions(axis=ax_rtf, fill_variables=phases)
        Bs[i].plot_fractions(axis=ax_frac, fill_variables=fractions)

        ax_frac.set_xlabel(xlabel)

        ax_rtf.set_ylim(rtf_ylims)
        ax_frac.set_ylim(-10.0, 110.0)

        if x_axis == 'num_nvp':
            xticks = ax_rtf.get_xticks().flatten()
            xticklabels = (xticks).astype(int)
            ax_rtf.set_xticks(xticks)
            ax_rtf.set_xticklabels(xticklabels)
            ax_frac.set_xticks(xticks)
            ax_frac.set_xticklabels(xticklabels)

        # get network size(s) and add to plot
        if 'N_ex' in Bs[i].df_data and 'N_ex' in Bs[i].df_data and 'N_in' in Bs[i].df_data:
            # calculate from recording
            N_size_labels = (Bs[i].df_data['N_ex'].values + Bs[i].df_data['N_in'].values + Bs[i].df_data['N_astro'].values).astype(int)
        else:
            # calculate from network_size (all nodes in NEST) minus one poisson generator
            N_size_labels = Bs[i].df_data['network_size'].values.astype(int) - 1
        if scaling_strength == 'weak':
            ax_rtf_twin = ax_rtf.twiny() # top axis for network_size
            xticklabels = [np.format_float_scientific(x, trim='-', exp_digits=1).replace("+", "") for x in N_size_labels]
            ax_rtf_twin.set_xticks(ax_rtf.get_xticks().flatten())
            ax_rtf_twin.set_xticklabels(xticklabels, fontsize='small')
            ax_rtf_twin.set_xlabel('Network size\n(number of cells)', fontsize='small')
            ax_rtf_twin.set_xlim(ax_rtf.get_xlim())

    axs_rtf[0].set_ylabel('Real-time factor for\nstate propagation')
    axs_frac[0].set_ylabel('Relative\nreal-time\nfactor (%)')

    plt.tight_layout()
    pname = "plot_phases_detail" if detail else "plot_phases"
    plt.savefig(f'{save_path}/{pname}.png', dpi=400)
    plt.savefig(f'{save_path}/{pname}.eps', format='eps', dpi=400)
    plt.close()

    # Make legend figure
    fig, ax_legend = plt.subplots(figsize=(2, 8))
    phases_ = phases if reverse_phases else phases[::-1]
    for i, phase in enumerate(phases_):
        ax_legend.fill_between(
            [],
            [],
            [],
            label=Bs[0].label_params[phase],
            facecolor=Bs[0].color_params[phase],
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
