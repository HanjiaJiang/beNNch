#!/bin/bash

pathw="../outpath/production3/000053"
pathconn="../models/astrocyte2"

scale=2

cp $pathw/plot_major.eps ./plot_major_weak.eps
cp $pathw/legend_major.eps ./legend_major_weak.eps

cp $pathconn/bernoulli10_$scale/conn_num_distr_a2n.eps ./conn_num_distr_a2n_10.eps
cp $pathconn/bernoulli10_$scale/conn_target_distr_a2n.eps ./conn_target_distr_a2n_10.eps
cp $pathconn/bernoulli10_$scale/conn_source_distr_a2n.eps ./conn_source_distr_a2n_10.eps

cp $pathconn/bernoulli100_$scale/conn_num_distr_a2n.eps ./conn_num_distr_a2n_100.eps
cp $pathconn/bernoulli100_$scale/conn_target_distr_a2n.eps ./conn_target_distr_a2n_100.eps
cp $pathconn/bernoulli100_$scale/conn_source_distr_a2n.eps ./conn_source_distr_a2n_100.eps

cp $pathconn/bernoulli1000_$scale/conn_num_distr_a2n.eps ./conn_num_distr_a2n_1000.eps
cp $pathconn/bernoulli1000_$scale/conn_target_distr_a2n.eps ./conn_target_distr_a2n_1000.eps
cp $pathconn/bernoulli1000_$scale/conn_source_distr_a2n.eps ./conn_source_distr_a2n_1000.eps

cp $pathconn/bernoulli10000_$scale/conn_num_distr_a2n.eps ./conn_num_distr_a2n_10000.eps
cp $pathconn/bernoulli10000_$scale/conn_target_distr_a2n.eps ./conn_target_distr_a2n_10000.eps
cp $pathconn/bernoulli10000_$scale/conn_source_distr_a2n.eps ./conn_source_distr_a2n_10000.eps

python makefig_benchmark_poolsize.py
