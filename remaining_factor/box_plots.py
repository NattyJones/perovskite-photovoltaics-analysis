import os
import re
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ============================================================
# 1. FOLDER PATHS
# ============================================================

config_folders = {
    "PFN-Br": {
        "pre": r"D:\University\Dissertation\Python Files\Graphs\BOX\BEFORE\PFN-Br",
        "post": r"D:\University\Dissertation\Python Files\Graphs\BOX\AFTER\PFN-Br"
    },

    "Al2O3": {
        "pre": r"D:\University\Dissertation\Python Files\Graphs\BOX\BEFORE\Al2O3",
        "post": r"D:\University\Dissertation\Python Files\Graphs\BOX\AFTER\Al2O3"
    },

    "Al2O3 + LiF": {
        "pre": r"D:\University\Dissertation\Python Files\Graphs\BOX\BEFORE\Al2O3-LiF",
        "post": r"D:\University\Dissertation\Python Files\Graphs\BOX\AFTER\Al2O3-LiF"
    },

    "Al2O3 + EDAl + LiF": {
        "pre": r"D:\University\Dissertation\Python Files\Graphs\BOX\BEFORE\Al2O3-LiF-EDAI-0-30",
        "post": r"D:\University\Dissertation\Python Files\Graphs\BOX\AFTER\Al2O3-LiF-EDAI-0-30"
    },

    "Al2O3 + EDAl": {
        "pre": r"D:\University\Dissertation\Python Files\Graphs\BOX\BEFORE\Al2O3-EDAI-0-30",
        "post": r"D:\University\Dissertation\Python Files\Graphs\BOX\AFTER\Al2O3-EDAI-0-30"
    }
}

config_order = [
    "PFN-Br",
    "Al2O3",
    "Al2O3 + LiF",
    "Al2O3 + EDAl + LiF",
    "Al2O3 + EDAl"
]

# ============================================================
# 2. SETTINGS
# ============================================================

# Excel row 79 = illuminated reverse scan
# pandas index = 78
REVERSE_ROW_INDEX = 78

# Column indexes from your screenshot
COLUMN_INDEXES = {
    "PCE": 7,   # Efficiency (%)
    "Voc": 3,   # Voc (V)
    "Jsc": 9,   # Jsc (mA/cm^2)
    "FF": 8     # Fill Factor (%)
}

metrics = ["PCE", "Voc", "Jsc", "FF"]

# Keep remaining factor as ratio
# 1.0 = unchanged
USE_PERCENT = False

# Basic sanity limits for raw JV values
SANITY_LIMITS = {
    "PCE": (0, 35),
    "Voc": (0, 1.5),
    "Jsc": (0, 35),
    "FF": (0, 100)
}

# Minimum PRE values required
MIN_PRE_THRESHOLDS = {
    "PCE": 1.0,
    "Voc": 0.5,
    "Jsc": 1.0,
    "FF": 30.0
}

# Remaining factor filter
MIN_RF = 0.0
MAX_RF = 1.5

SHOW_BOX_FLIERS = False

palette = {
    "PFN-Br": "#F4A3A3",
    "Al2O3": "#C7B5E8",
    "Al2O3 + LiF": "#AFCBFF",
    "Al2O3 + EDAl + LiF": "#B9E4C9",
    "Al2O3 + EDAl": "#F3D7A6"
}

# Y-axis limits you specifically want
custom_y_limits = {
    "PCE": (0.6, 1.05),
    "Voc": (0.9, 1.05),
    "FF": (0.7, 1.05)
}

# ============================================================
# 3. FUNCTIONS
# ============================================================

def extract_device_pixel(filename):
    match = re.search(r"D0*(\d+)_P0*(\d+)", filename, re.IGNORECASE)
    if match:
        device = int(match.group(1))
        pixel = int(match.group(2))
        return f"D{device}_P{pixel}"
    return None


def read_jv_file(file_path):
    extension = os.path.splitext(file_path)[1].lower()

    try:
        if extension in [".xlsx", ".xls"]:
            df = pd.read_excel(file_path, header=None)
        elif extension == ".csv":
            df = pd.read_csv(file_path, header=None)
        else:
            return None
    except Exception as e:
        print(f"Could not read file: {file_path}")
        print(e)
        return None

    if len(df) <= REVERSE_ROW_INDEX:
        print(f"Skipped (fewer than 79 rows): {os.path.basename(file_path)}")
        return None

    row = df.iloc[REVERSE_ROW_INDEX]

    values = {}
    for metric, col_index in COLUMN_INDEXES.items():
        try:
            values[metric] = pd.to_numeric(row.iloc[col_index], errors="coerce")
        except Exception:
            values[metric] = None

    if all(pd.isna(v) for v in values.values()):
        print(f"Skipped (no usable values in row 79): {os.path.basename(file_path)}")
        return None

    return values


def value_is_sane(metric, value):
    if pd.isna(value):
        return False

    lower, upper = SANITY_LIMITS[metric]
    return lower <= value <= upper


