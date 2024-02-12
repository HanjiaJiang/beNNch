import numpy as np
import bennchplot as bp
from matplotlib import pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.transforms as mtransforms
plt.rcParams.update({'font.size': 20})

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
         label_4='d'
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
    fig = plt.figure(figsize=(12, 8))
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

    ax_rtf_1.set_title(label_1, pad=20, fontsize='medium', fontweight='bold')
    ax_rtf_2.set_title(label_2, pad=20, fontsize='medium', fontweight='bold')
    ax_rtf_3.set_title(label_3, pad=20, fontsize='medium', fontweight='bold')
    ax_rtf_4.set_title(label_4, pad=20, fontsize='medium', fontweight='bold')

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

    # RTF for state propagation
    B1.plot_fractions(axis=ax_rtf_1,
                     fill_variables=[
                         'phase_others_factor',
                         'phase_ccd_factor',
                         'phase_update_factor',
                     ],
                     )
    B1.plot_fractions(axis=ax_frac_1,
                     fill_variables=[
                         'frac_phase_others',
                         'frac_phase_ccd',
                         'frac_phase_update',
                     ],
                     )
    B2.plot_fractions(axis=ax_rtf_2,
                     fill_variables=[
                         'phase_others_factor',
                         'phase_ccd_factor',
                         'phase_update_factor',
                     ],
                     )
    B2.plot_fractions(axis=ax_frac_2,
                     fill_variables=[
                         'frac_phase_others',
                         'frac_phase_ccd',
                         'frac_phase_update',
                     ],
                     )
    B3.plot_fractions(axis=ax_rtf_3,
                     fill_variables=[
                         'phase_others_factor',
                         'phase_ccd_factor',
                         'phase_update_factor',
                     ],
                     )
    B3.plot_fractions(axis=ax_frac_3,
                     fill_variables=[
                         'frac_phase_others',
                         'frac_phase_ccd',
                         'frac_phase_update',
                     ],
                     )
    B4.plot_fractions(axis=ax_rtf_4,
                     fill_variables=[
                         'phase_others_factor',
                         'phase_ccd_factor',
                         'phase_update_factor',
                     ],
                     )
    B4.plot_fractions(axis=ax_frac_4,
                     fill_variables=[
                         'frac_phase_others',
                         'frac_phase_ccd',
                         'frac_phase_update',
                     ],
                     )

    ax_rtf_1.set_ylabel('Real-time factor of\nstate propagation')
    ax_frac_1.set_ylabel('Relative\nreal-time\nfactor (%)', fontsize='small')
    ax_frac_1.set_xlabel(xlabel)
    ax_frac_2.set_xlabel(xlabel)
    ax_frac_3.set_xlabel(xlabel)
    ax_frac_4.set_xlabel(xlabel)

    ax_rtf_4.legend()
    # to reverse the order
    handles2, labels2 = ax_rtf_4.get_legend_handles_labels()
    ax_rtf_4.legend(handles2[::-1], labels2[::-1], fontsize='small', frameon=False)

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
        # 1
        ax_rtf_1_twin.set_xticks(ax_rtf_1.get_xticks().flatten())
        ax_rtf_1_twin.set_xticklabels(N_size_labels.tolist(), rotation=30, fontsize='small')
        ax_rtf_1_twin.set_xlabel('Network size\n(number of cells)')
        ax_rtf_1_twin.set_xlim(ax_rtf_1.get_xlim())
        # 2
        ax_rtf_2_twin.set_xticks(ax_rtf_2.get_xticks().flatten())
        ax_rtf_2_twin.set_xticklabels(N_size_labels.tolist(), rotation=30, fontsize='small')
        ax_rtf_2_twin.set_xlabel('Network size\n(number of cells)')
        ax_rtf_2_twin.set_xlim(ax_rtf_2.get_xlim())
        # 3            
        ax_rtf_3_twin.set_xticks(ax_rtf_3.get_xticks().flatten())
        ax_rtf_3_twin.set_xticklabels(N_size_labels.tolist(), rotation=30, fontsize='small')
        ax_rtf_3_twin.set_xlabel('Network size\n(number of cells)')
        ax_rtf_3_twin.set_xlim(ax_rtf_3.get_xlim())
        # 4
        ax_rtf_4_twin.set_xticks(ax_rtf_4.get_xticks().flatten())
        ax_rtf_4_twin.set_xticklabels(N_size_labels.tolist(), rotation=30, fontsize='small')
        ax_rtf_4_twin.set_xlabel('Network size\n(number of cells)')
        ax_rtf_4_twin.set_xlim(ax_rtf_4.get_xlim())

    plt.tight_layout()
    plt.savefig(f'{save_path}/plot_phases_quad.png', dpi=400)
    plt.savefig(f'{save_path}/plot_phases_quad.eps', format='eps', dpi=400)
