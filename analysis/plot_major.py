import os

import numpy as np
import bennchplot as bp
from matplotlib import pyplot as plt
import matplotlib.gridspec as gridspec
#import matplotlib.transforms as mtransforms
import matplotlib.ticker as ticker

do_diff = True

def plot_major(
         timer_files,
         labels,
         save_path,
         scaling_strength,
         x_axis='num_nodes',
         cons_ylims=None,
         conn_ylims=None,
         prop_ylims=None,
         colors=None,
         styles=None,
         lw=3,
         tk_size='small',
    ):

    # Set x axis type and label
    x_axis = x_axis if x_axis == 'num_nvp' else 'num_nodes'
    if x_axis == 'num_nvp':
        xlabel = 'Number of VPs'
    else:
        xlabel = 'Number of\ncompute nodes'

    # Set line colors and styles
    colors = colors if isinstance(colors, list) else ['#004488','#994455','#997700','#6699cc']
    styles = styles if isinstance(styles, list) else ['-', '--', ':', ':']

    # Create plot objects and get model time in s
    pobjects = []
    model_time_in_s = None
    for i, timer_file in enumerate(timer_files):
        if not os.path.isfile(timer_file):
            break
        args = {'data_file': timer_file, 'x_axis': [x_axis], 'time_scaling': 1e3}
        B = bp.Plot(**args)
        pobjects.append(B)
        if model_time_in_s is None:
            model_time_in_s = B.df_data["model_time_sim"][0]

    # Create figure and axes
    widths = [1, 1, 1]
    heights = [1]
    fig = plt.figure(figsize=(8, 4))
    spec = gridspec.GridSpec(ncols=3, nrows=1, figure=fig, width_ratios=widths, height_ratios=heights)

    ax_crea = fig.add_subplot(spec[0, 0])
    ax_conn = fig.add_subplot(spec[0, 1])
    ax_prop = fig.add_subplot(spec[0, 2])

    ax_prop_rtf = ax_prop.twinx()  # twin axis for real-time factor
    ax_prop_rtf.set_position(ax_prop.get_position())

    for ax_tmp in [ax_crea, ax_conn, ax_prop, ax_prop_rtf]:
        ax_tmp.tick_params(axis='both', which='major', labelsize=tk_size)

    # If weak scaling, create twin axes for network size
    if scaling_strength == 'weak':
        ax_crea_twin = ax_crea.twiny()
        ax_crea_twin.set_position(ax_crea.get_position())
        ax_conn_twin = ax_conn.twiny()
        ax_conn_twin.set_position(ax_conn.get_position())
        ax_prop_twin = ax_prop.twiny()
        ax_prop_twin.set_position(ax_prop.get_position())

    #trans = mtransforms.ScaledTranslation(-20 / 72, 7 / 72, fig.dpi_scale_trans)

    # Plot major timer data:
    # network creation time
    # network connection time
    # state propagation time
    for i in range(len(pobjects)):
        pobjects[i].plot_main(quantities=['py_time_create'],
                axis=ax_crea,
                subject=labels[i],
                line_color=colors[i],
                line_style=styles[i],
                linewidth=lw,
                )
        pobjects[i].plot_main(quantities=['py_time_connect'],
                axis=ax_conn,
                subject=labels[i],
                line_color=colors[i],
                line_style=styles[i],
                linewidth=lw,
                )
        pobjects[i].plot_main(quantities=['time_simulate'],
                axis=ax_prop,
                subject=labels[i],
                line_color=colors[i],
                line_style=styles[i],
                linewidth=lw,
                )

    # set xlabels
    ax_crea.set_xlabel(xlabel)
    ax_conn.set_xlabel(xlabel)
    ax_prop.set_xlabel(xlabel)

    # set xtick interval
    ax_crea.xaxis.set_major_locator(ticker.MultipleLocator(base=1))
    ax_conn.xaxis.set_major_locator(ticker.MultipleLocator(base=1))
    ax_prop.xaxis.set_major_locator(ticker.MultipleLocator(base=1))

    # set ylabels
    ax_crea.set_ylabel('Network creation time (s)')
    ax_conn.set_ylabel('Network connection time (s)')
    ax_prop.set_ylabel('State propagation\ntime (s) for '
                   r'$T_{\mathrm{model}} =$'
                   + f'{model_time_in_s:.0f} s')

    # set ylims
    for ax_tmp, ylims, key in zip([ax_crea, ax_conn, ax_prop], [cons_ylims, conn_ylims, prop_ylims], ['py_time_create', 'py_time_connect', 'time_simulate']):
        if isinstance(ylims, tuple):
            ylims_ = ylims
        else:
            data_all = []
            for i in range(len(pobjects)):
                data_i = pobjects[i].df_data[key].values.tolist()
                data_all = data_all + data_i
            ylims_ = (0, max(max(data_all)*1.1, 2*np.mean(data_all)))
        ax_tmp.set_ylim(ylims_)

    # set twin axis for real-time factor
    ax_prop_rtf.set_ylabel('Real-time factor', rotation=270, labelpad=20)
    ax_prop_rtf.set_ylim((ax_prop.get_ylim()[0]/model_time_in_s, ax_prop.get_ylim()[1]/model_time_in_s))

    # if weak scaling, get network size(s) and add to plot
    if scaling_strength == 'weak':
        if 'N_ex' in pobjects[0].df_data and 'N_ex' in pobjects[0].df_data and 'N_in' in pobjects[0].df_data:
            # calculate from recording
            N_size_labels = (pobjects[0].df_data['N_ex'].values + pobjects[0].df_data['N_in'].values + pobjects[0].df_data['N_astro'].values).astype(int)
        else:
            # calculate from network_size (all nodes in NEST) minus one poisson generator
            N_size_labels = pobjects[0].df_data['network_size'].values.astype(int) - 1
        for ax_twin_tmp, ax_tmp in zip([ax_crea_twin, ax_conn_twin, ax_prop_twin], [ax_crea, ax_conn, ax_prop]):
            xticks = sorted(set(pobjects[0].df_data['num_nodes'].values.tolist()))
            xticklabels = [np.format_float_scientific(x, trim='-', exp_digits=1).replace("+", "") for x in N_size_labels]
            ax_twin_tmp.set_xticks(xticks)
            ax_twin_tmp.set_xticklabels(xticklabels, fontsize=tk_size)
            ax_twin_tmp.set_xlim(ax_tmp.get_xlim())
            ax_twin_tmp.set_xlabel('Network size')

    # Save figure
    plt.tight_layout()
    plt.savefig(f'{save_path}/plot_major.png', dpi=400)
    plt.savefig(f'{save_path}/plot_major.eps', format='eps', dpi=400)
    plt.close()

    # Make legend figure
    fig, ax_legend = plt.subplots(figsize=(2, 4))
    for i, label in enumerate(labels):
        if not os.path.isfile(timer_files[i]):
            break
        ax_legend.plot(
            [],
            [],
            label=label.replace(" ", "\n", 1).replace("=", "=\n", 1),
            marker=None,
            color=colors[i],
            linewidth=3,
            linestyle=styles[i],
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

    # Output difference data
    if do_diff:
        os.system(f"mkdir -p {save_path}/diff_abs")
        os.system(f"mkdir -p {save_path}/diff_rel")
        for i, B_i in enumerate(pobjects):
            label_i = labels[i].replace("\n", "")
            B_i.df_data.to_csv(f"{save_path}/df_{label_i}.csv", index=False, float_format="%.3f")
            for j, B_j in enumerate(pobjects):
                if j != i:
                    label_j = labels[j].replace("\n", "")
                    df_i, df_j = B_i.df_data.copy(), B_j.df_data.copy()
                    for key in df_i.columns:
                        if key not in df_j:
                            df_i = df_i.drop(columns=[key])
                    for key in df_j.columns:
                        if key not in df_i:
                            df_j = df_j.drop(columns=[key])
                    df_diff_abs = df_j - df_i
                    df_diff_rel = (df_j - df_i)/df_i
                    df_diff_abs.to_csv(f"{save_path}/diff_abs/df_{label_j}_to_{label_i}.csv", index=False, float_format="%.3f")
                    df_diff_rel.to_csv(f"{save_path}/diff_rel/df_{label_j}_to_{label_i}.csv", index=False, float_format="%.3f")

