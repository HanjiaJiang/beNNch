import os

import numpy as np
import bennchplot as bp
from matplotlib import pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.ticker as ticker

def plot_major(
         timer_files,
         labels,
         save_path,
         scaling_strength,
         x_axis='num_nodes',
         colors=None,
         styles=None,
         tklb_size='small',
         do_diff=True,
    ):

    # Set plot items
    plot_keys = ['py_time_create', 'py_time_connect', 'time_simulate']

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
            model_time_in_s = B.df_data['model_time_sim'][0]

    # Create figure and axes
    # figure
    widths = [1, 1, 1]
    heights = [1]
    fig = plt.figure(figsize=(8, 4))
    spec = gridspec.GridSpec(ncols=3, nrows=1, figure=fig, width_ratios=widths, height_ratios=heights)

    # axes
    ax_crea = fig.add_subplot(spec[0, 0])
    ax_conn = fig.add_subplot(spec[0, 1])
    ax_prop = fig.add_subplot(spec[0, 2])
    axes = [ax_crea, ax_conn, ax_prop]

    # twin axis for real-time factor of state propagation
    ax_prop_rtf = ax_prop.twinx()
    ax_prop_rtf.set_position(ax_prop.get_position())

    # Plot major timer data:
    # network creation time
    # network connection time
    # state propagation time
    for i in range(len(pobjects)):
        pobjects[i].plot_main(quantities=['py_time_create'],
                axis=ax_crea,
                line_color=colors[i],
                line_style=styles[i],
                )
        pobjects[i].plot_main(quantities=['py_time_connect'],
                axis=ax_conn,
                line_color=colors[i],
                line_style=styles[i],
                )
        pobjects[i].plot_main(quantities=['time_simulate'],
                axis=ax_prop,
                line_color=colors[i],
                line_style=styles[i],
                )

    # set label tick parameters
    for ax_tmp in axes + [ax_prop_rtf]:
        ax_tmp.tick_params(axis='both', which='major', labelsize=tklb_size)

    # set xtick interval
    ax_crea.xaxis.set_major_locator(ticker.MultipleLocator(1))
    ax_conn.xaxis.set_major_locator(ticker.MultipleLocator(1))
    ax_prop.xaxis.set_major_locator(ticker.MultipleLocator(1))

    # set xlabels
    ax_crea.set_xlabel(xlabel)
    ax_conn.set_xlabel(xlabel)
    ax_prop.set_xlabel(xlabel)

    # set ylabels
    ax_crea.set_ylabel('Network creation time (s)')
    ax_conn.set_ylabel('Network connection time (s)')
    ax_prop.set_ylabel('State propagation\ntime (s) for '
                   r'$T_{\mathrm{model}} =$'
                   + f'{model_time_in_s:.0f} s')

    # set ylims
    for ax_tmp, key in zip(axes, plot_keys):
        data_all = []
        for i in range(len(pobjects)):
            data_i = pobjects[i].df_data[key].values.tolist()
            data_all = data_all + data_i
        ylims = (0, max(max(data_all)*1.1, 2*np.mean(data_all)))
        ax_tmp.set_ylim(ylims)

    # set label and ylims for twin of ax_prop
    ax_prop_rtf.set_ylabel('Real-time factor', rotation=270, labelpad=20)
    ylims_get = ax_prop.get_ylim()
    ax_prop_rtf.set_ylim((ylims_get[0]/model_time_in_s, ylims_get[1]/model_time_in_s))

    # if weak scaling, create twin axes for network size
    if scaling_strength == 'weak':
        ax_crea_twin = ax_crea.twiny()
        ax_crea_twin.set_position(ax_crea.get_position())
        ax_conn_twin = ax_conn.twiny()
        ax_conn_twin.set_position(ax_conn.get_position())
        ax_prop_twin = ax_prop.twiny()
        ax_prop_twin.set_position(ax_prop.get_position())
        # get network size and add to top axis
        df_tmp = pobjects[0].df_data
        assert 'N_ex' in df_tmp and 'N_in' in df_tmp, 'plot_major(): N_ex or N_in not in data!'
        N_sizes = (df_tmp['N_ex'].values + df_tmp['N_in'].values + df_tmp['N_astro'].values).astype(int)
        for ax_twin_tmp, ax_tmp in zip([ax_crea_twin, ax_conn_twin, ax_prop_twin], axes):
            xticks = sorted(set(df_tmp['num_nodes'].values.tolist()))
            xticklabels = [np.format_float_scientific(x, trim='-', exp_digits=1).replace('+', '') for x in N_sizes]
            ax_twin_tmp.set_xticks(xticks)
            ax_twin_tmp.set_xticklabels(xticklabels, fontsize=tklb_size)
            ax_twin_tmp.set_xlim(ax_tmp.get_xlim())
            ax_twin_tmp.set_xlabel('Network size')

    # Save figure
    plt.tight_layout()
    plt.savefig(f'{save_path}/plot_major.png', dpi=400)
    plt.savefig(f'{save_path}/plot_major.eps', format='eps', dpi=400)
    plt.close()

    # Make legend (separate image file)
    fig, ax_legend = plt.subplots(figsize=(2, 4))
    for i, label in enumerate(labels):
        if not os.path.isfile(timer_files[i]):
            break
        ax_legend.plot(
            [],
            [],
            label=label.replace(' ', '\n', 1).replace('=', '=\n', 1),
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
        os.system(f'mkdir -p {save_path}/diff_abs')
        os.system(f'mkdir -p {save_path}/diff_rel')
        output_str = f'Results of {scaling_strength} scaling, one to four compute nodes:\n'
        for i, B_i in enumerate(pobjects):
            label_i = labels[i].replace(' ', '').replace('-', '').replace('_', '')
            B_i.df_data.to_csv(f'{save_path}/df_{label_i}.csv', index=False, float_format='%.3f')
            output_str += f'\nMean neuronal firing rate, \'{labels[i]}\' model:\n'
            diff_fr = B_i.df_data['average_firing_rate'].values
            for a, diff in enumerate(diff_fr):
                output_str += f'{diff:.2f} spikes/s (number of nodes = {a+1})\n'
        for i, B_i in enumerate(pobjects):
            label_i = labels[i].replace(' ', '').replace('-', '').replace('_', '')
            for j, B_j in enumerate(pobjects):
                if j != i:
                    label_j = labels[j].replace(' ', '').replace('-', '').replace('_', '')
                    df_i, df_j = B_i.df_data, B_j.df_data
                    df_diff_abs = df_j - df_i
                    df_diff_rel = (df_j - df_i)/df_i
                    df_diff_abs.to_csv(f'{save_path}/diff_abs/df_{label_j}_vs_{label_i}.csv', index=False, float_format='%.3f')
                    df_diff_rel.to_csv(f'{save_path}/diff_rel/df_{label_j}_vs_{label_i}.csv', index=False, float_format='%.3f')
                    output_str += f'\nDifference in (1) state propagation time and (2) \'update\' time, \'{labels[j]}\' vs. \'{labels[i]}\':\n'
                    diff_simulate = df_diff_rel['time_simulate'].values*100
                    diff_update = df_diff_rel['time_update'].values*100
                    for a, (diff1, diff2) in enumerate(zip(diff_simulate, diff_update)):
                        output_str += f'(1) {diff1:.1f} % (2) {diff2:.1f} %  (number of nodes = {a+1})\n'
        print(output_str)
        with open(f'{save_path}/results.txt', 'w') as f:
            f.write(output_str)
