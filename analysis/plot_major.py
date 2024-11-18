import os

import numpy as np
import bennchplot as bp
from matplotlib import pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.transforms as mtransforms
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
         colors=['k', 'k', 'gray', 'gray'],
         styles=['-', ':', '-', ':'],
         lw=3,
         tk_size='small',
    ):

    print('plotting major timer data ...')

    x_axis = x_axis if x_axis == 'num_nvp' else 'num_nodes'
    if x_axis == 'num_nvp':
        xlabel = 'Number of VPs'
    else:
        xlabel = 'Number of\ncompute nodes'

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

    # Plotting
    widths = [1, 1, 1]
    heights = [1]
    fig = plt.figure(figsize=(8, 4))
    spec = gridspec.GridSpec(ncols=3, nrows=1, figure=fig, width_ratios=widths, height_ratios=heights)

    ax_cons = fig.add_subplot(spec[0, 0])
    ax_conn = fig.add_subplot(spec[0, 1])
    ax_prop = fig.add_subplot(spec[0, 2])

    ax_prop_rtf = ax_prop.twinx()
    ax_prop_rtf.set_position(ax_prop.get_position())

    for ax_tmp in [ax_cons, ax_conn, ax_prop, ax_prop_rtf]:
        ax_tmp.tick_params(axis='both', which='major', labelsize=tk_size)

    if scaling_strength == 'weak':
        ax_cons_twin = ax_cons.twiny() # top axis for network_size
        ax_cons_twin.set_position(ax_cons.get_position())
        ax_conn_twin = ax_conn.twiny() # top axis for network_size
        ax_conn_twin.set_position(ax_conn.get_position())
        ax_prop_twin = ax_prop.twiny() # top axis for network_size
        ax_prop_twin.set_position(ax_prop.get_position())

    trans = mtransforms.ScaledTranslation(-20 / 72, 7 / 72, fig.dpi_scale_trans)

    # Network construction
    for i in range(len(pobjects)):
        pobjects[i].plot_main(quantities=['py_time_create'],
                axis=ax_cons,
                subject=labels[i],
                line_color=colors[i],
                linewidth=lw,
                line_style=styles[i])
        pobjects[i].plot_main(quantities=['py_time_connect'],
                axis=ax_conn,
                subject=labels[i],
                line_color=colors[i],
                linewidth=lw,
                line_style=styles[i])
        pobjects[i].plot_main(quantities=['time_simulate'],
                axis=ax_prop,
                subject=labels[i],
                line_color=colors[i],
                linewidth=lw,
                line_style=styles[i])

    ax_cons.set_ylabel('Network creation time (s)')
    ax_conn.set_ylabel('Network connection time (s)')
    ax_prop.set_ylabel('State propagation\ntime (s) for '
                   r'$T_{\mathrm{model}} =$'
                   + f'{np.unique(pobjects[0].df_data.model_time_sim.values)[0]:.0f} s')

    ax_cons.set_xlabel(xlabel)
    ax_conn.set_xlabel(xlabel)
    ax_prop.set_xlabel(xlabel)

    ax_cons.xaxis.set_major_locator(ticker.MultipleLocator(base=1))
    ax_conn.xaxis.set_major_locator(ticker.MultipleLocator(base=1))
    ax_prop.xaxis.set_major_locator(ticker.MultipleLocator(base=1))

    # set ylims
    for ax_tmp, ylims, key in zip([ax_cons, ax_conn, ax_prop], [cons_ylims, conn_ylims, prop_ylims], ['py_time_create', 'py_time_connect', 'time_simulate']):
        if isinstance(ylims, tuple):
            ylims_ = ylims
        else:
            data_all = []
            for i in range(len(pobjects)):
                data_i = pobjects[i].df_data[key].values.tolist()
                data_all = data_all + data_i
            ylims_ = (0, max(max(data_all)*1.1, 2*np.mean(data_all)))
        ax_tmp.set_ylim(ylims_)

    ax_prop_rtf.set_ylim((ax_prop.get_ylim()[0]/model_time_in_s, ax_prop.get_ylim()[1]/model_time_in_s))
    ax_prop_rtf.set_ylabel('Real-time factor', rotation=270, labelpad=20)

    # get network size(s) and add to plot
    if 'N_ex' in pobjects[0].df_data and 'N_ex' in pobjects[0].df_data and 'N_in' in pobjects[0].df_data:
        # calculate from recording
        N_size_labels = (pobjects[0].df_data['N_ex'].values + pobjects[0].df_data['N_in'].values + pobjects[0].df_data['N_astro'].values).astype(int)
    else:
        # calculate from network_size (all nodes in NEST) minus one poisson generator
        N_size_labels = pobjects[0].df_data['network_size'].values.astype(int) - 1
    if scaling_strength == 'weak':
        for ax_twin_tmp, ax_tmp in zip([ax_cons_twin, ax_conn_twin, ax_prop_twin], [ax_cons, ax_conn, ax_prop]):
            xticks = sorted(set(pobjects[0].df_data['num_nodes'].values.tolist()))
            xticklabels = [np.format_float_scientific(x, trim='-', exp_digits=1).replace("+", "") for x in N_size_labels]
            ax_twin_tmp.set_xticks(xticks)
            ax_twin_tmp.set_xticklabels(xticklabels, fontsize=tk_size)
            ax_twin_tmp.set_xlim(ax_tmp.get_xlim())
            ax_twin_tmp.set_xlabel('Network size')

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

