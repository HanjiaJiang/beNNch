import numpy as np
import bennchplot as bp
from matplotlib import pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.transforms as mtransforms

def plot_phases_quad(
         timer_file_1,
         timer_file_2,
         timer_file_3,
         timer_file_4,
         save_path,
         scaling_strength,
         x_axis='num_nodes',
         rtf_ylims=(-0.5, 12.5),
         label_1='a',
         label_2='b',
         label_3='c',
         label_4='d',
         secondary=True,
         reverse_phases=False,
         ):

    x_axis = x_axis if x_axis == 'num_nvp' else 'num_nodes'
    print(f'x axis: {x_axis}')
    args1 = {
        'data_file': timer_file_1,
        'x_axis': [x_axis],
        'time_scaling': 1e3,
    }
    args2 = {
        'data_file': timer_file_2,
        'x_axis': [x_axis],
        'time_scaling': 1e3,
    }
    args3 = {
        'data_file': timer_file_3,
        'x_axis': [x_axis],
        'time_scaling': 1e3,
    }
    args4 = {
        'data_file': timer_file_4,
        'x_axis': [x_axis],
        'time_scaling': 1e3,
    }

    # Instantiate class
    B1 = bp.Plot(**args1)
    B2 = bp.Plot(**args2)
    B3 = bp.Plot(**args3)
    B4 = bp.Plot(**args4)

    # Plotting
    widths = [1, 1, 1, 1]
    heights = [4, 1]
    fig = plt.figure(figsize=(14, 8))
    spec = gridspec.GridSpec(ncols=4, nrows=2, figure=fig,
                             width_ratios=widths,
                             height_ratios=heights)

    ax_rtf_1 = fig.add_subplot(spec[0, 0])
    ax_frac_1 = fig.add_subplot(spec[1, 0])
    ax_rtf_2 = fig.add_subplot(spec[0, 1])
    ax_frac_2 = fig.add_subplot(spec[1, 1])
    ax_rtf_3 = fig.add_subplot(spec[0, 2])
    ax_frac_3 = fig.add_subplot(spec[1, 2])
    ax_rtf_4 = fig.add_subplot(spec[0, 3])
    ax_frac_4 = fig.add_subplot(spec[1, 3])

    label_1 = label_1.replace('#', '\n')
    label_2 = label_2.replace('#', '\n')
    label_3 = label_3.replace('#', '\n')
    label_4 = label_4.replace('#', '\n')
    ax_rtf_1.set_title(label_1, pad=20, fontsize='small', fontweight='bold')
    ax_rtf_2.set_title(label_2, pad=20, fontsize='small', fontweight='bold')
    ax_rtf_3.set_title(label_3, pad=20, fontsize='small', fontweight='bold')
    ax_rtf_4.set_title(label_4, pad=20, fontsize='small', fontweight='bold')

    if scaling_strength == 'weak':
        ax_rtf_1_twin = ax_rtf_1.twiny() # top axis for network_size
        ax_rtf_2_twin = ax_rtf_2.twiny()
        ax_rtf_3_twin = ax_rtf_3.twiny()
        ax_rtf_4_twin = ax_rtf_4.twiny()

    if x_axis == 'num_nvp':
        xlabel = 'Number of threads'
    else:
        xlabel = 'Number of\ncompute nodes'

    trans = mtransforms.ScaledTranslation(-20 / 72, 7 / 72, fig.dpi_scale_trans)

    print("plotting RTF ...")

    if secondary:
        phases = [
            'phase_update_factor',
            # 'phase_ccd_factor',
            'phase_collocate_factor',
            'phase_communicate_factor',
            'phase_deliver_factor',
            # 'phase_secondary_factor',
            'phase_gather_secondary_factor',
            'phase_deliver_secondary_factor',
            'phase_others_factor',
        ]
        fractions=[
            'frac_phase_update',
            # 'frac_phase_ccd',
            'frac_phase_collocate',
            'frac_phase_communicate',
            'frac_phase_deliver',
            # 'frac_phase_secondary',
            'frac_phase_gather_secondary',
            'frac_phase_deliver_secondary',
            'frac_phase_others',
        ]
    else:
        phases = [
            'phase_update_factor',
            'phase_ccd_factor',
            'phase_secondary_factor',
        ]
        fractions = [
            'frac_phase_update',
            'frac_phase_ccd',
            'frac_phase_secondary',
        ]
    if reverse_phases:
        phases.reverse()
        fractions.reverse()


    # RTF for state propagation
    B1.plot_fractions(axis=ax_rtf_1, fill_variables=phases)
    B1.plot_fractions(axis=ax_frac_1, fill_variables=fractions)
    B2.plot_fractions(axis=ax_rtf_2, fill_variables=phases)
    B2.plot_fractions(axis=ax_frac_2, fill_variables=fractions)
    B3.plot_fractions(axis=ax_rtf_3, fill_variables=phases)
    B3.plot_fractions(axis=ax_frac_3, fill_variables=fractions)
    B4.plot_fractions(axis=ax_rtf_4,  fill_variables=phases)
    B4.plot_fractions(axis=ax_frac_4, fill_variables=fractions)

    ax_rtf_1.set_ylabel('Real-time factor for\nstate propagation')
    ax_frac_1.set_ylabel('Relative\nreal-time\nfactor (%)', fontsize='small')
    ax_frac_1.set_xlabel(xlabel, fontsize='small')
    ax_frac_2.set_xlabel(xlabel, fontsize='small')
    ax_frac_3.set_xlabel(xlabel, fontsize='small')
    ax_frac_4.set_xlabel(xlabel, fontsize='small')

    ax_rtf_1.set_ylim(rtf_ylims)
    ax_frac_1.set_ylim(-10.0, 110.0)
    ax_rtf_2.set_ylim(rtf_ylims)
    ax_frac_2.set_ylim(-10.0, 110.0)
    ax_rtf_3.set_ylim(rtf_ylims)
    ax_frac_3.set_ylim(-10.0, 110.0)
    ax_rtf_4.set_ylim(rtf_ylims)
    ax_frac_4.set_ylim(-10.0, 110.0)

    if x_axis == 'num_nvp':
        xticks = ax_rtf_1.get_xticks().flatten()
        xticklabels = (xticks).astype(int)
        ax_rtf_1.set_xticks(xticks)
        ax_rtf_1.set_xticklabels(xticklabels)
        ax_frac_1.set_xticks(xticks)
        ax_frac_1.set_xticklabels(xticklabels)
        ax_rtf_2.set_xticks(xticks)
        ax_rtf_2.set_xticklabels(xticklabels)
        ax_frac_2.set_xticks(xticks)
        ax_frac_2.set_xticklabels(xticklabels)
        ax_rtf_3.set_xticks(xticks)
        ax_rtf_3.set_xticklabels(xticklabels)
        ax_frac_3.set_xticks(xticks)
        ax_frac_3.set_xticklabels(xticklabels)
        ax_rtf_4.set_xticks(xticks)
        ax_rtf_4.set_xticklabels(xticklabels)
        ax_frac_4.set_xticks(xticks)
        ax_frac_4.set_xticklabels(xticklabels)

    N_size_labels = B1.df_data['network_size'].values.astype(int) - 1 # minus 1 poisson generator
    if scaling_strength == 'weak':
        xticklabels = [np.format_float_scientific(x, trim='-', exp_digits=1).replace("+", "") for x in N_size_labels]
        # 1
        ax_rtf_1_twin.set_xticks(ax_rtf_1.get_xticks().flatten())
        ax_rtf_1_twin.set_xticklabels(xticklabels, fontsize='small')
        ax_rtf_1_twin.set_xlabel('Network size\n(number of cells)', fontsize='small')
        ax_rtf_1_twin.set_xlim(ax_rtf_1.get_xlim())
        # 2
        ax_rtf_2_twin.set_xticks(ax_rtf_2.get_xticks().flatten())
        ax_rtf_2_twin.set_xticklabels(xticklabels, fontsize='small')
        ax_rtf_2_twin.set_xlabel('Network size\n(number of cells)', fontsize='small')
        ax_rtf_2_twin.set_xlim(ax_rtf_2.get_xlim())
        # 3            
        ax_rtf_3_twin.set_xticks(ax_rtf_3.get_xticks().flatten())
        ax_rtf_3_twin.set_xticklabels(xticklabels, fontsize='small')
        ax_rtf_3_twin.set_xlabel('Network size\n(number of cells)', fontsize='small')
        ax_rtf_3_twin.set_xlim(ax_rtf_3.get_xlim())
        # 4
        ax_rtf_4_twin.set_xticks(ax_rtf_4.get_xticks().flatten())
        ax_rtf_4_twin.set_xticklabels(xticklabels, fontsize='small')
        ax_rtf_4_twin.set_xlabel('Network size\n(number of cells)', fontsize='small')
        ax_rtf_4_twin.set_xlim(ax_rtf_4.get_xlim())

    plt.tight_layout()
    plt.savefig(f'{save_path}/plot_phases_quad.png', dpi=400)
    plt.savefig(f'{save_path}/plot_phases_quad.eps', format='eps', dpi=400)
    plt.close()

    # Make legend figure
    fig, ax_legend = plt.subplots(figsize=(3, 8))
    phases_ = phases if reverse_phases else phases[::-1]
    for i, phase in enumerate(phases_):
        ax_legend.fill_between(
            [],
            [],
            [],
            label=B1.label_params[phase],
            facecolor=B1.color_params[phase],
            linewidth=0.5,
            edgecolor='#444444')
    ax_legend.legend(
        frameon=False, fontsize='x-small', bbox_to_anchor=[0.5, 0.5], loc='center',
        ncol=1)
    for side in ['left', 'right', 'top', 'bottom']:
        ax_legend.spines[side].set_visible(False)
    ax_legend.set_axis_off()
    plt.savefig(f'{save_path}/legend_phases.png', dpi=400)
    plt.savefig(f'{save_path}/legend_phases.eps', dpi=400)
    plt.close()
