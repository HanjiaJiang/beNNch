# JUBE benchmark script

This folder contains the JUBE benchmark script [astrocyte_benchmark.yaml](./astrocyte_benchmark.yaml) to run benchmarks with. This script specifies the model, the output path, the benchmark parameters, and the quantities recorded in the benchmark. The benchmark parameters are imported from the .yaml scripts in the [config](../config/) and [helpers](../helpers/) folder. To run benchmarks, specify parameters in these .yaml scripts and execute `jube run astrocyte_benchmark.yaml`.

The sets of benchmarks presented in the article and their specific parameters are listed below. These parameters can be specified in the script [config/astrocyte_benchmark_config.yaml](../config/astrocyte_benchmark_config.yaml). This script also includes the other parameters that are the same for all benchmarks.

## Benchmarks with neuron-astrocyte networks models (Fig 6)
- scaling_type = "strong", model_name = ["Sparse", "Synchronous", "Surrogate"], astro_pool_size = 10
- scaling_type = "weak", model_name = ["Sparse", "Synchronous", "Surrogate"], astro_pool_size = 10

## Benchmarks with different primary (neuron-to-neuron) connectivity (Fig 7)
- scaling_type = "strong", model_name = ["Bernoulli", "Fixed-indegree", "Fixed-outdegree", "Fixed-total-number"], astro_pool_size = 10
- scaling_type = "weak", model_name = ["Bernoulli", "Fixed-indegree", "Fixed-outdegree", "Fixed-total-number"], astro_pool_size = 10

## Weak scaling benchmarks with different astrocyte pool sizes (Fig 8)
- scaling_type = "weak", model_name = "Bernoulli", astro_pool_size = [10, 100, 1000, 10000]


