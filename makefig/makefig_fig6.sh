#!/bin/bash

paths="../analysis/results_Sparse_Synchronous_Surrogate_x_strong"
pathw="../analysis/results_Sparse_Synchronous_Surrogate_x_weak"

cp $paths/plot_major.eps ./plot_major_strong.eps
cp $pathw/plot_major.eps ./plot_major_weak.eps
cp $paths/plot_phases.eps ./plot_phases_strong.eps
cp $pathw/plot_phases.eps ./plot_phases_weak.eps

cp $paths/legend_major.eps ./legend_major_strong.eps
cp $paths/legend_phases.eps ./legend_phases_strong.eps
cp $pathw/legend_major.eps ./legend_major_weak.eps
cp $pathw/legend_phases.eps ./legend_phases_weak.eps

python makefig_fig6.py

rm master_figure.* plot*.eps legend*.eps
