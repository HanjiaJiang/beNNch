#!/bin/bash

pathw="../outpath/production1/000052"

cp $pathw/plot_major.eps ./plot_major_weak.eps
cp $pathw/plot_phases.eps ./plot_phases_weak.eps

cp $pathw/legend_major.eps ./legend_major_weak.eps
cp $pathw/legend_phases.eps ./legend_phases_weak.eps

python makefig_benchmark_poolsize.py
