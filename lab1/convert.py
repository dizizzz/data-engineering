import os
import time
import pyarrow.csv as pv
import pyarrow.parquet as pq

CSV_FILE = "transactions.csv"
CODECS = ["none", "snappy"]


def size_mb(path):
    return os.path.getsize(path) / 1024**2


# Читаємо CSV
start = time.perf_counter()
table = pv.read_csv(CSV_FILE)
read_time = time.perf_counter() - start
print(f"CSV прочитано: {table.num_rows:,} рядків за {read_time:.1f} с")
print(table.schema, "\n")

csv_size = size_mb(CSV_FILE)
results = []

# Записуємо Parquet з різним стисненням
for codec in CODECS:
    path = f"transactions_{codec}.parquet"
    start = time.perf_counter()
    pq.write_table(table, path, compression=codec)
    write_time = time.perf_counter() - start
    results.append((codec, size_mb(path), write_time))

# Підсумкова таблиця
print(f"{'Формат':<20}{'Розмір, МБ':>12}{'У скільки разів менше':>24}{'Час запису, с':>16}")
print(f"{'CSV':<20}{csv_size:>12.1f}{'1.0x':>24}{'-':>16}")
for codec, size, write_time in results:
    print(f"{'Parquet ' + codec:<20}{size:>12.1f}{csv_size / size:>23.1f}x{write_time:>16.1f}")