import numpy as np
import bennchplot as bp
from matplotlib import pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.transforms as mtransforms
plt.rcParams.update({'font.size': 20})

def plot_phases(timer_hash,
         timer_file_astrocyte,
         timer_file_surrogate,
         save_path,
         scaling_strength,
         x_axis='num_nodes',
         rtf_ylims=(-0.5, 12.5),
         data_label='',
         ctrl_label='',
         reverse_phases=False):

    x_axis = x_axis if x_axis == 'num_nvp' else 'num_nodes'
    print(f'x axis: {x_axis}')
    args = {
        'data_file': timer_file_astrocyte,
        'x_axis': [x_axis],
        'time_scaling': 1e3,
        'ctrl_file': timer_file_surrogate,
    }

    # Instantiate class
    B = bp.Plot(**args)

    # Plotting
    widths = [1, 1]
    heights = [4, 1]
    fig = plt.figure(figsize=(8, 8))
    spec = gridspec.GridSpec(ncols=2, nrows=2, figure=fig,
                             width_ratios=widths,
                             height_ratios=heights)

    ax_rtf_astrocyte = fig.add_subplot(spec[0, 0])
    ax_frac_astrocyte = fig.add_subplot(spec[1, 0])
    ax_rtf_surrogate = fig.add_subplot(spec[0, 1])
    ax_frac_surrogate = fig.add_subplot(spec[1, 1])

    ax_rtf_astrocyte.set_title(data_label, pad=20, fontsize='medium', fontweight='bold')
    ax_rtf_surrogate.set_title(ctrl_label, pad=20, fontsize='medium', fontweight='bold')

    if scaling_strength == 'weak':
        ax_rtf_astrocyte_twin = ax_rtf_astrocyte.twiny() # top axis for network_size
        ax_rtf_surrogate_twin = ax_rtf_surrogate.twiny()

    if x_axis == 'num_nvp':
        xlabel = 'Number of threads'
    else:
        xlabel = 'Number of\ncompute nodes'

    trans = mtransforms.ScaledTranslation(-20 / 72, 7 / 72, fig.dpi_scale_trans)

    print("plotting RTF ...")

    # RTF for state propagation
    # variables
    if reverse_phases:
        phases = [
            'phase_others_factor',
            'phase_secondary_factor',
            'phase_ccd_factor',
            'phase_update_factor',
        ]
        fractions=[
            'frac_phase_others',
            'frac_phase_secondary',
            'frac_phase_ccd',
            'frac_phase_update',
        ]
    else:
        phases = [
            'phase_update_factor',
            'phase_ccd_factor',
            'phase_secondary_factor',
            'phase_others_factor',
        ]
        fractions=[
            'frac_phase_update',
            'frac_phase_ccd',
            'frac_phase_secondary',
            'frac_phase_others',
        ]

    # astrocyte
    B.plot_fractions(axis=ax_rtf_astrocyte, fill_variables=phases)
    B.plot_fractions(axis=ax_frac_astrocyte, fill_variables=fractions)

    # surrogate
    B.plot_fractions(axis=ax_rtf_surrogate, fill_variables=phases, control=True)
    B.plot_fractions(axis=ax_frac_surrogate, fill_variables=fractions, control=True)

    ax_rtf_astrocyte.set_ylabel('Real-time factor')
    ax_frac_astrocyte.set_xlabel(xlabel)
    ax_frac_astrocyte.set_ylabel('Relative\nreal-time\nfactor (%)', fontsize='small')
    ax_frac_surrogate.set_xlabel(xlabel)

    ax_rtf_astrocyte.legend()
    ax_rtf_surrogate.legend()
    # to reverse the order
    handles2, labels2 = ax_rtf_astrocyte.get_legend_handles_labels()
    handles3, labels3 = ax_rtf_surrogate.get_legend_handles_labels()
    ax_rtf_astrocyte.legend(handles2[::-1], labels2[::-1], fontsize='small', frameon=False)
    ax_rtf_surrogate.legend(handles3[::-1], labels3[::-1], fontsize='small', frameon=False)

    ax_rtf_astrocyte.set_ylim(rtf_ylims)
    ax_frac_astrocyte.set_ylim(-5.0, 105.0)
    ax_rtf_surrogate.set_ylim(rtf_ylims)
    ax_frac_surrogate.set_ylim(-5.0, 105.0)

    if x_axis == 'num_nvp':
        xticks = ax_rtf_astrocyte.get_xticks().flatten()
        xticklabels = (xticks).astype(int)
        ax_rtf_astrocyte.set_xticks(xticks)
        ax_rtf_astrocyte.set_xticklabels(xticklabels)
        ax_frac_astrocyte.set_xticks(xticks)
        ax_frac_astrocyte.set_xticklabels(xticklabels)

    N_size_labels = B.df_data['network_size'].values.astype(int) - 1 # minus 1 poisson generator
    if scaling_strength == 'weak':
        # astrocyte RTF
        ax_rtf_astrocyte_twin.set_xticks(ax_rtf_astrocyte.get_xticks().flatten())
        ax_rtf_astrocyte_twin.set_xticklabels(N_size_labels.tolist(), rotation=30, fontsize='small')
        ax_rtf_astrocyte_twin.set_xlabel('Network size\n(number of cells)')
        ax_rtf_astrocyte_twin.set_xlim(ax_rtf_astrocyte.get_xlim())
        # surrogate RTF
        ax_rtf_surrogate_twin.set_xticks(ax_rtf_surrogate.get_xticks().flatten())
        ax_rtf_surrogate_twin.set_xticklabels(N_size_labels.tolist(), rotation=30, fontsize='small')
        ax_rtf_surrogate_twin.set_xlabel('Network size\n(number of cells)')
        ax_rtf_surrogate_twin.set_xlim(ax_rtf_surrogate.get_xlim())

    plt.tight_layout()
    plt.savefig(f'{save_path}/plot_phases.png', dpi=400)
    plt.savefig(f'{save_path}/plot_phases.eps', format='eps', dpi=400)
#    plt.savefig(f'{save_path}/{timer_hash}_phases.png', dpi=400)
#    plt.savefig(f'{save_path}/{timer_hash}_phases.eps', format='eps', dpi=400)

    # Calculate relative difference between astrocyte vs. surrogate
    df_data_mean = B.df_data.groupby(["num_nodes", "threads_per_task"]).mean().reset_index()
    df_ctrl_mean = B.df_ctrl.groupby(["num_nodes", "threads_per_task"]).mean().reset_index()
    df_rel_diff = (df_data_mean - df_ctrl_mean)/df_ctrl_mean
    df_rel_diff.to_csv(f"{save_path}/df_rel_diff.csv", index=False, float_format="%.3f")
