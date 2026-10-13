"""Генерирует входные графы в папку Data (по два файла на граф: для cpp и для fptl).

Все графы - неориентированные взвешенные деревья (матрица смежности симметричная,
рёбер ровно n-1). Если имя графа заканчивается на "b" - это двоичное дерево
(у каждой вершины не более двух потомков), иначе - случайное дерево.
"""
import os

import numpy as np

from config import DATA_DIR, GRAPHS

MAX_WEIGHT = 10   # веса рёбер от 1 до MAX_WEIGHT; 0 в матрице = ребра нет

os.makedirs(DATA_DIR, exist_ok=True)
rng = np.random.default_rng(0)

for graph in GRAPHS:
    n = int(graph.rstrip("b"))
    binary = graph.endswith("b")

    # Вершина 0 - корень. Каждая следующая вершина v присоединяется к родителю
    # с меньшим номером, поэтому граф всегда связный и без циклов.
    matrix = np.zeros((n, n), dtype=int)
    for v in range(1, n):
        if binary:
            parent = (v - 1) // 2          # полное двоичное дерево
        else:
            parent = rng.integers(0, v)    # любая из уже добавленных вершин
        weight = rng.integers(1, MAX_WEIGHT + 1)
        matrix[v, parent] = weight
        matrix[parent, v] = weight         # неориентированное ребро

    # cpp: только матрица
    np.savetxt(os.path.join(DATA_DIR, f"cpp_{graph}.txt"), matrix, fmt="%d")

    # fptl: сначала число вершин, потом матрица
    with open(os.path.join(DATA_DIR, f"fptl_{graph}.txt"), "w") as f:
        f.write(f"{n}\n")
        np.savetxt(f, matrix, fmt="%d")

    print("Создан граф", graph)
