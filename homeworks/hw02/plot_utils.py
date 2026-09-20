import matplotlib.pyplot as plt


def plot_pressure_over_time(table, output_dir):
    # Создаем рисунок и оси
    fig, ax = plt.subplots(figsize=(8, 5))

    # Строим две линии
    ax.plot(table["time_h"], table["boundary_pressure_mpa"],
            label="Давление на границе", marker="o", color="blue")
    ax.plot(table["time_h"], table["well_pressure_mpa"],
            label="Давление в скважине", marker="s", color="red")

    # Оформление осей и заголовка
    ax.set_xlabel("Время, ч")
    ax.set_ylabel("Давление, МПа")
    ax.set_title("Изменение давления во времени")

    # Сетка и легенда
    ax.grid(alpha=0.3)
    ax.legend()

    # Поиск и аннотация минимального значения
    min_index = table["well_pressure_mpa"].idxmin()
    min_time = table.loc[min_index, "time_h"]
    min_pressure = table.loc[min_index, "well_pressure_mpa"]

    ax.annotate(f"Min: {min_pressure:.2f} МПа",
                xy=(min_time, min_pressure),
                xytext=(min_time, min_pressure + 0.5),
                arrowprops=dict(facecolor='black', arrowstyle='->', lw=1.5))

    fig.tight_layout()

    # Сохранение и закрытие
    fig.savefig(output_dir / "pressure_over_time.png", dpi=200, bbox_inches="tight")
    fig.savefig(output_dir / "pressure_over_time.svg", bbox_inches="tight")
    plt.close(fig)


def plot_pressure_by_radius(table, output_dir):
    # Создаем рисунок и оси
    fig, ax = plt.subplots(figsize=(8, 5))

    # Точечный график (без соединительных линий)
    ax.plot(table["radius_m"], table["pressure_mpa"],
            marker="o", linestyle="none", color="green")

    # Логарифмическая шкала и оформление
    ax.set_xscale("log")
    ax.set_xlabel("Расстояние, м")
    ax.set_ylabel("Давление, МПа")
    ax.set_title("Давление в наблюдательных скважинах")
    ax.grid(alpha=0.3)

    fig.tight_layout()

    # Сохранение и закрытие
    fig.savefig(output_dir / "pressure_by_radius.png", dpi=200, bbox_inches="tight")
    fig.savefig(output_dir / "pressure_by_radius.svg", bbox_inches="tight")
    plt.close(fig)