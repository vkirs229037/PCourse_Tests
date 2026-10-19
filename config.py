"""Общие константы для всех скриптов."""

DATA_DIR = "Data"
RESULTS_DIR = "results"

# Пути к запускаемым программам
PROGRAMS = {
    "cpp": "./course_cpp",
    "fptl": "./course_fptl",
}

ALGORITHMS = ["dijkstra", "johnson", "floyd"]

THREADS = list(range(1, 25))

# Входные графы. Имя = размер + признак бинарности ("b" в конце).
# "100"  - взвешенный граф 100x100, файлы cpp_100.txt и fptl_100.txt
# "100b" - бинарный граф 100x100, файлы cpp_100b.txt и fptl_100b.txt
GRAPHS = ["20", "20b", "50", "50b", "100", "100b", "500", "500b"]

# Число прогонов
RUNS = 10
