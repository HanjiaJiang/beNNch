# The benchmark code for the NEST astrocyte support

This code implements the benchmark workflow for the NEST astrocyte support developed in [NEST simulator](https://nest-simulator.readthedocs.io/en/latest/index.html). This development of NEST astrocyte support is described in the article [Modeling neuron-astrocyte interactions in neural networks using distributed simulation](https://doi.org/10.1101/2024.11.11.622953). This code also reproduces the figures of benchmark data in the article. Please cite the article if you use this code.

This code is adapted from [beNNch](https://github.com/INM-6/beNNch) ([Albers et al., 2022](https://doi.org/10.3389/fninf.2022.837549)), a software framework for reproducible benchmarks of neuronal network simulations. beNNch is built around the [JUBE benchmarking environment](https://github.com/FZJ-JSC/JUBE) ([Breuer et al., 2024](https://zenodo.org/records/11394333), [Lührs et al., 2016](https://doi.org/10.3233/978-1-61499-621-7-431)).

Author: Han-Jia Jiang hjiang2@smail.uni-koeln.de

## Structure

| directory | description |
|-------------------|-------------------|
| [analysis](./analysis/)    | code for running data analysis and plotting |
| [benchmarks](./benchmarks/)    | code for running benchmarks |
| [config](./config/)    | benchmark configurations |
| [helpers](./helpers/)    | helper functions for running benchmarks and data collection |
| [models](./models/)    | benchmark models; neuron-astrocyte network models used for benchmarks |
| [outpath](./outpath/) | path where benchmark data are saved |

## How to run

### benchmarks
- edit [config/astrocyte_benchmark_config.yaml](./config/astrocyte_benchmark_config.yaml) to specify benchmark parameters
- go to the [benchmarks](./benchmarks/) folder and execute `jube run astrocyte_benchmark.yml`

### create figures
- go to the [analysis](./analysis/) folder and execute `bash run_analysis.sh` to run analysis and create figures

## Software dependencies

### benchmarks
- Python
- [NEST](https://nest-simulator.readthedocs.io/en/latest/index.html) (≥ 3.8)
- [JUBE](https://github.com/FZJ-JSC/JUBE) (≥ 2.6.1)
- [Astrocyte Surrogate Module](https://github.com/heplesser/astrocyte-surrogate-module) (a NEST extension module)

### data analysis and figures
- Python
- numpy
- pandas
- matplotlib

## License

GNU General Public License v3.0 (GPL-3.0)

## Acknowledgments

This project has received funding from the European Union's Horizon 2020 Framework Programme for Research and Innovation under Specific Grant Agreement No. 945539 (Human Brain Project SGA3), from its Partnering Project (AstroNeuronNets), from the European Union's Horizon Europe Programme under the Specific Grant Agreement No. 101147319 (EBRAINS 2.0 Project), from HiRSE_PS, the Helmholtz Platform for Research Software Engineering - Preparatory Study, an innovation pool project of the Helmholtz Association. Open access publication funded by the Deutsche Forschungsgemeinschaft (DFG, German Research Foundation) – 491111487.
