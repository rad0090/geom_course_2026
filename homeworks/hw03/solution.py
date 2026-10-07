import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# --- 1. Пути к файлам ---
ROOT = Path(__file__).resolve().parents[2]
raw_hw01 = ROOT / "data" / "raw" / "hw01"
processed_hw01 = ROOT / "data" / "processed" / "hw01"
figures_hw02 = ROOT / "figures" / "hw02"
figures_hw03 = ROOT / "figures" / "hw03"
hw03_dir = ROOT / "homeworks" / "hw03"

figures_hw03.mkdir(parents=True, exist_ok=True)
hw03_dir.mkdir(parents=True, exist_ok=True)

# Проверка предыдущих результатов
required_figures = [
    figures_hw02 / "pressure_over_time.svg",
    figures_hw02 / "pressure_by_radius.svg"
]
for path in required_figures:
    assert path.exists(), f"Файл {path} не существует!"
    assert path.stat().st_size > 0, f"Файл {path} пустой!"

# Загрузка таблиц
pumping_test = pd.read_csv(raw_hw01 / "pumping_test.txt", sep="\t")
wells = pd.read_csv(processed_hw01 / "wells_clean.csv")

assert pumping_test.shape == (13, 4)
assert wells.shape[0] == 7
assert not pumping_test.isna().any().any()
assert not wells.isna().any().any()

# --- 2. Подготовка массивов ---
time_h = pumping_test["time_h"].to_numpy()
boundary_pressure_mpa = pumping_test["boundary_pressure_mpa"].to_numpy()
well_pressure_mpa = pumping_test["well_pressure_mpa"].to_numpy()

well_id = wells["well_id"].to_numpy()
radius_m = wells["radius_m"].to_numpy()
observation_pressure_mpa = wells["pressure_mpa"].to_numpy()

# Сортировка массивов по радиусу
order = np.argsort(radius_m)
well_id = well_id[order]
radius_m = radius_m[order]
observation_pressure_mpa = observation_pressure_mpa[order]

# Расчет падения давления
pressure_drop_mpa = boundary_pressure_mpa - well_pressure_mpa
observation_drop_mpa = 12.0 - observation_pressure_mpa

# --- 3. Композиция 2 x 2 ---
fig1, axes = plt.subplots(2, 2, figsize=(12, 8), constrained_layout=True)

# Панель A. Линейный график
axA = axes[0, 0]
axA.plot(time_h, boundary_pressure_mpa, label="На границе", marker="o")
axA.plot(time_h, well_pressure_mpa, label="В скважине", marker="s")
axA.set_title("A. Давление во времени")
axA.set_xlabel("Время, ч")
axA.set_ylabel("Давление, МПа")
axA.legend()
axA.grid(alpha=0.3)

# Панель B. Точечная диаграмма
axB = axes[0, 1]
scatter = axB.scatter(radius_m, observation_pressure_mpa,
                      c=observation_pressure_mpa, cmap="viridis", s=100)
cbar = fig1.colorbar(scatter, ax=axB)
cbar.set_label("Давление, МПа")
axB.set_title("B. Давление в наблюдательных скважинах")
axB.set_xlabel("Расстояние, м")
axB.set_ylabel("Давление, МПа")
axB.grid(alpha=0.3)

# Панель C. Столбчатая диаграмма
axC = axes[1, 0]
axC.bar(well_id.astype(str), observation_drop_mpa, color="steelblue")
axC.set_title("C. Падение давления")
axC.set_xlabel("ID скважины")
axC.set_ylabel("Падение давления, МПа")
axC.grid(axis="y", alpha=0.3)

# Панель D. Диаграмма размаха
axD = axes[1, 1]
axD.boxplot([boundary_pressure_mpa, well_pressure_mpa], tick_labels=["На границе", "В скважине"])
axD.set_title("D. Размах давления")
axD.set_ylabel("Давление, МПа")
axD.grid(axis="y", alpha=0.3)

fig1.savefig(figures_hw03 / "pressure_overview.png", dpi=200)
fig1.savefig(figures_hw03 / "pressure_overview.svg")
plt.close(fig1)

# --- 4. Сравнение boxplot и violin plot ---
fig2, (ax_box, ax_violin) = plt.subplots(1, 2, figsize=(10, 5), constrained_layout=True)
data_to_plot = [boundary_pressure_mpa, well_pressure_mpa]
labels = ["На границе", "В скважине"]

# Boxplot
ax_box.boxplot(data_to_plot, tick_labels=labels)
ax_box.set_title("Boxplot (Диаграмма размаха)")
ax_box.set_ylabel("Давление, МПа")
ax_box.grid(axis="y", alpha=0.3)

# Violin plot
ax_violin.violinplot(data_to_plot, showmeans=True)
ax_violin.set_xticks([1, 2])
ax_violin.set_xticklabels(labels)
ax_violin.set_title("Violin plot (Скрипичная диаграмма)")
ax_violin.set_ylabel("Давление, МПа")
ax_violin.grid(axis="y", alpha=0.3)

fig2.savefig(figures_hw03 / "distributions.png", dpi=200)
fig2.savefig(figures_hw03 / "distributions.svg")
plt.close(fig2)

# --- 6. Подготовка данных для ДЗ №4 ---
output_path = hw03_dir / "viz_data.npz"
np.savez(
    output_path,
    time_h=time_h,
    boundary_pressure_mpa=boundary_pressure_mpa,
    well_pressure_mpa=well_pressure_mpa,
    pressure_drop_mpa=pressure_drop_mpa,
    well_id=well_id,
    radius_m=radius_m,
    observation_pressure_mpa=observation_pressure_mpa,
    observation_drop_mpa=observation_drop_mpa,
)

loaded = np.load(output_path, allow_pickle=True)
assert np.allclose(loaded["time_h"], time_h)
assert loaded["well_id"].shape == well_id.shape

print("Все графики успешно построены и сохранены!")