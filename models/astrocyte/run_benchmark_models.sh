#!/bin/bash

declare -a arr=("Sparse" "Synchronous")

for x in "${arr[@]}"
do
  echo "Running $x model ..."
  python run_benchmark_model.py "$x" $1
done

python plots.py
python makefig_benchmark_model.py
