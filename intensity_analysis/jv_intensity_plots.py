import pandas as pd

import matplotlib.pyplot as plt

import re


def plot_backward_bias_sweeps(file_path, title):

    # Load data

    data = pd.read_csv(file_path)

    # Identify voltage and current columns

    volt_column_indices = []

    j_column_indices = []

    for col in data.columns:

        if 'Volt (V)' in str(data[col].iloc[0]):

            volt_column_indices.append(col)

        elif '[J (mA/cm^2)]' in str(data[col].iloc[0]):

            j_column_indices.append(col)

    # Extract JV sweep data

    data_frames = []

    for volt_col, j_col in zip(volt_column_indices, j_column_indices):

        df = data.iloc[2:73].copy()

        df[volt_col] = pd.to_numeric(df[volt_col], errors='coerce')

        df[j_col] = pd.to_numeric(df[j_col], errors='coerce')

        data_frames.append(df)

    # Extract metadata for intensity and direction

    summary_rows = data.iloc[75:]

    pattern = re.compile(r'CH_Ref\(([\d.]+) SUN\)\.(Forward|Reverse)', re.IGNORECASE)

    sweep_entries = []

    for i in range(len(volt_column_indices)):

        try:

            sweep_info = str(summary_rows.iloc[i, 0])

            match = pattern.search(sweep_info)

            if match:

                intensity = float(match.group(1))

                direction = match.group(2).lower()

                if direction == "reverse":

                    sweep_entries.append({

                        "index": i,

                        "intensity": intensity,

                        "volt_col": volt_column_indices[i],

                        "j_col": j_column_indices[i]

                    })

        except:

            continue

    # Sort by intensity descending

    sweep_entries_sorted = sorted(sweep_entries, key=lambda x: -x["intensity"])

    # Plot

    fig, ax = plt.subplots(figsize=(10, 6))

    fig.suptitle(title, fontsize=18)

    plt.tight_layout(rect=[0, 0, 1, 0.95])

    print("Detected sweeps:", sweep_entries_sorted)

    for entry in sweep_entries_sorted:

        label = f"{entry['intensity']} SUN"

        df = data_frames[entry["index"]]

        ax.plot(df[entry["volt_col"]], df[entry["j_col"]], label=label)

    ax.set_xlabel("Voltage (V)", fontsize=18)

    ax.set_ylabel("Current Density (mA/cm$^2$)", fontsize=18)

    ax.set_xlim(-0.2, 1.2)

    ax.set_ylim(5, -25)

    ax.tick_params(labelsize=14)

    ax.legend(fontsize=10, bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)

    ax.grid(False)

    plt.tight_layout()

    plt.show()


# === Provide paths to five different files ===

graph_titles = [

    "Al2O3-EDAI - D02 P3 (Post-Irradiation)",

    "Al2O3 - D03 P2 (Post-Irradiation)",

    "Al2O3 - D03 P3 (Post-Irradiation)",

    "Al2O3-LiF - D06 P3 (Post-Irradiation)",

    "PFN-Br - D44 P3 (Post-Irradiation)"

]

file_paths = [

    r"D:\University\Dissertation\Python Files\IntensityFiles/WP0008_LT00798_NJ00471_D02_P3.csv",

    r"D:\University\Dissertation\Python Files\IntensityFiles/WP0008_LT00798_NJ00471_D03_P2.csv",

    r"D:\University\Dissertation\Python Files\IntensityFiles/WP0008_LT00798_NJ00471_D03_P3.csv",

    r"D:\University\Dissertation\Python Files\IntensityFiles/WP0008_LT00798_NJ00471_D06_P3.csv",

    r"D:\University\Dissertation\Python Files\IntensityFiles/WP0008_LT00798_NJ00471_D44_P3.csv"

    #r"E:\University\Dissertation\Python Files\IntensityFiles/LT00798_E016_D021_P1.csv"

]

# === Plot each file individually ===

for idx, file_path in enumerate(file_paths):

    plot_backward_bias_sweeps(file_path, graph_titles[idx])