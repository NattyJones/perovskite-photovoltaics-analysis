# -*- coding: utf-8 -*-
"""
EQE + Cumulative Photocurrent Plotter
Compares before and after irradiation EQE scans.

The cumulative photocurrent curve is scaled so that the final value matches
the integrated photocurrent reported inside the EQE Excel file.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os


# ============================================================
# USER INPUT SECTION
# ============================================================

before_file = r"D:\University\Dissertation\Python Files\EQE Files\BEFORE\RB3653_WP0008_D44_P2_2nd scan_use this.xlsx"
after_file  = r"D:\University\Dissertation\Python Files\EQE Files\AFTER\WP0008_E152_D44_P2_scan 1.xlsx"

output_folder = r"D:\University\Dissertation\Python Files\Graphs\EQE\Output"

title_before = "D44 P2 Before Irradiation"
title_after = "D44 P2 Post-Irradiation"

save_figures = True


# ============================================================
# FUNCTIONS
# ============================================================

def read_eqe_file(file_path):
    """
    Reads EQE Excel file.
    Extracts:
    - wavelength
    - EQE
    - final integrated photocurrent from bottom of file
    """

    df_raw = pd.read_excel(file_path, header=None)

    # Convert first two columns to numeric where possible
    wavelength = pd.to_numeric(df_raw.iloc[:, 0], errors="coerce")
    eqe = pd.to_numeric(df_raw.iloc[:, 1], errors="coerce")

    # Keep only real EQE spectral data
    # This removes header rows and bottom metadata rows such as R1, R2, MEASUREMENTS, etc.
    mask = (
        wavelength.notna()
        & eqe.notna()
        & (wavelength >= 250)
        & (wavelength <= 1200)
        & (eqe >= 0)
    )

    wavelength = wavelength[mask].to_numpy(dtype=float)
    eqe = eqe[mask].to_numpy(dtype=float)

    # Sort by wavelength just in case
    sort_idx = np.argsort(wavelength)
    wavelength = wavelength[sort_idx]
    eqe = eqe[sort_idx]

    # Extract integrated photocurrent value from bottom of file
    integrated_jsc = None

    for i in range(len(df_raw)):
        label = str(df_raw.iloc[i, 0]).lower()

        if "jsc" in label or "integral" in label:
            value = pd.to_numeric(df_raw.iloc[i, 1], errors="coerce")
            if pd.notna(value):
                integrated_jsc = float(value)
                break

    if integrated_jsc is None:
        print(f"⚠️ Could not find integrated photocurrent in: {file_path}")
        print("The cumulative photocurrent will be normalised to 1 instead.")
        integrated_jsc = 1.0

    return wavelength, eqe, integrated_jsc


def calculate_cumulative_photocurrent(wavelength, eqe, final_jsc):
    """
    Creates a cumulative photocurrent curve.

    Since the EQE file already provides the final integrated photocurrent,
    the cumulative shape is estimated from EQE × wavelength and then scaled
    to end at the measured integrated photocurrent value.
    """

    # Convert EQE from % to fraction
    eqe_fraction = eqe / 100

    # Approximate contribution weighting
    contribution = eqe_fraction * wavelength

    # Cumulative trapezoidal integration
    cumulative = np.zeros_like(wavelength, dtype=float)

    for i in range(1, len(wavelength)):
        dx = wavelength[i] - wavelength[i - 1]
        area = 0.5 * (contribution[i] + contribution[i - 1]) * dx
        cumulative[i] = cumulative[i - 1] + area

    # Scale so final value equals measured integrated Jsc from file
    if cumulative[-1] != 0:
        cumulative = cumulative / cumulative[-1] * final_jsc

    return cumulative


def plot_eqe_with_photocurrent(file_path, plot_title, output_name):
    wavelength, eqe, final_jsc = read_eqe_file(file_path)
    cumulative_jsc = calculate_cumulative_photocurrent(wavelength, eqe, final_jsc)

    fig, ax1 = plt.subplots(figsize=(9, 6))

    # EQE axis
    ax1.plot(wavelength, eqe, color="tab:blue", linewidth=2)
    ax1.set_xlabel("Wavelength (nm)", fontsize=13)
    ax1.set_ylabel("External Quantum Efficiency (%)", color="tab:blue", fontsize=13)
    ax1.tick_params(axis="y", labelcolor="tab:blue")
    ax1.set_xlim(300, 1100)
    ax1.set_ylim(0, 100)
    ax1.grid(False)

    # Cumulative photocurrent axis
    ax2 = ax1.twinx()
    ax2.plot(wavelength, cumulative_jsc, color="tab:red", linestyle="--", linewidth=2)
    ax2.set_ylabel("Cumulative Photocurrent from EQE (mA cm$^{-2}$)", color="tab:red", fontsize=13)
    ax2.tick_params(axis="y", labelcolor="tab:red")

    # Make the right axis sensible
    ax2.set_ylim(0, max(25, final_jsc * 1.1))

    plt.title(plot_title, fontsize=15)
    plt.tight_layout()

    if save_figures:
        os.makedirs(output_folder, exist_ok=True)
        save_path = os.path.join(output_folder, output_name)
        plt.savefig(save_path, dpi=300, bbox_inches="tight")
        print(f"✅ Saved: {save_path}")

    print(f"{plot_title}: Final integrated photocurrent = {final_jsc:.2f} mA cm⁻²")

    plt.show()


# ============================================================
# RUN
# ============================================================

plot_eqe_with_photocurrent(
    before_file,
    title_before,
    "EQE_before_irradiation.png"
)

plot_eqe_with_photocurrent(
    after_file,
    title_after,
    "EQE_post_irradiation.png"
)
