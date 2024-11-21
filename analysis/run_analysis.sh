#!/bin/bash

if [ ! -d ../outpath/astrocyte ]; then
  unzip ../outpath/astrocyte.zip -d ../outpath
else
  echo "../outpath/astrocyte already there."
fi

#id_arr=()
#for i in {1..21}; do
#  id_arr+=("$i")
#done
#python analysis.py "${id_arr[@]}"

python plot.py 1 2 3 99 Sparse Synchronous Surrogate x
python plot.py 4 5 6 99 Sparse Synchronous Surrogate x
python plot.py 1 7 8 9 Bernoulli "Fixed in-degree" "Fixed out-degree" "Fixed total-number"
python plot.py 4 10 11 12 Bernoulli "Fixed in-degree" "Fixed out-degree" "Fixed total-number"
python plot.py 4 16 17 18 pool_size=10 pool_size=100 pool_size=1000 pool_size=10000
