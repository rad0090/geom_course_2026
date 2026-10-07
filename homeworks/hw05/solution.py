import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from pathlib import Path

# --- Настройка путей ---
# --- Настройка путей ---
ROOT = Path(__file__).resolve().parents[2]
hw04_data_path = ROOT / "homeworks" / "hw04" / "field_data.npz"
hw04_fig_path = ROOT / "figures" / "hw04" / "pressure_maps.svg"
hw05_dir = ROOT / "homeworks" / "hw05"
figures_dir = ROOT / "figures" / "hw05"

# Добавь эти две команды для автоматического создания папок:
hw05_dir.mkdir(parents=True, exist_ok=True)
figures_dir.mkdir(parents=True, exist_ok=True)
# --- 1. Проверка результатов ДЗ №4 ---
loaded_data = np.load(hw04_data_path, allow_pickle=True)

time_h = loaded_data["time_h"]
radius_m = loaded_data["radius_m"]
well_id = loaded_data["well_id"]
pressure_field = loaded_data["pressure_field"]
contour_levels = loaded_data["contour_levels"]

assert time_h.shape == (13,)
assert radius_m.shape == (7,)
assert well_id.shape == (7,)
assert pressure_field.shape == (13, 7)
assert contour_levels.shape == (9,)
assert np.all(np.diff(time_h) > 0)
assert np.all(np.diff(radius_m) > 0)

assert hw04_fig_path.exists()
assert hw04_fig_path.stat().st_size > 0

# --- 2. Создание длинной таблицы ---
time_grid, radius_grid = np.meshgrid(time_h, radius_m, indexing="ij")
time_index, radius_index = np.indices(pressure_field.shape)
well_names_long = well_id[radius_index.reshape(-1)]

long_table = pd.DataFrame({
    "time_h": time_grid.reshape(-1),
    "radius_m": radius_grid.reshape(-1),
    "well_id": well_names_long,
    "pressure_mpa": pressure_field.reshape(-1)
})

assert long_table.shape == (91, 4)
assert long_table["time_h"].nunique() == 13
assert long_table["radius_m"].nunique() == 7
assert not long_table.isna().any().any()

csv_path = hw05_dir / "pressure_long.csv"
long_table.to_csv(csv_path, index=False)

# Повторная проверка
loaded_csv = pd.read_csv(csv_path)
assert loaded_csv.shape == (91, 4)
assert not loaded_csv.isna().any().any()

# --- 3. Создание анимации ---
fig, ax = plt.subplots(figsize=(8, 6))
ax.set_xscale("log")
ax.set_xlabel("Расстояние, м")
ax.set_ylabel("Давление, МПа")

margin = 0.1
y_min = pressure_field.min() - margin
y_max = pressure_field.max() + margin
ax.set_ylim(y_min, y_max)
ax.grid(alpha=0.3)

line, = ax.plot([], [], marker='o', color='steelblue', linewidth=2)


def update(frame_index):
    """Обновляет кадр для заданного момента времени."""
    current_time = time_h[frame_index]
    current_pressure = pressure_field[frame_index]

    line.set_data(radius_m, current_pressure)
    ax.set_title(f"Время: {current_time} ч")
    return line,


ani = FuncAnimation(fig, update, frames=len(time_h), blit=True)
ani.save(figures_dir / "pressure_animation.gif", writer="pillow", fps=2)
plt.close(fig)

print("Данные и анимация для ДЗ №5 успешно созданы!")