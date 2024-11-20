#!/bin/bash

pathw="../analysis/results_poolsize=10_poolsize=100_poolsize=1000_poolsize=10000_weak"

cp $pathw/plot_major.eps ./plot_major_weak.eps
cp $pathw/legend_major.eps ./legend_major_weak.eps
cp $pathw/plot_phases.eps ./plot_phases_weak.eps
cp $pathw/legend_phases.eps ./legend_phases_weak.eps

python makefig_fig8.py

rm master_figure.* plot*.eps legend*.eps
