#!/bin/bash

paths="../outpath/production/000004"
pathw="../outpath/production/000012"

cp $paths/plot_major.eps ./plot_major_4rules_strong.eps
cp $pathw/plot_major.eps ./plot_major_4rules_weak.eps
cp $pathw/legend_major.eps ./legend_major_4rules.eps

python makefig_4rules.py
