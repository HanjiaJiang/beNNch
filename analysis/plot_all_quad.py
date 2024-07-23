import numpy as np
import bennchplot as bp
from matplotlib import pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.transforms as mtransforms

def plot_all_quad(
         timer_file_1,
         timer_file_2,
         timer_file_3,
         timer_file_4,
         save_path,
         scaling_strength,
         x_axis='num_nodes',
         cons_ylims=(-1.0, 101.0),
         prop_ylims=(-1.0, 101.0),
         conn_ylims=(3990000, 4010000),
         spk_ylims=(-10000.0, 2010000.0),
         label_1='a',
         label_2='b',
         label_3='c',
         label_4='d',
         conn_plotted="sic_connection",
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

    label_1 = label_1.replace("#", "\n")
    label_2 = label_2.replace("#", "\n")
    label_3 = label_3.replace("#", "\n")
    label_4 = label_4.replace("#", "\n")

    # Plotting
    widths = [1]
    heights = [2, 1, 2, 1]
    fig = plt.figure(figsize=(6, 8))
    spec = gridspec.GridSpec(ncols=1, nrows=4, figure=fig,
                             width_ratios=widths,
                             height_ratios=heights)

    ax_cons = fig.add_subplot(spec[0, 0])
    ax_prop = fig.add_subplot(spec[2, 0])
    ax_conn = fig.add_subplot(spec[1, 0])
    ax_spk = fig.add_subplot(spec[3, 0])

    if scaling_strength == 'weak':
        ax_cons_twin = ax_cons.twiny() # top axis for network_size

    if x_axis == 'num_nvp':
        xlabel = 'Number of threads'
    else:
        xlabel = 'Number of compute nodes'

    trans = mtransforms.ScaledTranslation(-20 / 72, 7 / 72, fig.dpi_scale_trans)

    print('plotting timer data ...')

    # Network construction
    B1.plot_main(quantities=['wall_time_create+wall_time_connect'],
                axis=ax_cons,
                subject=label_1,
                line_color='k',
                linewidth=2,
                linestyle='-')
    B2.plot_main(quantities=['wall_time_create+wall_time_connect'],
                axis=ax_cons,
                subject=label_2,
                line_color='k',
                linewidth=2,
                linestyle=':')
    B3.plot_main(quantities=['wall_time_create+wall_time_connect'],
                axis=ax_cons,
                subject=label_3,
                line_color='gray',
                linewidth=2,
                linestyle='-')
    B4.plot_main(quantities=['wall_time_create+wall_time_connect'],
                axis=ax_cons,
                subject=label_4,
                line_color='gray',
                linewidth=2,
                linestyle=':')

    # State propagation
    B1.plot_main(quantities=['wall_time_sim'],
                axis=ax_prop,
                subject=label_1,
                line_color='k',
                linewidth=2, 
                linestyle='-')
    B2.plot_main(quantities=['wall_time_sim'],
                axis=ax_prop,
                subject=label_2,
                line_color='k',
                linewidth=2,
                linestyle=':')
    B3.plot_main(quantities=['wall_time_sim'],
                axis=ax_prop,
                subject=label_3,
                line_color='gray',
                linewidth=2, 
                linestyle='-')
    B4.plot_main(quantities=['wall_time_sim'],
                axis=ax_prop,
                subject=label_4,
                line_color='gray',
                linewidth=2,
                linestyle=':')

    # Number of connections
    B1.plot_main(quantities=[conn_plotted],
                axis=ax_conn,
                subject=label_1,
                line_color='k',
                linewidth=2,
                linestyle='-')
    B2.plot_main(quantities=[conn_plotted],
                axis=ax_conn,
                subject=label_2,
                line_color='k',
                linewidth=2,
                linestyle=':')
    B3.plot_main(quantities=[conn_plotted],
                axis=ax_conn,
                subject=label_3,
                line_color='gray',
                linewidth=2,
                linestyle='-')
    B4.plot_main(quantities=[conn_plotted],
                axis=ax_conn,
                subject=label_4,
                line_color='gray',
                linewidth=2,
                linestyle=':')

    # Average firing rate
    B1.plot_main(quantities=['average_firing_rate'],
                axis=ax_spk,
                subject=label_1,
                line_color='k',
                linewidth=2,
                linestyle='-')
    B2.plot_main(quantities=['average_firing_rate'],
                axis=ax_spk,
                subject=label_2,
                line_color='k',
                linewidth=2,
                linestyle=':')
    B3.plot_main(quantities=['average_firing_rate'],
                axis=ax_spk,
                subject=label_3,
                line_color='gray',
                linewidth=2,
                linestyle='-')
    B4.plot_main(quantities=['average_firing_rate'],
                axis=ax_spk,
                subject=label_4,
                line_color='gray',
                linewidth=2,
                linestyle=':')

    ax_cons.set_ylabel('Network\nconstruction\ntime (s)')
    ax_prop.set_ylabel('State\npropagation\ntime (s) for\n'
                   r'$T_{\mathrm{model}} =$'
                   + f'{np.unique(B1.df_data.model_time_sim.values)[0]:.0f} s')
    if conn_plotted == "sic_connection":
        text_conn = "SIC\nconnections"
    elif conn_plotted == "tsodyks_synapse":
        text_conn = "Tsodyks\nsynapses"
    else:
        text_conn = "connections"
    ax_conn.set_ylabel(f'Number of\n{text_conn}')
    ax_spk.set_xlabel(xlabel)
    ax_spk.set_ylabel('Average\nneuronal\nfiring rate\n(spikes/s)')

    ax_cons.set_ylim(cons_ylims)
    ax_prop.set_ylim(prop_ylims)
    ax_conn.set_ylim(conn_ylims)
    ax_spk.set_ylim(spk_ylims)

    if x_axis == 'num_nvp':
        xticks = ax_cons.get_xticks().flatten()
        xticklabels = (xticks).astype(int)
        ax_cons.set_xticks(xticks)
        ax_cons.set_xticklabels(xticklabels)
        ax_prop.set_xticks(xticks)
        ax_prop.set_xticklabels(xticklabels)
        ax_conn.set_xticks(xticks)
        ax_conn.set_xticklabels(xticklabels)
        ax_spk.set_xticks(xticks)
        ax_spk.set_xticklabels(xticklabels)

    N_size_labels = B1.df_data['network_size'].values.astype(int) - 1 # minus 1 poisson generator
    if scaling_strength == 'weak':
        xticks = sorted(set(B1.df_data['num_nodes'].values.tolist()))
        ax_cons_twin.set_xticks(xticks)
        xticklabels = [np.format_float_scientific(x, trim='-', exp_digits=1).replace("+", "") for x in N_size_labels]
        ax_cons_twin.set_xticklabels(xticklabels, fontsize='small')
        ax_cons_twin.set_xlabel('Network size (number of cells)')
        ax_cons_twin.set_xlim(ax_cons.get_xlim())

    plt.tight_layout()
    plt.savefig(f'{save_path}/plot_all_quad.png', dpi=400)
    plt.savefig(f'{save_path}/plot_all_quad.eps', format='eps', dpi=400)
    plt.close()

    # Output raw data
    df_mean_1 = B1.df_data.groupby(["num_nodes", "threads_per_task"]).mean().reset_index()
    df_mean_2 = B2.df_data.groupby(["num_nodes", "threads_per_task"]).mean().reset_index()
    df_mean_3 = B3.df_data.groupby(["num_nodes", "threads_per_task"]).mean().reset_index()
    df_mean_4 = B4.df_data.groupby(["num_nodes", "threads_per_task"]).mean().reset_index()
    df_mean_1.to_csv(f"{save_path}/df_mean_1.csv", index=False, float_format="%.3f")
    df_mean_2.to_csv(f"{save_path}/df_mean_2.csv", index=False, float_format="%.3f")
    df_mean_3.to_csv(f"{save_path}/df_mean_3.csv", index=False, float_format="%.3f")
    df_mean_4.to_csv(f"{save_path}/df_mean_4.csv", index=False, float_format="%.3f")
#    df_rel_diff = (df_data_mean - df_ctrl_mean)/df_ctrl_mean
#    df_rel_diff.to_csv(f"{save_path}/df_rel_diff.csv", index=False, float_format="%.3f")

    # Make legend figure
    fig, ax_legend = plt.subplots(figsize=(3, 8))
    styles = [('k', '-'), ('k', ':'), ('gray', '-'), ('gray', ':')]
    for i, label in enumerate([label_1, label_2, label_3, label_4]):
        ax_legend.plot(
            [],
            [],
            label=label,
            marker=None,
            color=styles[i][0],
            linewidth=3,
            linestyle=styles[i][1],
        )
    ax_legend.legend(
        frameon=False, fontsize='x-small', bbox_to_anchor=[0.5, 0.5], loc='center',
        ncol=1, labelspacing=1)
    for side in ['left', 'right', 'top', 'bottom']:
        ax_legend.spines[side].set_visible(False)
    ax_legend.set_axis_off()
    plt.savefig(f'{save_path}/legend_all.png', dpi=400)
    plt.savefig(f'{save_path}/legend_all.eps', dpi=400)
    plt.close()
