#!/bin/bash

################################################################################
# This script uses the included Python code to run single simulations of two
# benchmark models, "Sparse" and "Synchronous", and show the results.
################################################################################

# Define models
declare -a arr=("Sparse" "Synchronous")

# Run simulations
for x in "${arr[@]}"
do
  echo "Running the \"$x\" model ..."
  python run_benchmark_model.py "$x"
done

# Create plots to show results
python plots.py
