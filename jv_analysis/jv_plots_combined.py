import matplotlib.pyplot as plt

import pandas as pd

import sys


# -----------------------------

# File paths

# -----------------------------

folder = r"D:\University\Dissertation\Python Files\Graphs\JV\CSVFiles\Al2O3"

fname_before = "WP0008_LT00798_NJ00471_D3_P2_Before.csv"

fname_after = "WP0008_LT00798_NJ00471_D03_P2_After.csv"

path_before = f"{folder}/{fname_before}"

path_after = f"{folder}/{fname_after}"


# -----------------------------

# Function to load reverse sweep

# -----------------------------

def load_reverse_sweep(file_path):

    try:

        data = pd.read_csv(file_path)

    except FileNotFoundError:

        print(f"Error: File '{file_path}' not found.")

        sys.exit(1)


    volt_cols = []

    j_cols = []

    for col in data.columns:

        if 'Volt (V)' in str(data[col].iloc[0]):

            volt_cols.append(col)

        elif '[J (mA/cm^2)]' in str(data[col].iloc[0]):

            j_cols.append(col)

    if len(volt_cols) == 0 or len(j_cols) == 0:

        print("Error: Voltage or current columns not found.")

        sys.exit(1)


    # Assume last pair = reverse sweep

    volt_col = volt_cols[-1]

    j_col = j_cols[-1]

    df = data.iloc[2:73].copy()

    df[volt_col] = pd.to_numeric(df[volt_col], errors='coerce')

    df[j_col] = pd.to_numeric(df[j_col], errors='coerce')

    return df[volt_col], df[j_col]


# -----------------------------

# Load data

# -----------------------------

V_before, J_before = load_reverse_sweep(path_before)

V_after, J_after = load_reverse_sweep(path_after)


# -----------------------------

# Plot

# -----------------------------

plt.figure(figsize=(10, 6))

plt.plot(V_before, J_before,

         color='blue',

         linestyle='-',

         linewidth=2,

         label='Before irradiation D03 (P2)')

plt.plot(V_after, J_after,

         color='red',

         linestyle=':',

         linewidth=2,

         label='After irradiation D03 (P2)')

plt.xlabel('Voltage (V)', fontsize=18)

plt.ylabel('Current Density (mA/cm$^2$)', fontsize=18)

plt.title(

    'J-V Curves Al2O3 Best Device',

    fontsize=18

)

plt.xlim(-0.2, 1.2)

plt.gca().invert_yaxis()

plt.ylim(5, -30)

plt.xticks(fontsize=14)

plt.yticks(fontsize=14)


#plt.legend(fontsize=14)

plt.legend(

    loc='lower left',

    fontsize=14,

    frameon=True

)

plt.tight_layout()

plt.show()
