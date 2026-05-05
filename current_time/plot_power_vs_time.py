# -*- coding: utf-8 -*-
"""
Plot IT Power Output vs Time
with a consistent y-axis range across all files
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
from glob import glob

# ============================================================
# CHANGE THIS TO YOUR ACTUAL IT FILE FOLDER
# ============================================================

folder_path = r"D:\University\Dissertation\Python Files\ITFiles"

# ============================================================
# OUTPUT FOLDER
# ============================================================

plot_folder = os.path.join(folder_path, "Power_vs_Time_Plots")
os.makedirs(plot_folder, exist_ok=True)

summary_results = []


def read_it_file(file_path):
    with open(file_path, "r", encoding="utf-8", errors="ignore") as file:
        lines = file.readlines()

    output_voltage = None
    data_start_index = None

    for i, line in enumerate(lines):

        # Find output voltage
        if "Output Volt" in line:
            parts = line.strip().split()
            try:
                output_voltage = float(parts[-1])
            except:
                pass

        # Find where the time/current data starts
        if line.strip().startswith("Time(s)"):
            data_start_index = i + 1

    if output_voltage is None:
        raise ValueError("Could not find Output Volt in file.")

    if data_start_index is None:
        raise ValueError("Could not find Time(s) Current(A) table in file.")

    data = []

    for line in lines[data_start_index:]:
        parts = line.strip().split()

        if len(parts) >= 2:
            try:
                time_s = float(parts[0])
                current_a = float(parts[1])
                data.append([time_s, current_a])
            except:
                continue

    if len(data) == 0:
        raise ValueError("No current-time data was extracted.")

    df = pd.DataFrame(data, columns=["Time_s", "Current_A"])

    return output_voltage, df


# ============================================================
# FIND FILES
# ============================================================

txt_files = glob(os.path.join(folder_path, "*.txt")) + glob(os.path.join(folder_path, "*.TXT"))

print("Folder path being used:")
print(folder_path)
print()
print(f"Number of .txt files found: {len(txt_files)}")
print()

if len(txt_files) == 0:
    print("No .txt files were found.")
    print("Check the folder_path.")
else:
    # ========================================================
    # FIRST PASS: READ ALL FILES AND FIND GLOBAL Y-AXIS RANGE
    # ========================================================

    processed_data = []
    global_min_power = float("inf")
    global_max_power = float("-inf")

    for file_path in txt_files:
        try:
            filename = os.path.basename(file_path)
            output_voltage, df = read_it_file(file_path)

            # Convert to power in mW
            df["Power_mW"] = abs(df["Current_A"] * output_voltage) * 1000

            file_min = df["Power_mW"].min()
            file_max = df["Power_mW"].max()

            if file_min < global_min_power:
                global_min_power = file_min
            if file_max > global_max_power:
                global_max_power = file_max

            processed_data.append((filename, output_voltage, df))

        except Exception as e:
            print(f"Error reading {file_path}: {e}")

    if len(processed_data) == 0:
        print("No files were successfully read.")
    else:
        # Add a small padding so the lines don't touch the plot edges
        y_padding = 0.05 * (global_max_power - global_min_power)

        # In case all values are almost identical
        if y_padding == 0:
            y_padding = 0.05

        y_min = global_min_power - y_padding
        y_max = global_max_power + y_padding

        print(f"Consistent y-axis range will be: {y_min:.3f} to {y_max:.3f} mW")
        print()

        # ====================================================
        # SECOND PASS: PLOT ALL FILES WITH SAME Y-AXIS
        # ====================================================

        for filename, output_voltage, df in processed_data:
            try:
                average_power = df["Power_mW"].mean()
                min_power = df["Power_mW"].min()
                max_power = df["Power_mW"].max()

                summary_results.append({
                    "File": filename,
                    "Output Voltage (V)": output_voltage,
                    "Average Power Output (mW)": average_power,
                    "Minimum Power Output (mW)": min_power,
                    "Maximum Power Output (mW)": max_power
                })

                plt.figure(figsize=(6, 4))
                plt.plot(df["Time_s"], df["Power_mW"], linewidth=1.5)

                plt.xlabel("Time (s)")
                plt.ylabel("Power Output (mW)")
                plt.title(filename.replace(".txt", "").replace(".TXT", ""))
                plt.ylim(y_min, y_max)   # <-- consistent y-axis here
                plt.grid(True, linestyle="--", alpha=0.35)
                plt.tight_layout()

                output_plot_path = os.path.join(
                    plot_folder,
                    filename.replace(".txt", "_Power_vs_Time.png").replace(".TXT", "_Power_vs_Time.png")
                )

                plt.savefig(output_plot_path, dpi=300)
                plt.close()

                print(f"Saved plot: {output_plot_path}")
                print(f"Average power: {average_power:.3f} mW")
                print()

            except Exception as e:
                print(f"Error plotting {filename}: {e}")

# ============================================================
# SAVE SUMMARY
# ============================================================

if len(summary_results) > 0:
    summary_df = pd.DataFrame(summary_results)
    summary_excel_path = os.path.join(folder_path, "Power_vs_Time_Summary.xlsx")
    summary_df.to_excel(summary_excel_path, index=False)

    print("Done.")
    print(f"Summary saved to: {summary_excel_path}")
    print(f"Plots saved in: {plot_folder}")
else:
    print("No files were successfully processed, so no summary Excel file was created.")