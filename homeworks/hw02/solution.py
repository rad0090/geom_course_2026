import pandas as pd
from pathlib import Path
import plot_utils

# --- 1. Пути и папки ---
ROOT = Path(__file__).resolve().parents[2]
raw_hw01 = ROOT / "data" / "raw" / "hw01"
processed_hw01 = ROOT / "data" / "processed" / "hw01"
figures_dir = ROOT / "figures" / "hw02"

figures_dir.mkdir(parents=True, exist_ok=True)

# --- 2. Чтение данных ---
pumping_test = pd.read_csv(raw_hw01 / "pumping_test.txt", sep="\t")
wells_clean = pd.read_csv(processed_hw01 / "wells_clean.csv")

# --- 3. Сортировка и проверка ---
wells_sorted = wells_clean.sort_values("radius_m")
assert (wells_sorted["radius_m"] > 0).all()

# --- 4. Построение графиков ---
print("Строим графики...")
plot_utils.plot_pressure_over_time(pumping_test, figures_dir)
plot_utils.plot_pressure_by_radius(wells_sorted, figures_dir)

# --- 5. Проверка файлов ---
assert (figures_dir / "pressure_over_time.png").exists()
assert (figures_dir / "pressure_over_time.svg").exists()
assert (figures_dir / "pressure_by_radius.png").exists()
assert (figures_dir / "pressure_by_radius.svg").exists()

print("Готово! Графики успешно сохранены в папку figures/hw02/")