def plot_conn_fr(
         timer_files,
         save_path,
         scaling_strength,
         x_axis='num_nodes',
         conn_ylims=(0, None),
         fr_ylims=(0, None),
         colors=['k', 'k', 'gray', 'gray'],
         styles=['-', ':', '-', ':'],
    ):

    x_axis = x_axis if x_axis == 'num_nvp' else 'num_nodes'

    pobjects = []
    for i, timer_file in enumerate(timer_files):
        if not os.path.isfile(timer_file):
            break
        args = {'data_file': timer_file, 'x_axis': [x_axis], 'time_scaling': 1e3}
        B = bp.Plot(**args)
        pobjects.append(B)

    # Plotting
    widths = [1]
    heights = [1, 1]
    fig = plt.figure(figsize=(3, 8))
    spec = gridspec.GridSpec(ncols=1, nrows=2, figure=fig, width_ratios=widths, height_ratios=heights)

    ax_conn = fig.add_subplot(spec[0, 0])
    ax_fr = fig.add_subplot(spec[1, 0])

    if scaling_strength == 'weak':
        ax_conn_twin = ax_conn.twiny() # top axis for network_size

    if x_axis == 'num_nvp':
        xlabel = 'Number of VPs'
    else:
        xlabel = 'Number of\ncompute nodes'

    trans = mtransforms.ScaledTranslation(-20 / 72, 7 / 72, fig.dpi_scale_trans)

    # Network conntruction
    lw = 2
    for i in range(len(pobjects)):
        pobjects[i].plot_main(quantities=['tsodyks_synapse'],
                axis=ax_conn,
                subject='tsodyks_synapse',
                line_color=colors[i],
                linewidth=lw,
                line_style=styles[i])
        pobjects[i].plot_main(quantities=['average_firing_rate'],
                axis=ax_fr,
                subject='average_firing_rate',
                line_color=colors[i],
                linewidth=lw,
                line_style=styles[i])

    ax_conn.set_ylabel('Number of\ntsodyks_synapse')
    ax_fr.set_ylabel('Mean neuronal\nfiring rate')

    ax_fr.set_xlabel(xlabel)

    ax_conn.set_ylim(conn_ylims)
    ax_fr.set_ylim(fr_ylims)

    # get network size(s) and add to plot
    if 'N_ex' in pobjects[0].df_data and 'N_ex' in pobjects[0].df_data and 'N_in' in pobjects[0].df_data:
        # calculate from recording
        N_size_labels = (pobjects[0].df_data['N_ex'].values + pobjects[0].df_data['N_in'].values + pobjects[0].df_data['N_astro'].values).astype(int)
    else:
        # calculate from network_size (all nodes in NEST) minus one poisson generator
        N_size_labels = pobjects[0].df_data['network_size'].values.astype(int) - 1
    if scaling_strength == 'weak':
        xticks = sorted(set(pobjects[0].df_data['num_nodes'].values.tolist()))
        ax_conn_twin.set_xticks(xticks)
        xticklabels = [np.format_float_scientific(x, trim='-', exp_digits=1).replace("+", "") for x in N_size_labels]
        ax_conn_twin.set_xticklabels(xticklabels, fontsize='small')
        ax_conn_twin.set_xlabel('Network size\n(number of cells)')
        ax_conn_twin.set_xlim(ax_conn.get_xlim())

    plt.tight_layout()
    plt.savefig(f'{save_path}/plot_conn_fr.png', dpi=400)
    plt.savefig(f'{save_path}/plot_conn_fr.eps', format='eps', dpi=400)
    plt.close()
