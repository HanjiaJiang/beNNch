#!/bin/bash

pathm="../models/astrocyte/results_fig3"

cp $pathm/*.eps .

python makefig_fig3.py

paths="../analysis/results_fig6a"
pathw="../analysis/results_fig6b"

cp $paths/plot_major.eps ./plot_major_strong.eps
cp $pathw/plot_major.eps ./plot_major_weak.eps
cp $paths/plot_phases.eps ./plot_phases_strong.eps
cp $pathw/plot_phases.eps ./plot_phases_weak.eps

cp $paths/legend_major.eps ./legend_major_strong.eps
cp $paths/legend_phases.eps ./legend_phases_strong.eps
cp $pathw/legend_major.eps ./legend_major_weak.eps
cp $pathw/legend_phases.eps ./legend_phases_weak.eps

python makefig_fig6.py

paths="../analysis/results_fig7a"
pathw="../analysis/results_fig7b"

cp $paths/plot_major.eps ./plot_major_4rules_strong.eps
cp $pathw/plot_major.eps ./plot_major_4rules_weak.eps
cp $pathw/legend_major.eps ./legend_major_4rules.eps

python makefig_fig7.py

pathw="../analysis/results_fig8"

cp $pathw/plot_major.eps ./plot_major_weak.eps
cp $pathw/legend_major.eps ./legend_major_weak.eps
cp $pathw/plot_phases.eps ./plot_phases_weak.eps
cp $pathw/legend_phases.eps ./legend_phases_weak.eps

python makefig_fig8.py

rm master_figure.* plot*.eps legend*.eps benchmark_model_*.eps
