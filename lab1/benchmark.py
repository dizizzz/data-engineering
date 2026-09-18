import time
import pandas as pd

FILES = {
    "CSV": "transactions.csv",
    "Parquet none": "transactions_none.parquet",
    "Parquet snappy": "transactions_snappy.parquet",
}
REPEATS = 3


def read(fmt, path, columns=None):
    if fmt == "CSV":
        return pd.read_csv(path, usecols=columns)
    return pd.read_parquet(path, columns=columns)


# Запити: (назва, потрібні стовпці, функція обробки)
QUERIES = [
    ("Читання всього файлу", None,
     lambda df: len(df)),
    ("Кількість шахрайських операцій", ["isFraud"],
     lambda df: int(df["isFraud"].sum())),
    ("Сума за типом операції", ["type", "amount"],
     lambda df: df.groupby("type")["amount"].sum()),
    ("Топ-5 переказів TRANSFER", ["type", "amount", "nameOrig"],
     lambda df: df[df["type"] == "TRANSFER"].nlargest(5, "amount")),
]


def measure(fmt, path, columns, func):
    best = float("inf")
    for _ in range(REPEATS):
        start = time.perf_counter()
        result = func(read(fmt, path, columns))
        best = min(best, time.perf_counter() - start)
    return best, result


timings = {}
for name, columns, func in QUERIES:
    print(f"\n=== {name} ===")
    for fmt, path in FILES.items():
        seconds, result = measure(fmt, path, columns, func)
        timings[(name, fmt)] = seconds
        print(f"{fmt:<16} {seconds:6.2f} с")
    print("Результат:")
    print(result)

# Підсумкова таблиця для звіту
print("\n\nЧас виконання, с (найкращий з", REPEATS, "запусків)")
header = f"{'Запит':<34}" + "".join(f"{fmt:>16}" for fmt in FILES)
print(header)
for name, _, _ in QUERIES:
    row = f"{name:<34}" + "".join(f"{timings[(name, fmt)]:>16.2f}" for fmt in FILES)
    print(row)