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
import os

import pandas as pd
import matplotlib
import numpy as np

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
    color_params : dict, optional
        unique colors for variables
    label_params : dict, optional
        labels used when plotting
    time_scaling : int, optional
        scaling parameter for simulation time
   """

    def __init__(self, x_axis,
                 x_ticks='data',
                 data_file='/path/to/data',
                 color_params=pp.color_params,
                 label_params=pp.label_params,
                 time_scaling=1):

        self.x_axis = x_axis
        self.x_ticks = x_ticks
        self.color_params = color_params
        self.label_params = label_params
        self.time_scaling = time_scaling
        self.df_data = None

        self.load_data(data_file)
        self.compute_derived_quantities()

    def load_data(self, data_file):
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
        assert os.path.isfile(data_file), 'File could not be found'
        df = pd.read_csv(data_file, delimiter=',')

        # Set items for major timer data
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
                 'num_connections': ['mean', 'std'],
                 'local_spike_counter': ['mean', 'std'],
                 }

        col = ['num_nodes', 'threads_per_task', 'tasks_per_node',
               'model_time_sim', 'time_construction_create',
               'time_construction_create_std', 'time_construction_connect',
               'time_construction_connect_std', 'time_simulate',
               'time_simulate_std',
               'py_time_create', 'py_time_create_std',
               'py_time_connect', 'py_time_connect_std',
               'network_size',
               'num_connections', 'num_connections_std',
               'local_spike_counter', 'local_spike_counter_std',
               ]

        # Set items for numbers of cells
        N_recorders = ['N_ex', 'N_in', 'N_astro']
        for N_recorder in N_recorders:
            if N_recorder in df.columns:
                dict_.update({N_recorder: 'first'})
                col.append(N_recorder)

        # Set items for detailed timer data
        detailed_timers = [
            'time_update',
            'time_collocate_spike_data',
            'time_communicate_spike_data',
            'time_deliver_spike_data',
            'time_gather_secondary_data',
            'time_deliver_secondary_data',
            'time_communicate_target_data',
            'time_gather_spike_data',
            'time_gather_target_data',
            'time_communicate_prepare',
            'base_memory',
            'node_memory',
            'network_memory',
            'init_memory',
            'total_memory',
        ]
        for timer in detailed_timers:
            if timer in df.columns:
                dict_.update({timer: ['mean', 'std']})
                col.append(timer)
                col.append(timer+'_std')

        # Use the raw data to calculate group means and standard deviations
        df = df.drop('rng_seed', axis=1).groupby(
            ['num_nodes',
             'threads_per_task',
             'tasks_per_node',
             'model_time_sim'], as_index=False).agg(dict_)

        # Keep data in object
        df.columns = col
        self.df_data = df

    def compute_derived_quantities(self):
        """
        Do computations to get parameters needed for plotting.
        """
        df = self.df_data
        df['num_nvp'] = (df['threads_per_task'] * df['tasks_per_node'])
        df['model_time_sim'] /= self.time_scaling
        df['sim_factor'] = (df['time_simulate'] / df['model_time_sim'])
        df['sim_factor_std'] = (df['time_simulate_std'] / df['model_time_sim'])

        # Item that adds up all known phases
        # This is for calculating the 'other' phase
        df['time_addup'] = (
            df['time_update'] +
            df['time_collocate_spike_data'] +
            df['time_communicate_spike_data'] +
            df['time_deliver_spike_data'] +
            df['time_gather_secondary_data'] +
            df['time_deliver_secondary_data']
        )
        df['time_addup_std'] = \
            np.sqrt(
            df['time_update_std']**2 +
            df['time_collocate_spike_data_std']**2 +
            df['time_communicate_spike_data_std']**2 +
            df['time_deliver_spike_data_std']**2 +
            df['time_gather_secondary_data_std']**2 +
            df['time_deliver_secondary_data_std']**2
        )
        df['time_addup_factor'] = (
            df['time_addup'] /
            df['model_time_sim'])
        df['time_addup_std_factor'] = (
            df['time_addup_std'] /
            df['model_time_sim'])

        # Calculate phases and their fractions
        # model_time_sim (model time) and time_simulate (wall time) are needed
        phases = [
            'time_update',
            'time_collocate_spike_data',
            'time_communicate_spike_data',
            'time_deliver_spike_data',
            'time_gather_secondary_data',
            'time_deliver_secondary_data',
        ]
        for phase in phases:
            df[phase + '_factor'] = df[phase] / df['model_time_sim']
            df[phase + '_frac'] = 100 * df[phase] / df['time_simulate']

        # spike CCD = collocate + communicate + deliver
        df['spike_ccd_factor'] = (
            df['time_collocate_spike_data_factor'] +
            df['time_communicate_spike_data_factor'] +
            df['time_deliver_spike_data_factor']
        )
        df['spike_ccd_frac'] = (
            df['time_collocate_spike_data_frac'] +
            df['time_communicate_spike_data_frac'] +
            df['time_deliver_spike_data_frac']
        )

        # secondary GD = gather + deliver
        df['secondary_gd_factor'] = (
            df['time_gather_secondary_data_factor'] +
            df['time_deliver_secondary_data_factor']
        )
        df['secondary_gd_frac'] = (
            df['time_gather_secondary_data_frac'] +
            df['time_deliver_secondary_data_frac']
        )

        # others = the rest
        df['others_factor'] = (df['time_simulate'] - df['time_addup']) / df['model_time_sim']
        df['others_frac'] = 100 * (df['time_simulate'] - df['time_addup']) / df['time_simulate']

        # total spike count per second
        df['total_spike_count_per_s'] = (df['local_spike_counter'] / df['model_time_sim'])
        df['total_spike_count_per_s_std'] = (df['local_spike_counter_std'] / df['model_time_sim'])

        # average firing rate
        if 'N_ex' in df.columns and 'N_in' in df.columns:
            df['average_firing_rate'] = df['total_spike_count_per_s'] / (df['N_ex'] + df['N_in'])
            df['average_firing_rate_std'] = df['total_spike_count_per_s_std'] / (df['N_ex'] + df['N_in'])

        if 'base_memory' in df and 'network_memory' in df and 'init_memory' in df and 'total_memory' in df:
            df['memory_network_minus_base'] = df['network_memory'] - df['base_memory']
            df['memory_init_minus_network'] = df['init_memory'] - df['network_memory']
            df['memory_total_minus_init'] = df['total_memory'] - df['init_memory']

    def plot_fractions(self, axis, fill_variables,
                       interpolate=False, step=None, alpha=1.,
                       error=False):
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
        alpha, int, default
            alpha value of fill_between plot
        error : bool
            whether plot should have error bars
        """
        df = self.df_data

        fill_height = 0
        for i, fill in enumerate(fill_variables):
            line_color = 'k'
            axis.fill_between(np.squeeze(df[self.x_axis]),
                              fill_height,
                              np.squeeze(df[fill]) + fill_height,
                              facecolor=self.color_params[fill],
                              interpolate=interpolate,
                              step=step,
                              alpha=alpha,
                              linewidth=0.5,
                              edgecolor='#444444')
            # for error bars
            if error and fill + '_std' in df:
                axis.errorbar(np.squeeze(df[self.x_axis]),
                              np.squeeze(df[fill]) + fill_height,
                              yerr=np.squeeze(df[fill + '_std']),
                              capsize=3,
                              capthick=1,
                              color=line_color,
                              fmt='none',
                              )
            fill_height += df[fill].to_numpy()

        # Set xticks according to data or user input
        if self.x_ticks == 'data':
            try:
                axis.set_xticks(np.squeeze(df[self.x_axis]))
            except:
                print("set_xticks() failed!")
        else:
            axis.set_xticks(self.x_ticks)

    def plot_main(self, quantities, axis,
                  line_color=None, line_style=None, linewidth=3,
                  markersize=10.0, alpha=1.0
                  ):
        """
        Main plotting function.

        Attributes
        ----------
        quantities : list
            list with plotting quantities
        axis : axis object
            axis object used when plotting
        error : bool, default
            whether or not to plot error bars
        """
        df = self.df_data

        for i, y in enumerate(quantities):
            if y not in df:
                continue
            axis.plot(df[self.x_axis].values,
                      df[y].values,
                      marker='.',
                      markersize=markersize,
                      color=line_color,
                      linewidth=linewidth,
                      linestyle=line_style,
                      alpha=alpha)
            # for error bars
            str_std = y + '_std'
            if str_std in df:
                axis.errorbar(
                    df[self.x_axis].values,
                    df[y].values,
                    yerr=df[y + '_std'].values,
                    marker=None,
                    color=line_color,
                    linewidth=0.5*linewidth,
                    linestyle='none',  # line is not needed in this case
                    capsize=linewidth,
                    capthick=0.5*linewidth,
                    alpha=alpha)
            else:                
                print(f'plot_main(): {str_std} not in data!')
