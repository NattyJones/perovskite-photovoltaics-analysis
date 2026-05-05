# Perovskite Photovoltaics Analysis

This repository contains the Python analysis scripts used for my dissertation project on perovskite solar cells for space applications. The project investigates the effect of different interfacial modification and passivation strategies on photovoltaic performance and proton irradiation stability.

The analysis includes J-V curve comparison, EQE analysis, current-time stability, intensity dependence, ideality factor extraction, and remaining factor box plots.

## Project Overview

The devices analysed include PFN-Br and Al2O3-based perovskite solar cell architectures, with additional passivation layers such as EDAI and LiF. The devices were compared before and after proton irradiation to assess radiation tolerance and degradation behaviour.

The main analysis methods include:

- J-V curve comparison before and after irradiation
- External quantum efficiency analysis
- Current-time stability analysis
- Intensity-dependent J-V and Voc analysis
- Ideality factor calculation from Voc vs ln(Intensity)
- Remaining factor analysis for Voc, Jsc, FF, and PCE

## Repository Structure

```text
perovskite-photovoltaics-analysis/
│
├── README.md
├── requirements.txt
│
├── jv_analysis/
│   └── Python scripts for plotting J-V curves before and after irradiation
│
├── eqe_analysis/
│   └── Python scripts for plotting EQE spectra and cumulative photocurrent
│
├── current_time/
│   └── Python scripts for current-time and PCE-time stability analysis
│
├── intensity_analysis/
│   └── Python scripts for intensity-dependent J-V plots, Voc vs ln(Intensity), and ideality factor analysis
│
└── remaining_factor/
    └── Python scripts for remaining factor box plots of Voc, Jsc, FF, and PCE
