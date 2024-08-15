import numpy as np
import bennchplot as bp
from matplotlib import pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.transforms as mtransforms

def plot_thirdin(
         timer_file_1,
         save_path,
         scaling_strength,
         x_axis='num_nodes',
         label_1='a',
    ):

    x_axis = x_axis if x_axis == 'num_nvp' else 'num_nodes'
    args1 = {
        'data_file': timer_file_1,
        'x_axis': [x_axis],
        'time_scaling': 1e3,
    }

    # Instantiate class
    B1 = bp.Plot(**args1)

    label_1 = label_1.replace("#", "\n")

    # Plotting
    widths = [1]
    heights = [1, 1, 1, 1, 1]
    fig = plt.figure(figsize=(4, 8))
    spec = gridspec.GridSpec(ncols=1, nrows=5, figure=fig,
                             width_ratios=widths,
                             height_ratios=heights)

    ax_count = fig.add_subplot(spec[0, 0])
    ax_max = fig.add_subplot(spec[1, 0])
    ax_fill = fig.add_subplot(spec[2, 0])
    ax_communicate = fig.add_subplot(spec[3, 0])
    ax_connect = fig.add_subplot(spec[4, 0])

    if scaling_strength == 'weak':
        ax_count_twin = ax_coount.twiny() # top axis for network_size

    if x_axis == 'num_nvp':
        xlabel = 'Number of threads'
    else:
        xlabel = 'Number of\ncompute nodes'

    trans = mtransforms.ScaledTranslation(-20 / 72, 7 / 72, fig.dpi_scale_trans)

    # Network construction
    B1.plot_main(quantities=['time_construction_connect_third_inner_count'],
                axis=ax_count,
                subject=label_1,
                line_color='k',
                linewidth=2,
                linestyle='-')
    B1.plot_main(quantities=['time_construction_connect_third_inner_max'],
                axis=ax_max,
                subject=label_1,
                line_color='k',
                linewidth=2,
                linestyle='-')
    B1.plot_main(quantities=['time_construction_connect_third_inner_fill'],
                axis=ax_fill,
                subject=label_1,
                line_color='k',
                linewidth=2,
                linestyle='-')
    B1.plot_main(quantities=['time_construction_connect_third_inner_communicate'],
                axis=ax_communicate,
                subject=label_1,
                line_color='k',
                linewidth=2,
                linestyle='-')
    B1.plot_main(quantities=['time_construction_connect_third_inner_connect'],
                axis=ax_connect,
                subject=label_1,
                line_color='k',
                linewidth=2,
                linestyle='-')

    ax_count.set_ylabel('Time for\n\"count\" (s)')
    ax_max.set_ylabel('Time for\n\"max\" (s)')
    ax_fill.set_ylabel('Time for\n\"fill\"(s)')
    ax_communicate.set_ylabel('Time for\n\"communicate\"\n(s)')
    ax_connect.set_ylabel('Time for\n\"connect\" (s)')

    ax_connect.set_xlabel(xlabel)

    if x_axis == 'num_nvp':
        xticks = ax_count.get_xticks().flatten()
        xticklabels = (xticks).astype(int)
        ax_count.set_xticks(xticks)
        ax_count.set_xticklabels(xticklabels)
        ax_max.set_xticks(xticks)
        ax_max.set_xticklabels(xticklabels)
        ax_fill.set_xticks(xticks)
        ax_fill.set_xticklabels(xticklabels)
        ax_communicate.set_xticks(xticks)
        ax_communicate.set_xticklabels(xticklabels)
        ax_connect.set_xticks(xticks)
        ax_connect.set_xticklabels(xticklabels)

    N_size_labels = B1.df_data['network_size'].values.astype(int) - 1 # minus 1 poisson generator
    if scaling_strength == 'weak':
        xticks = sorted(set(B1.df_data['num_nodes'].values.tolist()))
        ax_count_twin.set_xticks(xticks)
        xticklabels = [np.format_float_scientific(x, trim='-', exp_digits=1).replace("+", "") for x in N_size_labels]
        ax_count_twin.set_xticklabels(xticklabels, fontsize='small')
        ax_count_twin.set_xlabel('Network size\n(number of cells)')
        ax_count_twin.set_xlim(ax_count.get_xlim())

    plt.tight_layout()
    plt.savefig(f'{save_path}/plot_thirdin.png', dpi=400)
    plt.savefig(f'{save_path}/plot_thirdin.eps', format='eps', dpi=400)
    plt.close()
