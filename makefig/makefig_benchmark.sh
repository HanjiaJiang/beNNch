#!/bin/bash

pathm="../models/astrocyte/makefig_benchmark_model"

cp $pathm/*.eps .

python makefig_fig3.py

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

paths="../analysis/results_Bernoulli_Fixedindegree_Fixedoutdegree_Fixedtotalnumber_strong"
pathw="../analysis/results_Bernoulli_Fixedindegree_Fixedoutdegree_Fixedtotalnumber_weak"

cp $paths/plot_major.eps ./plot_major_4rules_strong.eps
cp $pathw/plot_major.eps ./plot_major_4rules_weak.eps
cp $pathw/legend_major.eps ./legend_major_4rules.eps

python makefig_fig7.py

pathw="../analysis/results_poolsize=10_poolsize=100_poolsize=1000_poolsize=10000_weak"

cp $pathw/plot_major.eps ./plot_major_weak.eps
cp $pathw/legend_major.eps ./legend_major_weak.eps
cp $pathw/plot_phases.eps ./plot_phases_weak.eps
cp $pathw/legend_phases.eps ./legend_phases_weak.eps

python makefig_fig8.py

rm master_figure.* plot*.eps legend*.eps benchmark_model_*.eps
