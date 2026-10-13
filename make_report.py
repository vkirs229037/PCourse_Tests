"""По results/raw.csv строит таблицы (.xlsx) и графики (.png) в папке results."""
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

from config import ALGORITHMS, GRAPHS, PROGRAMS, RESULTS_DIR

PLOTS_DIR = os.path.join(RESULTS_DIR, "plots")
os.makedirs(PLOTS_DIR, exist_ok=True)

# характеристика -> (название листа / графика, подпись оси Y)
CHARACTERISTICS = {
    "time": ("Время", "Время выполнения, с"),
    "speedup": ("Ускорение", "Ускорение"),
    "efficiency": ("Эффективность", "Эффективность"),
}

raw = pd.read_csv(os.path.join(RESULTS_DIR, "raw.csv"), dtype={"graph": str})


# ---------- Таблицы ----------
# tables[(реализация, алгоритм)][характеристика] = DataFrame (строки - потоки, столбцы - графы)
tables = {}
for impl in PROGRAMS:
    for algo in ALGORITHMS:
        d = raw[(raw["impl"] == impl) & (raw["algo"] == algo)]
        time = d.pivot(index="threads", columns="graph", values="time")[GRAPHS]
        speedup = time.loc[1] / time                  # время на 1 потоке / время на N потоках
        efficiency = speedup.div(time.index, axis=0)  # ускорение / число потоков
        tables[(impl, algo)] = {"time": time, "speedup": speedup, "efficiency": efficiency}

for (impl, algo), t in tables.items():
    with pd.ExcelWriter(os.path.join(RESULTS_DIR, f"{impl}_{algo}.xlsx")) as writer:
        for key, (sheet, _) in CHARACTERISTICS.items():
            t[key].to_excel(writer, sheet_name=sheet, index_label="Потоки")


# ---------- Графики ----------
def save_plot(lines, title, ylabel, filename):
    """lines - словарь {подпись: Series, где индекс - число потоков}."""
    plt.figure(figsize=(8, 5))
    for label, series in lines.items():
        plt.plot(series.index, series.values, marker="o", label=label)
    plt.title(title)
    plt.xlabel("Число потоков")
    plt.ylabel(ylabel)
    plt.grid(True)
    plt.legend()
    plt.savefig(os.path.join(PLOTS_DIR, filename), dpi=150, bbox_inches="tight")
    plt.close()


# По каждой реализации: 3 характеристики x размеры графов, все алгоритмы на одном графике
for impl in PROGRAMS:
    for key, (name, ylabel) in CHARACTERISTICS.items():
        for graph in GRAPHS:
            lines = {algo: tables[(impl, algo)][key][graph] for algo in ALGORITHMS}
            save_plot(lines, f"{impl}: {name.lower()}, граф {graph}", ylabel,
                      f"{impl}_{key}_{graph}.png")

# Сравнение реализаций: для каждого алгоритма и размера графа - время/ускорение/эффективность cpp и fptl
for algo in ALGORITHMS:
    for key, (name, ylabel) in CHARACTERISTICS.items():
        for graph in GRAPHS:
            lines = {impl: tables[(impl, algo)][key][graph] for impl in PROGRAMS}
            save_plot(lines, f"Сравнение реализаций ({name.lower()}): {algo}, граф {graph}",
                    ylabel, f"compare_{algo}_{graph}.png")

print("Готово:", RESULTS_DIR)
