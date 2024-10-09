import os

import numpy as np
import bennchplot as bp
from matplotlib import pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.transforms as mtransforms
import matplotlib.ticker as ticker

def plot_separate(
         timer_files,
         labels,
         save_path,
         scaling_strength,
         quantities,
         x_axis='num_nodes',
         colors=['b', 'g', 'orange', 'purple'],
         lw=4,
         alpha=0.6,
         file_postfix='',
         ylabel_prefix='',
    ):

    # create plot objects
    pobjects = []
    for i, timer_file in enumerate(timer_files):
        if not os.path.isfile(timer_file):
            break
        args = {'data_file': timer_file, 'x_axis': [x_axis], 'time_scaling': 1e3}
        B = bp.Plot(**args)
        pobjects.append(B)

    # create figure
    fig, axs = plt.subplots(1, 4, figsize=(12, 8))    

    # set xlabel
    if x_axis == 'num_nvp':
        xlabel = 'Number of\nvirtual processes'
    else:
        xlabel = 'Number of\ncompute nodes'

    # plot
    for q, quantity in enumerate(quantities):
        for p, pobject in enumerate(pobjects):
            pobject.plot_main(quantities=[quantity], axis=axs[q], subject=labels[p], line_color=colors[p], linewidth=lw, alpha=alpha)

    # get network size data
    xticks = sorted(set(pobjects[0].df_data['num_nodes'].values.tolist()))
    if 'N_ex' in pobjects[0].df_data and 'N_ex' in pobjects[0].df_data and 'N_in' in pobjects[0].df_data:
        # calculate from recording
        N_size_labels = (pobjects[0].df_data['N_ex'].values + pobjects[0].df_data['N_in'].values + pobjects[0].df_data['N_astro'].values).astype(int)
    else:
        # calculate from network_size (all nodes in NEST) minus one poisson generator
        N_size_labels = pobjects[0].df_data['network_size'].values.astype(int) - 1
    xticklabels = [np.format_float_scientific(x, trim='-', exp_digits=1).replace("+", "") for x in N_size_labels]

    # set labels and twins
    for i, ax in enumerate(axs):
        ax.set_ylim(bottom=0)
        ax.set_xlabel(xlabel)
        ylabel = pobjects[0].label_params[quantities[i]]
        ax.set_ylabel(f"{ylabel_prefix}{ylabel}")
        if scaling_strength == 'weak':
            ax_twin = ax.twiny() # top axis for network_size            
            ax_twin.set_xticks(xticks)            
            ax_twin.set_xticklabels(xticklabels, fontsize='small')
            ax_twin.set_xlabel('Network size\n(number of cells)')
            ax_twin.set_xlim(ax.get_xlim())

    # save
    plt.tight_layout()
    plt.savefig(f'{save_path}/plot_separate_{file_postfix}.png', dpi=400)
    plt.savefig(f'{save_path}/plot_separate_{file_postfix}.eps', format='eps', dpi=400)
    plt.close()

    # make legend figure
    fig, ax_legend = plt.subplots(figsize=(3, 8))
    for i, label in enumerate(labels):
        if not os.path.isfile(timer_files[i]):
            break
        ax_legend.plot(
            [],
            [],
            label=label,
            marker=None,
            color=colors[i],
            linewidth=lw,
            alpha=alpha,
        )
    ax_legend.legend(
        frameon=False, fontsize='medium', bbox_to_anchor=[0.4, 0.5], loc='center',
        ncol=1, labelspacing=1)
    for side in ['left', 'right', 'top', 'bottom']:
        ax_legend.spines[side].set_visible(False)
    ax_legend.set_axis_off()
    plt.savefig(f'{save_path}/legend_separate_{file_postfix}.png', dpi=400)
    plt.savefig(f'{save_path}/legend_separate_{file_postfix}.eps', dpi=400)
    plt.close()

