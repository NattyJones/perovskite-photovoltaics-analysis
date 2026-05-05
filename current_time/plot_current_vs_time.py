import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

def read_data_from_file(file_path):
    time_seconds = []
    current_amperes = []

    with open(file_path, 'r') as file:
        lines = file.readlines()

        for line in lines:
            if line.startswith('Time(s)'):
                continue

            elif line.strip():
                data = line.split('\t')

                try:
                    time_seconds.append(float(data[0]))
                    current_amperes.append(float(data[1]))

                except ValueError:
                    continue

    return time_seconds, current_amperes


# === FILES TO PLOT ===
file_paths = [
    r"D:\University\Dissertation\Python Files\ITFiles\WP0008_LT00798_NJ00471_D02_P3.txt",
    r"D:\University\Dissertation\Python Files\ITFiles\WP0008_LT00798_NJ00471_D03_P1.txt",
    r"D:\University\Dissertation\Python Files\ITFiles\WP0008_LT00798_NJ00471_D06_P1.txt",
    r"D:\University\Dissertation\Python Files\ITFiles\WP0008_LT00798_NJ00471_D07_P3.txt",
    r"D:\University\Dissertation\Python Files\ITFiles\WP0008_LT00798_NJ00471_D44_P3.txt",
    r"D:\University\Dissertation\Python Files\ITFiles\WP0008_LT00798_NJ00471_D03_P3.txt"
]


# === COLOURS FOR EACH FILE ===
colors = [
    'black',
    '#FF7D7D',
    '#D1A7D6',
    '#FFE188',
    '#9EE2BB',
    'blue'
]


# === TITLES FOR EACH PLOT ===
titles = [
    'D02_P3 Post Irradiation',
    'D03_P1 Post Irradiation',
    'D06_P1 Post Irradiation',
    'D07_P3 Post Irradiation',
    'D44_P3 Post Irradiation',
    'D03_P3 Post Irradiation'
]


# =========================
# FIRST LOOP → find global y range in mA
# =========================
all_currents_mA = []

for file_path in file_paths:
    time, current = read_data_from_file(file_path)

    current_mA = [i * 1000 for i in current]
    all_currents_mA.extend(current_mA)


y_min = min(all_currents_mA)
y_max = max(all_currents_mA)

# Add padding so the curves do not touch the graph edges
padding = 0.05 * (y_max - y_min)

y_min = y_min - padding
y_max = y_max + padding


# =========================
# SECOND LOOP → plot with same y-axis limits
# =========================
for file_path, color, title in zip(file_paths, colors, titles):

    time, current = read_data_from_file(file_path)

    current_mA = [i * 1000 for i in current]

    plt.figure(figsize=(10, 6))

    plt.plot(
        time,
        current_mA,
        linestyle='-',
        color=color
    )

    ax = plt.gca()

    # Force y-axis labels to 2 decimal places
    ax.yaxis.set_major_formatter(ticker.FormatStrFormatter('%.2f'))

    # Force same y-axis range for all plots
    plt.ylim(y_min, y_max)

    plt.title(title, fontsize=16)
    plt.xlabel('Time (s)', fontsize=18)
    plt.ylabel('Current (mA)', fontsize=18)

    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)

    plt.grid(False)
    plt.tight_layout()
    plt.show()
