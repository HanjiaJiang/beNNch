#!/bin/bash

if [ ! -d ../outpath/astrocyte ]; then
  unzip ../outpath/astrocyte.zip -d ../outpath
else
  echo "../outpath/astrocyte already there."
fi

python plot.py 1 2 3 99 Sparse Synchronous Surrogate x
python plot.py 4 5 6 99 Sparse Synchronous Surrogate x
python plot.py 1 7 8 9 Bernoulli "Fixed in-degree" "Fixed out-degree" "Fixed total-number"
python plot.py 4 10 11 12 Bernoulli "Fixed in-degree" "Fixed out-degree" "Fixed total-number"
python plot.py 4 16 17 18 pool_size=10 pool_size=100 pool_size=1000 pool_size=10000

mv results_Sparse_Synchronous_Surrogate_x_strong results_fig6a
mv results_Sparse_Synchronous_Surrogate_x_weak results_fig6b
mv results_Bernoulli_Fixedindegree_Fixedoutdegree_Fixedtotalnumber_strong results_fig7a
mv results_Bernoulli_Fixedindegree_Fixedoutdegree_Fixedtotalnumber_weak results_fig7b
mv results_poolsize=10_poolsize=100_poolsize=1000_poolsize=10000_weak results_fig8
