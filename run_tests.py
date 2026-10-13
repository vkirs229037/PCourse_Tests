"""Запускает обе программы при всех параметрах и сохраняет времена в results/raw.csv."""
import os
import re
import subprocess

import pandas as pd

from config import ALGORITHMS, DATA_DIR, GRAPHS, PROGRAMS, RESULTS_DIR, THREADS, RUNS


def get_time(impl, output):
    if impl == "cpp":
        # Время - последняя непустая строка вывода (после строки "Время выполнения (с):").
        # Заголовок не ищем, чтобы не зависеть от кодировки консоли.
        lines = [line for line in output.splitlines() if line.strip()]
        return float(lines[-1])
    # fptl: строка "Evaluation time: 0.037s"
    return float(re.search(r"Evaluation time:\s*([\d.]+)s", output).group(1))


rows = []
for impl, program in PROGRAMS.items():
    for algo in ALGORITHMS:
        for graph in GRAPHS:
            path = os.path.join(DATA_DIR, f"{impl}_{graph}.txt")
            for threads in THREADS:
                time = 0
                print("runs ")
                for run in range(RUNS):
                    print(run, end=" ", flush=True)
                    result = subprocess.run(
                        [program, algo, path, str(threads)],
                        capture_output=True, text=True, errors="replace",
                    )
                    time_i = get_time(impl, result.stdout)
                    time += time_i
                print()
                time = time / RUNS
                rows.append({"impl": impl, "algo": algo, "graph": graph,
                             "threads": threads, "time": time})
                print(impl, algo, graph, threads, time, flush=True)

os.makedirs(RESULTS_DIR, exist_ok=True)
pd.DataFrame(rows).to_csv(os.path.join(RESULTS_DIR, "raw.csv"), index=False)
