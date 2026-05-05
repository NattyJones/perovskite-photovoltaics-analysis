# Perovskite Photovoltaics Analysis

This repository contains the Python scripts used for data processing, plotting, and analysis in my dissertation project:

**Perovskite Photovoltaics for Space**

The project investigates the effect of different interfacial modification and passivation strategies on the photovoltaic performance and proton irradiation stability of perovskite solar cells.

The analysis includes J-V curve comparison, EQE analysis, current-time stability analysis, intensity dependence analysis, Ideality factor calculation, and remaining factor analysis.

## Repository Structure

The code is organised using separate GitHub branches for each type of analysis.

| Branch | Description |
|---|---|
| `main` | Main repository branch containing the README and general project information. |
| `jv_analysis` | Contains Python scripts used to plot and compare J-V curves before and after irradiation. |
| `intensity_analysis` | Contains Python scripts for intensity-dependent J-V plots, open-circuit voltage against ln(Intensity), Ideality factor calculation, and Ideality factor comparison plots. |
| `current_time` | Contains Python scripts used for current-time or PCE-time stability analysis after irradiation. |
| `remaining_factor` | Contains Python scripts used to calculate and plot remaining performance factors for Voc, Jsc, fill factor, and PCE. |
| `eqe_analysis` | Contains Python scripts used to plot external quantum efficiency spectra and cumulative photocurrent. |

## Analysis Included

### J-V Analysis

The J-V analysis scripts compare the current density-voltage behaviour of selected devices before and after proton irradiation. These scripts were used to assess changes in open-circuit voltage, short-circuit current density, fill factor, and overall curve shape.

### Intensity Dependence and Ideality Factor Analysis

The intensity analysis scripts process measurements taken at different illumination intensities. Open-circuit voltage is plotted against ln(Intensity), allowing Ideality factors to be calculated from the fitted gradient. These values were used to compare recombination behaviour before and after irradiation.

### EQE Analysis

The EQE analysis scripts plot external quantum efficiency spectra and cumulative photocurrent. This was used to assess whether changes in device performance were linked to optical absorption or photocurrent generation losses.

### Current-Time Stability Analysis

The current-time scripts analyse short-term device stability under illumination after irradiation. These plots were used to compare how different configurations maintained power conversion efficiency over time.

### Remaining Factor Analysis

The remaining factor scripts calculate and plot the retention of key photovoltaic parameters after irradiation. This includes remaining factors for:

- Open-circuit voltage, Voc
- Short-circuit current density, Jsc
- Fill factor, FF
- Power conversion efficiency, PCE

## Requirements

The scripts require Python 3 and the following packages:

```bash
pip install pandas numpy matplotlib scipy openpyxl
