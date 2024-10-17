#!/bin/bash

paths="../outpath/production1/000013"
pathw="../outpath/production1/000017"

cp $paths/plot_major.eps ./plot_major_4rules_strong.eps
cp $pathw/plot_major.eps ./plot_major_4rules_weak.eps
cp $pathw/legend_major.eps ./legend_major_4rules.eps

python makefig_benchmark_4rules.py
