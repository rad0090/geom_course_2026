import numpy as np
import pandas as pd
from pathlib import Path
import data_utils

# --- 1. Пути и папки ---
ROOT = Path(__file__).resolve().parents[2]
raw = ROOT / "data" / "raw" / "hw01"
processed = ROOT / "data" / "processed" / "hw01"
exports = ROOT / "exports" / "hw01"

processed.mkdir(parents=True, exist_ok=True)
exports.mkdir(parents=True, exist_ok=True)

# --- 2. Чтение данных ---
wells = data_utils.read_wells(raw / "wells.csv")
layers = data_utils.read_layers(raw / "layers.xlsx")
pump = data_utils.read_pumping_test(raw / "pumping_test.txt")

for name, tbl in [("Wells", wells), ("Layers", layers), ("Pump", pump)]:
    data_utils.print_table_info(name, tbl)

# --- 3. Проверка и очистка (ИСПРАВЛЕНО: Вывод количества пропусков) ---
print("\n--- Количество пропусков в таблице wells ---")
print(wells.isna().sum())

wells_clean = wells.dropna(subset=["pressure_mpa"]).copy()

assert (wells_clean["radius_m"] > 0).all()
assert (layers["thickness_m"] > 0).all()
assert layers["porosity_fraction"].between(0, 1).all()

# --- 4. Вычисления столбцов ---
wells_clean["pressure_pa"] = wells_clean["pressure_mpa"] * 1000000
wells_clean["pressure_difference_mpa"] = 12 - wells_clean["pressure_mpa"]
wells_clean["relative_change_percent"] = (wells_clean["pressure_difference_mpa"] / 12) * 100

# --- 5. Функции NumPy ---
rad = wells_clean["azimuth_deg"] * np.pi / 180
assert np.allclose(wells_clean["radius_m"] * np.cos(rad), wells_clean["x_m"], atol=0.02)
assert np.allclose(wells_clean["radius_m"] * np.sin(rad), wells_clean["y_m"], atol=0.02)

wells_clean["log_radius"] = np.log(wells_clean["radius_m"])
pump["decay"] = np.exp(-pump["time_h"] / 36)
assert np.isclose(pump["decay"].iloc[0], 1.0, atol=0.05)

# --- ИСПРАВЛЕНО: Сохраняем таблицу ТОЛЬКО после добавления всех новых столбцов ---
wells_clean.to_csv(processed / "wells_clean.csv", index=False)

# --- 6. Минимум, максимум, среднее ---
stats_data = []
for df, col in [(wells_clean, "pressure_mpa"), (wells_clean, "radius_m"),
                (layers, "thickness_m"), (layers, "porosity_fraction")]:
    stats_data.append([col, df[col].min(), df[col].max(), df[col].mean()])

stats_df = pd.DataFrame(stats_data, columns=["Параметр", "Min", "Max", "Mean"])

# --- 7. Выбор элементов ---
p = wells_clean["pressure_mpa"].to_numpy()
print("\nИндексы:", p[0], p[-1])
print("Срезы:", p[:3], p[::2])
print("Маска (ниже среднего):", p[p < p.mean()])
print("Дальше 100м:\n", wells_clean[wells_clean["radius_m"] > 100])

# --- 8. Массивы NumPy (2D и 3D) ---
mat = pump[["boundary_pressure_mpa", "well_pressure_mpa"]].to_numpy()
cube = np.stack([mat, mat + 0.05], axis=0)

print("\nndim, shape, size, dtype (2D):", mat.ndim, mat.shape, mat.size, mat.dtype)
print("1 табл:\n", cube[0], "\n2 табл:\n", cube[1], "\n1 строка:", cube[0, 0])
print("Столбец:\n", cube[:, :, 1])

# --- 9. Reshape и транспонирование ---
mat_transposed = mat.T
assert np.allclose(cube.reshape(-1).reshape(cube.shape), cube)

# --- 10. Классы ---
print("\nКлассы:")
print(data_utils.DatasetInfo("Wells", wells_clean).describe())
print(data_utils.DatasetInfo("Layers", layers).describe())
print(data_utils.DatasetInfo("Pump", pump).describe())

# --- 11. Сохранение и финальная проверка ---
stats_df.to_excel(processed / "table_summary.xlsx", index=False)
np.save(processed / "pressure_matrix.npy", mat)
np.savez(processed / "pressure_cube.npz", pressure_cube=cube)

with open(exports / "results.txt", "w", encoding="utf-8") as f:
    f.write(f"Форма 2D: {mat.shape}\nФорма 3D: {cube.shape}\n\nСтатистика:\n")
    f.write(stats_df.to_string(index=False))

assert np.allclose(np.load(processed / "pressure_matrix.npy"), mat)
assert np.allclose(np.load(processed / "pressure_cube.npz")["pressure_cube"], cube)

print("\nГотово! Код успешно дошел до конца.")