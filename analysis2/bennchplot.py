"""
beNNch-plot - standardized plotting routines for performance benchmarks.
Copyright (C) 2021 Forschungszentrum Juelich GmbH, INM-6

This program is free software: you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation, either version 3 of the License, or (at your option) any later
version.
This program is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
PARTICULAR PURPOSE. See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with
this program. If not, see <https://www.gnu.org/licenses/>.

SPDX-License-Identifier: GPL-3.0-or-later
"""

"""
Class for benchmarking plots
"""
import pandas as pd
import matplotlib
from matplotlib import pyplot as plt
from matplotlib import gridspec
import numpy as np
import yaml
import os
try:
    from . import plot_params as pp
except ImportError:
    import plot_params as pp


class Plot():
    """
    Class organizing benchmarking plots.

    Attributes
    ----------
    x_axis : str or list
        variable to be plotted on x-axis
    x_ticks : str, optional

    data_file : str, optional
        path to data
    matplotlib_params : dict, optional
        parameters passed to matplotlib
    color_params : dict, optional
        unique colors for variables
    additional_params : dict, optional
        additional parameters used for plotting
    label_params : dict, optional
        labels used when plotting
    time_scaling : int, optional
        scaling parameter for simulation time
   """

    def __init__(self, x_axis,
                 x_ticks='data',
                 data_file='/path/to/data',
                 matplotlib_params=pp.matplotlib_params,
                 color_params=pp.color_params,
                 additional_params=pp.additional_params,
                 label_params=pp.label_params,
                 time_scaling=1,
                 ctrl_file=None,
                 construct_timer="Python"):

        self.x_axis = x_axis
        self.x_ticks = x_ticks
        self.matplotlib_params = matplotlib_params
        self.additional_params = additional_params
        self.color_params = color_params
        self.label_params = label_params
        self.time_scaling = time_scaling
        self.df_data = None
        self.df_ctrl = None
        self.construct_timer = construct_timer

        self.load_data(data_file)
        if isinstance(ctrl_file, str):
            self.load_data(ctrl_file, control=True)
        self.compute_derived_quantities()
        if isinstance(ctrl_file, str):
            self.compute_derived_quantities(control=True)

    def load_data(self, data_file, control=False):
        """
        Load data to dataframe, to be used later when plotting.

        Group the data by specified operations.

        Attributes
        ----------
        data_file : str
            data file to be loaded and later plotted

        Raises
        ------
        ValueError
        """
        print(f'Loading {data_file} ...')
        try:
            df = pd.read_csv(data_file, delimiter=',')
        except FileNotFoundError:
            print('File could not be found')
            quit()

        for py_timer in ['py_time_create', 'py_time_connect']:
            if py_timer not in df:
                df[py_timer] = np.nan
                raise ValueError('Warning! Python timers are not found. ' +
                                 'Construction time measurements will not ' +
                                 'be accurate.')
        dict_ = {'num_nodes': 'first',
                 'threads_per_task': 'first',
                 'tasks_per_node': 'first',
                 'model_time_sim': 'first',
                 'time_construction_create': ['mean', 'std'],
                 'time_construction_connect': ['mean', 'std'],
                 'time_simulate': ['mean', 'std'],
                 'py_time_create': ['mean', 'std'],
                 'py_time_connect': ['mean', 'std'],
                 'network_size': 'first',
                 'N_ex': 'first',
                 'N_in': 'first',
                 'N_astro': 'first',
                 'num_connections': ['mean', 'std'],
                 'local_spike_counter': ['mean', 'std'],
                 'tsodyks_synapse': ['mean', 'std'],
                 'sic_connection': ['mean', 'std'],
                 }

        col = ['num_nodes', 'threads_per_task', 'tasks_per_node',
               'model_time_sim', 'time_construction_create',
               'time_construction_create_std', 'time_construction_connect',
               'time_construction_connect', 'time_simulate',
               'time_simulate_std',
               'py_time_create', 'py_time_create_std',
               'py_time_connect', 'py_time_connect_std',
               'network_size',
               'N_ex',
               'N_in',
               'N_astro',
               'num_connections', 'num_connections_std',
               'local_spike_counter', 'local_spike_counter_std',
               'tsodyks_synapse', 'tsodyks_synapse_std',
               'sic_connection', 'sic_connection_std',
               ]

        # Timers for connection building in TripartiteConnect()
        detailed_timers = [
            'time_collocate_spike_data',
            'time_communicate_spike_data',
            'time_deliver_spike_data',
            'time_update',
            'time_deliver_secondary_data',
            'time_gather_secondary_data',
            'time_communicate_target_data',
            'time_gather_spike_data',
            'time_gather_target_data',
            'time_communicate_prepare',
            'time_construction_connect_third_inner_count',
            'time_construction_connect_third_inner_max',
            'time_construction_connect_third_inner_fill',
            'time_construction_connect_third_inner_communicate',
            'time_construction_connect_third_inner_connect',
            'time_synchronize',
        ]
        for timer in detailed_timers:
            if timer in df.columns:
                dict_.update({timer: ['mean', 'std']})
                col.append(timer)
                col.append(timer+'_std')

        df = df.drop('rng_seed', axis=1).groupby(
            ['num_nodes',
             'threads_per_task',
             'tasks_per_node',
             'model_time_sim'], as_index=False).agg(dict_)
        df.columns = col
        if control:
            self.df_ctrl = df.copy()
        else:
            self.df_data = df.copy()

    def compute_derived_quantities(self, control=False):
        """
        Do computations to get parameters needed for plotting.
        """
        if control:
            df = self.df_ctrl
        else:
            df = self.df_data
        df['num_nvp'] = (
            df['threads_per_task'] * df['tasks_per_node']
        )
        df['model_time_sim'] /= self.time_scaling
        if self.construct_timer == "C++":
            df['time_construct'] = (df['time_construction_create'] + df['time_construction_connect'])
            df['time_construct_std'] = (np.sqrt((df['time_construction_create_std']**2 + df['time_construction_connect_std']**2)))
        else:
            df['time_construct'] = (df['py_time_create'] + df['py_time_connect'])
            df['time_construct_std'] = (np.sqrt((df['py_time_create']**2 + df['py_time_connect']**2)))
        df['sim_factor'] = (df['time_simulate'] / df['model_time_sim'])
        df['sim_factor_std'] = (df['time_simulate_std'] / df['model_time_sim'])

        df['time_addup'] = (
            df['time_update'] +
            df['time_communicate_spike_data'] +
            df['time_deliver_spike_data'] +
            df['time_collocate_spike_data'] +
            df['time_deliver_secondary_data'] +
            df['time_gather_secondary_data']
        )
        df['time_addup_std'] = \
            np.sqrt(
            df['time_update_std']**2 +
            df['time_communicate_spike_data_std']**2 +
            df['time_deliver_spike_data_std']**2 +
            df['time_collocate_spike_data_std']**2 +
            df['time_deliver_secondary_data_std']**2 +
            df['time_gather_secondary_data_std']**2
        )
        df['time_addup_factor'] = (
            df['time_addup'] /
            df['model_time_sim'])
        df['time_addup_std_factor'] = (
            df['time_addup_std'] /
            df['model_time_sim'])

        # calculate phases and their fractions, using model_time_sim (model time) and time_simulate (wall time)
        phases = [
            'time_update',
            'time_communicate_spike_data',
            'time_deliver_spike_data',
            'time_collocate_spike_data',
            'time_deliver_secondary_data',
            'time_gather_secondary_data',
        ]
        for phase in phases:
            df[phase + '_factor'] = (df[phase] / df['model_time_sim'])
            df[phase + '_frac'] = (100 * df[phase] / df['time_simulate'])

        # spike CCD = collocate + communicate + deliver
        df['spike_ccd_factor'] = (
            df['time_communicate_spike_data_factor'] +
            df['time_deliver_spike_data_factor'] +
            df['time_collocate_spike_data_factor'])
        df['spike_ccd_frac'] = (
            df['time_communicate_spike_data_frac'] +
            df['time_deliver_spike_data_frac'] +
            df['time_collocate_spike_data_frac'])

        # secondary event (gather and deliver)
        df['secondary_gd_factor'] = (
            df['time_deliver_secondary_data_factor'] +
            df['time_gather_secondary_data_factor'])
        df['secondary_gd_frac'] = (
            df['time_deliver_secondary_data_frac'] +
            df['time_gather_secondary_data_frac']
        )

        # others = the rest
        df['others_factor'] = (df['time_simulate'] - df['time_addup'])/df['model_time_sim']
        df['others_frac'] = 100 * (df['time_simulate'] - df['time_addup']) / df['time_simulate']

        # total spike count
        df['total_spike_count_per_s'] = (df['local_spike_counter'] / df['model_time_sim'])
        df['total_spike_count_per_s_std'] = (df['local_spike_counter_std'] / df['model_time_sim'])

        # average firing rate
        if 'N_ex' in df.columns and 'N_in' in df.columns:
            print('N_ex and N_in in df. Use them to calculate firing rate.')
            df['average_firing_rate'] = df['total_spike_count_per_s']/(df['N_ex'] + df['N_in'])
            df['average_firing_rate_std'] = df['total_spike_count_per_s_std']/(df['N_ex'] + df['N_in'])
        else:
            print('N_ex or N_in not in df!')
            df['average_firing_rate'] = df['total_spike_count_per_s']/((df['network_size']-1)/2) # minus 1 Poisson generator
            df['average_firing_rate_std'] = df['total_spike_count_per_s_std']/((df['network_size']-1)/2)

    def plot_fractions(self, axis, fill_variables,
                       interpolate=False, step=None, log=False, alpha=1.,
                       error=False, control=False, line=False, subject=None, ylims=None):
        """
        Fill area between curves.

        axis : Matplotlib axes object
        fill_variables : list
            variables (e.g. timers) to be plotted as fill  between graph and
            x axis
        interpolate : bool, default
            whether to interpolate between the curves
        step : {'pre', 'post', 'mid'}, optional
            should the filling be a step function
        log : bool, default
            whether the x-axes should have logarithmic scale
        alpha, int, default
            alpha value of fill_between plot
        error : bool
            whether plot should have error bars
        """
        if control:
            df = self.df_ctrl
        else:
            df = self.df_data

        fill_height = 0
        for i, fill in enumerate(fill_variables):
            main_label = subject if isinstance(subject, str) else None
            main_label = main_label if fill == fill_variables[-1] else None
            line_color = 'dimgray' if control else 'k'
            try:
                frac_label = self.label_params[fill]
                if isinstance(subject, str):
                    frac_label += f' ({subject})'
                axis.fill_between(np.squeeze(df[self.x_axis]),
                                  fill_height,
                                  np.squeeze(df[fill]) + fill_height,
                                  label=frac_label,
                                  facecolor=self.color_params[fill],
                                  interpolate=interpolate,
                                  step=step,
                                  alpha=alpha,
                                  linewidth=0.5,
                                  edgecolor='#444444')
            except:
                print("fill_between() failed!")
            if error:
                axis.errorbar(np.squeeze(df[self.x_axis]),
                              np.squeeze(df[fill]) + fill_height,
                              yerr=np.squeeze(df[fill + '_std']),
                              capsize=3,
                              capthick=1,
                              color=line_color,
                              fmt='none',
                              label=main_label
                              )
            fill_height += df[fill].to_numpy()

        if self.x_ticks == 'data':
            try:
                axis.set_xticks(np.squeeze(df[self.x_axis]))
            except:
                print("set_xticks() failed!")
        else:
            axis.set_xticks(self.x_ticks)

        if isinstance(ylims, tuple):
            axis.set_ylim(ylims)

        if log:
            axis.set_xscale('log')
            axis.tick_params(bottom=False, which='minor')
            axis.get_xaxis().set_major_formatter(
                matplotlib.ticker.ScalarFormatter())

    def plot_main(self, quantities, axis, log=(False, False),
                  error_only=False, fmt='none', control=False, subject=None, line_color=None, ylims=None, linewidth=1.5, linestyle=None):
        """
        Main plotting function.

        Attributes
        ----------
        quantities : list
            list with plotting quantities
        axis : axis object
            axis object used when plotting
        log : tuple of bools, default
            whether x and y axis should have logarithmic scale
        error : bool, default
            whether or not to plot error bars
        fmt : string
            matplotlib format string (fmt) for defining line style
        """
        if control:
            df = self.df_ctrl
        else:
            df = self.df_data

        for y in quantities:
            if y not in df:
                continue
            line_style = ':' if control else '-'
            line_style = linestyle if isinstance(linestyle, str) else line_style
            line_color = self.color_params[y] if line_color is None else line_color
            label = subject if isinstance(subject, str) else self.label_params[y]
            if not error_only:
                axis.plot(df[self.x_axis],
                          df[y],
                          marker='.',
                          markersize=10.0,
                          color=line_color,
                          linewidth=linewidth,
                          linestyle=line_style,
                          label=label)
            axis.errorbar(
                df[self.x_axis].values,
                df[y].values,
                yerr=df[y + '_std'].values,
                marker=None,
                capsize=3,
                capthick=1.5,
                linewidth=linewidth,
#                label=label,
                color=line_color,
                fmt=fmt)

#        if self.x_ticks == 'data':
#           axis.set_xticks(df[self.x_axis].values)
#        else:
#           axis.set_xticks(self.x_ticks)

        if isinstance(ylims, tuple):
            axis.set_ylim(ylims)

        if log[0]:
            axis.set_xscale('log')
        if log[1]:
            axis.tick_params(bottom=False, which='minor')
            axis.set_yscale('log')

    def merge_legends(self, ax1, ax2):
        """
        Merge legends from two axes, display them in the first

        Attributes
        ----------
        ax1 : axes object
            first axis
        ax2 : axes object
            second axis
        """
        handles, labels = [(a + b) for a, b in zip(
            ax2.get_legend_handles_labels(),
            ax1.get_legend_handles_labels())]
        ax1.legend(handles, labels, loc='upper right')

    def simple_axis(self, ax):
        """
        Remove top and right spines.

        Attributes
        ----------
        ax : axes object
            axes object for which to adjust spines
        """
        # Hide the right and top spines
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)

        # Only show ticks on the left and bottom spines
        ax.yaxis.set_ticks_position('left')
        ax.xaxis.set_ticks_position('bottom')
