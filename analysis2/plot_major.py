import numpy as np
import bennchplot as bp
from matplotlib import pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.transforms as mtransforms

def plot_major(
         files,
         labels,
         save_path,
         scaling_strength,
         x_axis='num_nodes',
         cons_ylims=(0, None),
         prop_ylims=(0, None),
         colors=['k', 'k', 'gray', 'gray'],
         styles=['-', ':', '-', ':'],
    ):

    x_axis = x_axis if x_axis == 'num_nvp' else 'num_nodes'
    print(f'x axis: {x_axis}')

    pobjects = []
    for i, file in enumerate(files):
        args = {'data_file': file, 'x_axis': [x_axis], 'time_scaling': 1e3}
        B = bp.Plot(**args)
        pobjects.append(B)
        labels[i] = labels[i].replace("#", "\n")

    # Plotting
    widths = [1]
    heights = [1, 1]
    fig = plt.figure(figsize=(3, 8))
    spec = gridspec.GridSpec(ncols=1, nrows=2, figure=fig, width_ratios=widths, height_ratios=heights)

    ax_cons = fig.add_subplot(spec[0, 0])
    ax_prop = fig.add_subplot(spec[1, 0])

    if scaling_strength == 'weak':
        ax_cons_twin = ax_cons.twiny() # top axis for network_size

    if x_axis == 'num_nvp':
        xlabel = 'Number of VPs'
    else:
        xlabel = 'Number of\ncompute nodes'

    trans = mtransforms.ScaledTranslation(-20 / 72, 7 / 72, fig.dpi_scale_trans)

    print('plotting timer data ...')

    # Network construction
    lw = 2
    for i in range(len(pobjects)):
        pobjects[i].plot_main(quantities=['time_construct'],
                axis=ax_cons,
                subject=labels[i],
                line_color=colors[i],
                linewidth=lw,
                linestyle=styles[i])
        pobjects[i].plot_main(quantities=['time_simulate'],
                axis=ax_prop,
                subject=labels[i],
                line_color=colors[i],
                linewidth=lw,
                linestyle=styles[i])

    ax_cons.set_ylabel('Network construction\ntime (s)')
    ax_prop.set_ylabel('State propagation time (s)\nfor '
                   r'$T_{\mathrm{model}} =$'
                   + f'{np.unique(pobjects[0].df_data.model_time_sim.values)[0]:.0f} s')

    ax_prop.set_xlabel(xlabel)

    ax_cons.set_ylim(cons_ylims)
    ax_prop.set_ylim(prop_ylims)

    # get network size(s) and add to plot
    if 'N_ex' in pobjects[0].df_data and 'N_ex' in pobjects[0].df_data and 'N_in' in pobjects[0].df_data:
        # calculate from recording
        N_size_labels = (pobjects[0].df_data['N_ex'].values + pobjects[0].df_data['N_in'].values + pobjects[0].df_data['N_astro'].values).astype(int)
    else:
        # calculate from network_size (all nodes in NEST) minus one poisson generator
        N_size_labels = pobjects[0].df_data['network_size'].values.astype(int) - 1
    if scaling_strength == 'weak':
        xticks = sorted(set(pobjects[0].df_data['num_nodes'].values.tolist()))
        ax_cons_twin.set_xticks(xticks)
        xticklabels = [np.format_float_scientific(x, trim='-', exp_digits=1).replace("+", "") for x in N_size_labels]
        ax_cons_twin.set_xticklabels(xticklabels, fontsize='small')
        ax_cons_twin.set_xlabel('Network size\n(number of cells)')
        ax_cons_twin.set_xlim(ax_cons.get_xlim())

    plt.tight_layout()
    plt.savefig(f'{save_path}/plot_major.png', dpi=400)
    plt.savefig(f'{save_path}/plot_major.eps', format='eps', dpi=400)
    plt.close()

    # Output raw data
    for i, B_i in enumerate(pobjects):
        B_i.df_data.to_csv(f"{save_path}/df_{labels[i]}.csv", index=False, float_format="%.3f")
        for j, B_j in enumerate(pobjects):
            if j == i:
                continue
            else:
                df_diff = (B_j.df_data - B_i.df_data)/B_i.df_data
                df_diff.to_csv(f"{save_path}/df_{labels[j]}_to_{labels[i]}.csv", index=False, float_format="%.3f")

    # Make legend figure
    fig, ax_legend = plt.subplots(figsize=(3, 8))
    styles = [('k', '-'), ('k', ':'), ('gray', '-'), ('gray', ':')]
    for i, label in enumerate(labels):
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
        frameon=False, fontsize='medium', bbox_to_anchor=[0.4, 0.5], loc='center',
        ncol=1, labelspacing=1)
    for side in ['left', 'right', 'top', 'bottom']:
        ax_legend.spines[side].set_visible(False)
    ax_legend.set_axis_off()
    plt.savefig(f'{save_path}/legend_major.png', dpi=400)
    plt.savefig(f'{save_path}/legend_major.eps', dpi=400)
    plt.close()
