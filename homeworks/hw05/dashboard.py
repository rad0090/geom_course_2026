"""Приложение Dash для интерактивного просмотра поля давления."""

from pathlib import Path
import pandas as pd
import plotly.express as px
from dash import Dash, Input, Output, dcc, html

ROOT = Path(__file__).resolve().parents[2]
DATA_PATH = ROOT / "homeworks" / "hw05" / "pressure_long.csv"

table = pd.read_csv(DATA_PATH)
required_columns = {
    "time_h",
    "radius_m",
    "well_id",
    "pressure_mpa",
}
assert required_columns.issubset(table.columns)

time_values = sorted(table["time_h"].unique())

app = Dash(__name__)
app.layout = html.Div(
    [
        html.H1("Давление и расстояние"),
        dcc.Slider(
            id="time-slider",
            min=0,
            max=len(time_values) - 1,
            step=1,
            value=0,
            marks={
                index: str(time)
                for index, time in enumerate(time_values)
            },
        ),
        dcc.Graph(id="pressure-graph"),
    ]
)


@app.callback(
    Output("pressure-graph", "figure"),
    Input("time-slider", "value"),
)
def update_graph(time_index):
    """Верните фигуру Plotly для выбранного момента времени."""
    selected_time = time_values[time_index]
    current = table[table["time_h"] == selected_time]

    # Создание точечно-линейной фигуры Plotly
    fig = px.line(
        current,
        x="radius_m",
        y="pressure_mpa",
        log_x=True,
        markers=True,
        title=f"Давление от расстояния (Текущее время: {selected_time} ч)",
        labels={
            "radius_m": "Расстояние, м",
            "pressure_mpa": "Давление, МПа"
        }
    )

    # Фиксируем ось Y, чтобы график не скакал, как в анимации
    margin = 0.1
    fig.update_layout(yaxis_range=[table["pressure_mpa"].min() - margin,
                                   table["pressure_mpa"].max() + margin])
    return fig


if __name__ == "__main__":
    app.run(debug=True)