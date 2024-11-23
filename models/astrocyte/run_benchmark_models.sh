#!/bin/bash

declare -a arr=("Sparse" "Synchronous")

echo "Number of CPU cores available?"
read n_core

for x in "${arr[@]}"
do
  echo "Running the \"$x\" model ..."
  python run_benchmark_model.py "$x"
done

python plots.py
