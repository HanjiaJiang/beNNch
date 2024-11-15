#!/bin/bash

dpath=../outpath/production1/0000$1

convert $dpath/plot_major.png $dpath/legend_major.png +append $dpath/combine_major.png
convert $dpath/plot_phases.png $dpath/legend_phases.png +append $dpath/combine_phases.png
convert $dpath/plot_separate_rtf.png $dpath/legend_separate_rtf.png +append $dpath/combine_separate_rtf.png
convert $dpath/plot_separate_memory.png $dpath/legend_separate_memory.png +append $dpath/combine_separate_memory.png
convert $dpath/plot_separate_memory-diff.png $dpath/legend_separate_memory-diff.png +append $dpath/combine_separate_memory-diff.png

convert $dpath/combine_major.png $dpath/combine_phases.png +append $dpath/combine_all.png
