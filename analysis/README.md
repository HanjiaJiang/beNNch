# Benchmark data analysis and plotting

This folder contains the code for benchmark data analysis and plotting. To run the code, execute `bash run_analysis.sh`. It runs the main Python script [plot.py](./plot.py) for each set of benchmark to analyze and plot the data. The generated folders will be named results_fig# and contain the results (in results.txt) and figures (Fig 6 to 8 in the article). The required benchmark data are already available in [outpath](../outpath/).

| file | description |
|-------------------|-------------------|
| [run_analysis.sh](./run_analysis.sh)    | runs plot.py for each set of benchmark |
| [plot.py](./plot.py)    | is the main script for analysis and plotting |
| [plot_major.py](./plot_major.py)    | analyzes and plots the major benchmark data, i.e., network creation time, network connections time, state propagation time |
| [plot_phases.py](./plot_phases.py)    | analyzes and plots the phases of state propagation, i.e., update, spike CCD, SIC GD, other |
| [bennchplot.py](./bennchplot.py)    | contains the core plotting functions |
| [plot_params.py](./plot_params.py)    | contains the plotting parameters  |
| [tol_colors.py](./tol_colors.py)    | defines colors for plotting |
