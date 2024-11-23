#!/bin/bash

declare -a arr=("Sparse" "Synchronous")

echo "Number of CPU cores available?"
read n_core

for x in "${arr[@]}"
do
  echo "Running the \"$x\" model ..."
  if [ -z "$n_core" ]; then
    python run_benchmark_model.py "$x" $n_core
  else
    echo "Number of CPU cores is not given and will be determined automatically."
    python run_benchmark_model.py "$x"
  fi
done

python plots.py
