#!/bin/bash

################################################################################
# This script runs the analysis and plotting for the benchmark data in the
# article "Modeling neuron-astrocyte interactions in neural networks using
# distributed simulation.
################################################################################

# Unzip the benchmark data if necessary
if [ ! -d ../outpath/astrocyte ]; then
  unzip ../outpath/astrocyte.zip -d ../outpath
else
  echo "../outpath/astrocyte already there."
fi

# Run data analysis and plotting
python plot.py 1 2 3 99 Sparse Synchronous Surrogate x
python plot.py 4 5 6 99 Sparse Synchronous Surrogate x
python plot.py 1 7 8 9 Bernoulli "Fixed in-degree" "Fixed out-degree" "Fixed total-number"
python plot.py 4 10 11 12 Bernoulli "Fixed in-degree" "Fixed out-degree" "Fixed total-number"
python plot.py 4 16 17 18 pool_size=10 pool_size=100 pool_size=1000 pool_size=10000

# Change result folder names
rsync -au results_Sparse_Synchronous_Surrogate_x_strong/ results_fig6a
rsync -au results_Sparse_Synchronous_Surrogate_x_weak/ results_fig6b
rsync -au results_Bernoulli_Fixedindegree_Fixedoutdegree_Fixedtotalnumber_strong/ results_fig7a
rsync -au results_Bernoulli_Fixedindegree_Fixedoutdegree_Fixedtotalnumber_weak/ results_fig7b
rsync -au results_poolsize=10_poolsize=100_poolsize=1000_poolsize=10000_weak/ results_fig8
rm -r results_Sparse_Synchronous_Surrogate_x_strong
rm -r results_Sparse_Synchronous_Surrogate_x_weak
rm -r results_Bernoulli_Fixedindegree_Fixedoutdegree_Fixedtotalnumber_strong
rm -r results_Bernoulli_Fixedindegree_Fixedoutdegree_Fixedtotalnumber_weak
rm -r results_poolsize=10_poolsize=100_poolsize=1000_poolsize=10000_weak
