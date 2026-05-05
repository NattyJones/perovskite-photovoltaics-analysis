# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import linregress
import re
import os
from glob import glob

# === SETTINGS ===
folder_path = r"D:\University\Dissertation\Python Files\IntensityFiles\Post"  # change this
output_excel = os.path.join(folder_path, "ideality_factors_reverse_only.xlsx")
plot_folder = os.path.join(folder_path, "new_plots_reverse_only")

SCAN_DIRECTION = "Reverse"   # keep this as Reverse
THERMAL_VOLTAGE = 0.02585    # kT/q at room temperature, in volts

os.makedirs(plot_folder, exist_ok=True)

results = []


def extract_intensity(label):
    """
    Extracts the light intensity from labels like:
    intensity (intensity.CH_Ref(0.9 SUN).Reverse(1))
    """
    match = re.search(r"CH_Ref\(([\d.]+)\s*SUN\)", str(label))
    return float(match.group(1)) if match else None


def extract_scan_direction(label):
    """
    Extracts Forward or Reverse from the label.
    """
    match = re.search(r"\.(Forward|Reverse)\(", str(label))
    return match.group(1) if match else None


for file_path in glob(os.path.join(folder_path, "*.csv")):
    try:
        df = pd.read_csv(file_path, header=None)

        header_rows = df.index[df.iloc[:, 0].astype(str).str.strip().eq("Name")].tolist()

        if not header_rows:
            print(f"Skipping {file_path}: Could not find summary table header row.")
            continue

        header_row = header_rows[0]

        data = df.iloc[header_row + 1:, [0, 3]].copy()
        data.columns = ["Label", "Voc"]

        data = data.dropna(subset=["Label", "Voc"])

        data["Intensity"] = data["Label"].apply(extract_intensity)
        data["Scan"] = data["Label"].apply(extract_scan_direction)

        data["Voc"] = pd.to_numeric(data["Voc"], errors="coerce")
        data = data.dropna(subset=["Intensity", "Scan", "Voc"])

        data = data[data["Scan"] == SCAN_DIRECTION].copy()

        if data.empty:
            print(f"Skipping {file_path}: No {SCAN_DIRECTION} scan data found.")
            continue

        data = data.sort_values("Intensity")

        data["ln_Intensity"] = np.log(data["Intensity"])

        slope, intercept, r_value, p_value, std_err = linregress(
            data["ln_Intensity"],
            data["Voc"]
        )

        ideality_factor = slope / THERMAL_VOLTAGE
        r_squared = r_value ** 2

        filename = os.path.splitext(os.path.basename(file_path))[0]
        plot_path = os.path.join(plot_folder, f"{filename}_Reverse_Voc_vs_lnIntensity.png")

        plt.figure(figsize=(6, 4))

        plt.plot(
            data["ln_Intensity"],
            data["Voc"],
            "o",
            label="Reverse scan data"
        )

        plt.plot(
            data["ln_Intensity"],
            intercept + slope * data["ln_Intensity"],
            "-",
            label=f"Fit: slope={slope:.4f} V, n={ideality_factor:.2f}, R²={r_squared:.3f}"
        )

        plt.xlabel("ln(Intensity)")
        plt.ylabel("Voc (V)")
        plt.title(f"{filename} - Reverse Scan Voc vs ln(Intensity)")
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.savefig(plot_path, dpi=300)
        plt.close()

        results.append({
            "File": os.path.basename(file_path),
            "Scan Direction Used": SCAN_DIRECTION,
            "Number of Points Used": len(data),
            "Slope (V)": slope,
            "Ideality Factor n": ideality_factor,
            "Intercept (V)": intercept,
            "R²": r_squared,
            "Std Error": std_err
        })

    except Exception as e:
        print(f"Error processing {file_path}: {e}")


# === EXPORT RESULTS ===
result_df = pd.DataFrame(results)
result_df.to_excel(output_excel, index=False)

print(f"\nProcessed {len(results)} files.")
print(f"Ideality factors saved to: {output_excel}")
print(f"Plots saved in: {plot_folder}")