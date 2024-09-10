#!/bin/bash

dpath=../outpath/production/0000$1

convert $dpath/plot_major.png $dpath/legend_major.png +append $dpath/combine_major.png
convert $dpath/plot_phases.png $dpath/legend_phases.png +append $dpath/combine_phases.png
