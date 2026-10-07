import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# --- 1. Пути и папки ---
ROOT = Path(__file__).resolve().parents[2]
hw03_data_path = ROOT / "homeworks" / "hw03" / "viz_data.npz"
hw04_dir = ROOT / "homeworks" / "hw04"
figures_dir = ROOT / "figures" / "hw04"

hw04_dir.mkdir(parents=True, exist_ok=True)
figures_dir.mkdir(parents=True, exist_ok=True)

# Загрузка данных из ДЗ №3
loaded_data = np.load(hw03_data_path, allow_pickle=True)

time_h = loaded_data["time_h"]
well_pressure_mpa = loaded_data["well_pressure_mpa"]
well_id = loaded_data["well_id"]
radius_m = loaded_data["radius_m"]
observation_pressure_mpa = loaded_data["observation_pressure_mpa"]

# Проверки из задания
assert time_h.shape == (13,)
assert well_pressure_mpa.shape == (13,)
assert well_id.shape == (7,)
assert radius_m.shape == (7,)
assert observation_pressure_mpa.shape == (7,)
assert np.all(np.diff(time_h) > 0)
assert np.all(np.diff(radius_m) > 0)
assert (radius_m > 0).all()

# --- 2. Создание учебного поля ---
time_component = well_pressure_mpa - well_pressure_mpa[0]
radius_component = observation_pressure_mpa - observation_pressure_mpa[0]

pressure_field = (
    well_pressure_mpa[0]
    + time_component[:, np.newaxis]
    + radius_component[np.newaxis, :]
)
assert pressure_field.shape == (13, 7)

# --- 3. Ориентация массива ---
field_for_plot = pressure_field.T
assert field_for_plot.shape == (7, 13)

# --- 4. Цветовая шкала ---
vmin = pressure_field.min()
vmax = pressure_field.max()
levels = np.linspace(vmin, vmax, 9)

# --- 8. Сравнение способов изображения (Две панели) ---
fig1, axes = plt.subplots(1, 2, figsize=(14, 6), constrained_layout=True)

# Панель A: Тепловая карта (pcolormesh)
axA = axes[0]
mesh = axA.pcolormesh(
    time_h,
    radius_m,
    field_for_plot,
    shading="auto",
    cmap="viridis",
    vmin=vmin,
    vmax=vmax,
    edgecolors="white", # Тонкие границы ячеек, как просили в задании
    linewidths=0.5
)
axA.set_yscale("log")
axA.set_xlabel("Время, ч")
axA.set_ylabel("Расстояние, м")
axA.set_title("A. Тепловая карта по ячейкам")
fig1.colorbar(mesh, ax=axA, label="Давление, МПа")

# Панель B: Заливка по уровням (contourf) и изолинии (contour)
axB = axes[1]
filled = axB.contourf(
    time_h,
    radius_m,
    field_for_plot,
    levels=levels,
    cmap="viridis",
    vmin=vmin,
    vmax=vmax,
)
lines = axB.contour(
    time_h,
    radius_m,
    field_for_plot,
    levels=levels,
    colors="black",
    linewidths=0.6,
)
axB.clabel(lines, fmt="%.2f")
axB.set_yscale("log")
axB.set_xlabel("Время, ч")
axB.set_ylabel("Расстояние, м")
axB.set_title("B. Заливка по уровням с изолиниями")
fig1.colorbar(filled, ax=axB, label="Давление, МПа")

fig1.savefig(figures_dir / "pressure_maps.png", dpi=200)
fig1.savefig(figures_dir / "pressure_maps.svg")
plt.close(fig1)

# --- 9. Только изолинии ---
fig2, ax = plt.subplots(figsize=(8, 6), constrained_layout=True)
lines_only = ax.contour(
    time_h,
    radius_m,
    field_for_plot,
    levels=levels,
    colors="black",
    linewidths=0.6,
)
ax.clabel(lines_only, fmt="%.2f")
ax.set_yscale("log")
ax.set_xlabel("Время, ч")
ax.set_ylabel("Расстояние, м")
ax.set_title("Изолинии поля давления")

fig2.savefig(figures_dir / "pressure_isolines.png", dpi=200)
fig2.savefig(figures_dir / "pressure_isolines.svg")
plt.close(fig2)

# --- 10. Сохранение данных для ДЗ №5 ---
output_path = hw04_dir / "field_data.npz"
np.savez(
    output_path,
    time_h=time_h,
    radius_m=radius_m,
    well_id=well_id,
    pressure_field=pressure_field,
    contour_levels=levels,
)

loaded = np.load(output_path, allow_pickle=True)
assert np.allclose(loaded["pressure_field"], pressure_field)

print("Все графики для ДЗ №4 успешно построены и сохранены!")