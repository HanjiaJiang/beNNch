#!/bin/bash

paths="../outpath/production3/000051"
pathw="../outpath/production3/000052"

cp $paths/plot_major.eps ./plot_major_4rules_strong.eps
cp $pathw/plot_major.eps ./plot_major_4rules_weak.eps
cp $pathw/legend_major.eps ./legend_major_4rules.eps

python makefig_fig7.py
