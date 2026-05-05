# perovskite-photovoltaicss-analysis
All Python code used for Dissertation: 'Perovskite Photovoltaics for Space'

This repository contains the Python scripts used for data processing and analysis in my dissertation project on proton-irradiated perovskite solar cells.

## Contents

- `jv_analysis/` - scripts for extracting photovoltaic parameters from J-V data and calculating remaining factors.
- `intensity_analysis/` - scripts for intensity-dependent J-V analysis and Ideality factor calculation.
- `eqe_analysis/` - scripts for plotting EQE spectra and integrated photocurrent.
- `stability_analysis/` - scripts for converting current-time measurements into PCE-time plots.

## Requirements

The scripts require Python 3 and the following packages:

- pandas
- numpy
- matplotlib
- scipy
- openpyxl

Install requirements using:

```bash
pip install -r requirements.txt
