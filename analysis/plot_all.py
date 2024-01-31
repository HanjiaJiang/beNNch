import numpy as np
import bennchplot as bp
from matplotlib import pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.transforms as mtransforms
plt.rcParams.update({'font.size': 20})

def plot_all(timer_hash,
         timer_file_astrocyte,
         timer_file_surrogate,
         save_path,
         scaling_strength,
         x_axis='num_nodes',
         cons_ylims=(-1.0, 101.0),
         prop_ylims=(-1.0, 101.0),
         spk_ylims=(-10000.0, 2010000.0)):

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
    widths = [1]
    heights = [2, 2, 1]
    fig = plt.figure(figsize=(6, 8))
    spec = gridspec.GridSpec(ncols=1, nrows=3, figure=fig,
                             width_ratios=widths,
                             height_ratios=heights)

    ax_cons = fig.add_subplot(spec[0, 0])
    ax_prop = fig.add_subplot(spec[1, 0])
    ax_spk = fig.add_subplot(spec[2, 0])

    if scaling_strength == 'weak':
        ax_cons_twin = ax_cons.twiny() # top axis for network_size

    if x_axis == 'num_nvp':
        xlabel = 'Number of threads'
    else:
        xlabel = 'Number of compute nodes'

    trans = mtransforms.ScaledTranslation(-20 / 72, 7 / 72, fig.dpi_scale_trans)

    print('plotting timer data ...')

    # Network construction
    B.plot_main(quantities=['wall_time_create+wall_time_connect'],
                axis=ax_cons,
                subject='astrocyte_lr_1994',
                line_color='k',
                linewidth=2)
    B.plot_main(quantities=['wall_time_create+wall_time_connect'],
                axis=ax_cons,
                control=True,
                subject='astrocyte_surrogate',
                line_color='gray',
                linewidth=2)

    # State propagation
    B.plot_main(quantities=['wall_time_sim'],
                axis=ax_prop,
                subject='astrocyte_lr_1994',
                line_color='k',
                linewidth=2)
    B.plot_main(quantities=['wall_time_sim'],
                axis=ax_prop,
                control=True,
                subject='astrocyte_surrogate',
                line_color='gray',
                linewidth=2)

    # Average firing rate
    B.plot_main(quantities=['average_firing_rate'],
                axis=ax_spk,
                subject='astrocyte_lr_1994',
                line_color='k',
                linewidth=2)
    B.plot_main(quantities=['average_firing_rate'],
                axis=ax_spk,
                control=True,
                subject='astrocyte_surrogate',
                line_color='gray',
                linewidth=2)

    ax_cons.set_ylabel('Network\nconstruction\ntime (s)')
    ax_prop.set_ylabel('State propagation\ntime (s) for\n'
                   r'$T_{\mathrm{model}} =$'
                   + f'{np.unique(B.df_data.model_time_sim.values)[0]:.0f} s')
    ax_spk.set_xlabel(xlabel)
    ax_spk.set_ylabel('Average\nfiring rate\n(spikes/s)')

    ax_cons.legend(fontsize='small', frameon=False)
    # to reverse the order
    # handles1, labels1 = ax_cons.get_legend_handles_labels()

    ax_cons.set_ylim(cons_ylims)
    ax_prop.set_ylim(prop_ylims)
    ax_spk.set_ylim(spk_ylims)

    if x_axis == 'num_nvp':
        xticks = ax_cons.get_xticks().flatten()
        xticklabels = (xticks).astype(int)
        ax_cons.set_xticks(xticks)
        ax_cons.set_xticklabels(xticklabels)
        ax_prop.set_xticks(xticks)
        ax_prop.set_xticklabels(xticklabels)
        ax_spk.set_xticks(xticks)
        ax_spk.set_xticklabels(xticklabels)

    N_size_labels = B.df_data['network_size'].values.astype(int) - 1 # minus 1 poisson generator
    if scaling_strength == 'weak':
        # astrocyte+surrogate construction time
        ax_cons_twin.set_xticks(ax_cons.get_xticks().flatten())
        ax_cons_twin.set_xticklabels(N_size_labels.tolist(), rotation=30, fontsize='small')
        ax_cons_twin.set_xlabel('Network size (number of cells)')
        ax_cons_twin.set_xlim(ax_cons.get_xlim())

    plt.tight_layout()
    plt.savefig(f'{save_path}/plot_all.png', dpi=400)
    plt.savefig(f'{save_path}/plot_all.eps', format='eps', dpi=400)
#    plt.savefig(f'{save_path}/{timer_hash}_all.png', dpi=400)
#    plt.savefig(f'{save_path}/{timer_hash}_all.eps', format='eps', dpi=400)

    # Calculate relative difference between astrocyte vs. surrogate
    df_data_mean = B.df_data.groupby(["num_nodes", "threads_per_task"]).mean().reset_index()
    df_ctrl_mean = B.df_ctrl.groupby(["num_nodes", "threads_per_task"]).mean().reset_index()
    df_rel_diff = (df_data_mean - df_ctrl_mean)/df_ctrl_mean
    df_rel_diff.to_csv(f"{save_path}/df_rel_diff.csv", index=False, float_format="%.3f")
