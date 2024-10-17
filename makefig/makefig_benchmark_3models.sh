#!/bin/bash

paths="../outpath/production1/000001"
pathw="../outpath/production1/000005"

cp $paths/plot_major.eps ./plot_major_strong.eps
cp $pathw/plot_major.eps ./plot_major_weak.eps
cp $paths/plot_phases.eps ./plot_phases_strong.eps
cp $pathw/plot_phases.eps ./plot_phases_weak.eps

cp $paths/legend_major.eps ./legend_major_strong.eps
cp $paths/legend_phases.eps ./legend_phases_strong.eps
cp $pathw/legend_major.eps ./legend_major_weak.eps
cp $pathw/legend_phases.eps ./legend_phases_weak.eps

python makefig_benchmark_3models.py
#python makefig_benchmark.py
