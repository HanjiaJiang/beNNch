#!/bin/bash

pathm="../models/astrocyte/makefig_benchmark_model"

cp $pathm/*.eps .

python makefig_fig3.py

rm master_figure.* benchmark_model_*.eps
