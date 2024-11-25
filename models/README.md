# Benchmark models

This folder contains the code that implements benchmark models. The benchmark models used in the article are implemented in the subfolder [astrocyte](./astrocyte). For the approach to run benchmarks, see [benchmarks](../benchmarks). For single simulations that illustrate the dynamics of the benchmark models (Fig 3 in the article), go to the subfolder [astrocyte](./astrocyte) and run `bash run_benchmark_models.sh`. The results and plots will be saved in a folder named results_fig3.


The scripts in the subfolder [astrocyte](./astrocyte) are listed below.

| file | description |
|-------------------|-------------------|
| [astrocyte_benchmark.py](./astrocyte/astrocyte_benchmark.py)    | code for running astrocyte benchmarks under beNNch |
| [network.py](./astrocyte/network.py)    | code for building neuron-astrocyte networks for benchmarks; used by [astrocyte_benchmark.py](./astrocyte/astrocyte_benchmark.py) and [run_benchmark_model.py](./astrocyte/run_benchmark_model.py) |
| [plots.py](./astrocyte/plots.py)    | code for plotting benchmark model dynamics |
| [run_benchmark_model.py](./astrocyte/run_benchmark_model.py)    | code for single simulations of benchmark models |
| [run_benchmark_models.sh](./astrocyte/run_benchmark_models.sh)    | uses [run_benchmark_model.py](./astrocyte/run_benchmark_model.py) and [plots.py](./astrocyte/plots.py) to run single simulations of two benchmark models ("Sparse" and "Synchronous") and plot the data |