def load_folder_data(folder_path):
    data = {}

    if not os.path.exists(folder_path):
        print(f"Folder does not exist: {folder_path}")
        return data

    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)

        if not os.path.isfile(file_path):
            continue

        if not filename.lower().endswith((".xlsx", ".xls", ".csv")):
            continue

        device_pixel = extract_device_pixel(filename)
        if device_pixel is None:
            print(f"Skipped (device/pixel not found): {filename}")
            continue

        values = read_jv_file(file_path)
        if values is None:
            continue

        if device_pixel in data:
            print(f"Warning: duplicate file for {device_pixel} in {folder_path}. Overwriting previous entry.")

        data[device_pixel] = values

    return data


# ============================================================
# 4. CALCULATE REMAINING FACTORS
# ============================================================

remaining_factor_rows = []
excluded_rows = []

for config_name, folders in config_folders.items():

    print(f"\nProcessing: {config_name}")

    pre_data = load_folder_data(folders["pre"])
    post_data = load_folder_data(folders["post"])

    matched_pixels = sorted(set(pre_data.keys()) & set(post_data.keys()))

    print(f"Pre files found: {len(pre_data)}")
    print(f"Post files found: {len(post_data)}")
    print(f"Matched pixels found: {len(matched_pixels)}")
    print(matched_pixels)

    for device_pixel in matched_pixels:
        for metric in metrics:

            pre_value = pre_data[device_pixel].get(metric)
            post_value = post_data[device_pixel].get(metric)

            if pd.isna(pre_value) or pd.isna(post_value):
                excluded_rows.append([config_name, device_pixel, metric, pre_value, post_value, "NaN value"])
                continue

            if not value_is_sane(metric, pre_value):
                excluded_rows.append([config_name, device_pixel, metric, pre_value, post_value, "Pre value outside sane range"])
                continue

            if not value_is_sane(metric, post_value):
                excluded_rows.append([config_name, device_pixel, metric, pre_value, post_value, "Post value outside sane range"])
                continue

            if pre_value < MIN_PRE_THRESHOLDS[metric]:
                excluded_rows.append([config_name, device_pixel, metric, pre_value, post_value, "Pre value below threshold"])
                continue

            if pre_value == 0:
                excluded_rows.append([config_name, device_pixel, metric, pre_value, post_value, "Pre value = 0"])
                continue

            remaining_factor = post_value / pre_value

            if remaining_factor < MIN_RF or remaining_factor > MAX_RF:
                excluded_rows.append([config_name, device_pixel, metric, pre_value, post_value, f"Remaining factor outside {MIN_RF} to {MAX_RF}"])
                continue

            plot_value = remaining_factor * 100 if USE_PERCENT else remaining_factor

            remaining_factor_rows.append({
                "Configuration": config_name,
                "Device_Pixel": device_pixel,
                "Metric": metric,
                "Pre": pre_value,
                "Post": post_value,
                "Remaining Factor": remaining_factor,
                "Plot Value": plot_value
            })

remaining_df = pd.DataFrame(remaining_factor_rows)
excluded_df = pd.DataFrame(
    excluded_rows,
    columns=["Configuration", "Device_Pixel", "Metric", "Pre", "Post", "Reason"]
)

print("\nRemaining factor data used in plots:")
print(remaining_df)

print("\nExcluded data:")
print(excluded_df)

if remaining_df.empty:
    raise ValueError("No data left after filtering. Check thresholds and file contents.")

remaining_df.to_csv("remaining_factor_results_cleaned.csv", index=False)
excluded_df.to_csv("remaining_factor_excluded_rows.csv", index=False)

# ============================================================
# 5. PLOT BOX PLOTS
# ============================================================

sns.set_style("white")

if USE_PERCENT:
    ref_line = 100
else:
    ref_line = 1.0

for metric in metrics:
    plot_data = remaining_df[remaining_df["Metric"] == metric].copy()

    plt.figure(figsize=(11, 6))

    sns.boxplot(
        data=plot_data,
        x="Configuration",
        y="Plot Value",
        order=config_order,
        palette=palette,
        showfliers=SHOW_BOX_FLIERS,
        width=0.6
    )

    sns.stripplot(
        data=plot_data,
        x="Configuration",
        y="Plot Value",
        order=config_order,
        color="black",
        size=5,
        jitter=0.15,
        alpha=0.75
    )

    #plt.axhline(ref_line, color="red", linestyle="--", linewidth=1.2)

    plt.title(f"{metric} Remaining Factor After Irradiation", fontsize=16)
    plt.xlabel("Configuration", fontsize=14)

    if USE_PERCENT:
        plt.ylabel(f"{metric} Remaining Factor (%)", fontsize=14)
    else:
        plt.ylabel(f"{metric} Remaining Factor (Post / Pre)", fontsize=14)

    # ========================================================
    # Custom y-axis handling
    # ========================================================
    if metric in custom_y_limits:
        y_min, y_base_max = custom_y_limits[metric]
        data_max = plot_data["Plot Value"].max()

        # Start at 0.5, go to at least 1.0,
        # but if filtered data has values above 1.0 (e.g. 1.2),
        # extend the axis so they still show
        plt.ylim(y_min, y_base_max)

    plt.xticks(rotation=20, fontsize=12)
    plt.yticks(fontsize=12)
    plt.grid(False)
    plt.tight_layout()
    plt.show()
