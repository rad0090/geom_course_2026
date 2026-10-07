# ДЗ №5. Анимация и интерактивный просмотр

**Темы:** временные ряды, кадры анимации, `FuncAnimation`, длинный формат таблицы, Dash, callback.

## Цель

Научиться показывать изменение поля из ДЗ №4 во времени двумя способами:

- как GIF-анимацию;
- как интерактивный график с ползунком.

Один кадр соответствует одному моменту времени.

## Подготовка

```powershell
python -m pip install -r environment/requirements-dash.txt
```

В папке задания находится `dashboard_template.py`. Скопируйте его в `dashboard.py` и заполните участок `TODO`.

## 1. Проверьте результат ДЗ №4

Загрузите:

```text
homeworks/hw04/field_data.npz
```

Проверьте:

```python
required_keys = {
    "time_h",
    "radius_m",
    "well_id",
    "pressure_field",
    "contour_levels",
}

assert time_h.shape == (13,)
assert radius_m.shape == (7,)
assert well_id.shape == (7,)
assert pressure_field.shape == (13, 7)
assert contour_levels.shape == (9,)
assert np.all(np.diff(time_h) > 0)
assert np.all(np.diff(radius_m) > 0)
```

Также проверьте, что существует и не является пустым:

```text
figures/hw04/pressure_maps.svg
```

## 2. Создайте длинную таблицу

В длинной таблице одна строка соответствует одному сочетанию времени и расстояния.

```python
time_grid, radius_grid = np.meshgrid(
    time_h,
    radius_m,
    indexing="ij",
)

time_index, radius_index = np.indices(
    pressure_field.shape
)
```

Создайте DataFrame со столбцами:

```text
time_h
radius_m
well_id
pressure_mpa
```

Для преобразования матриц в столбцы используйте `reshape(-1)`.

Названия скважин:

```python
well_names_long = well_id[
    radius_index.reshape(-1)
]
```

Проверьте:

```python
assert long_table.shape == (91, 4)
assert long_table["time_h"].nunique() == 13
assert long_table["radius_m"].nunique() == 7
assert not long_table.isna().any().any()
```

Сохраните:

```text
homeworks/hw05/pressure_long.csv
```

Загрузите CSV обратно и повторите проверки.

## 3. Создайте анимацию

В каждом кадре покажите зависимость давления от расстояния для одного момента времени.

Ось X должна быть логарифмической:

```python
ax.set_xscale("log")
```

Определите постоянные пределы Y:

```python
margin = 0.1
y_min = pressure_field.min() - margin
y_max = pressure_field.max() + margin
```

Пределы не должны меняться между кадрами. Иначе изменение масштаба будет выглядеть как изменение данных.

Создайте:

```python
def update(frame_index):
    ...
```

Функция должна:

1. выбирать `pressure_field[frame_index]`;
2. обновлять координаты линии и точек;
3. показывать текущее время в заголовке;
4. возвращать изменённые графические объекты.

Создайте `FuncAnimation` из 13 кадров и сохраните:

```text
figures/hw05/pressure_animation.gif
```

Используйте `PillowWriter`.

## 4. Создайте приложение Dash

Файл:

```text
homeworks/hw05/dashboard.py
```

Приложение должно читать `pressure_long.csv`. Числа давления нельзя повторять внутри программы.

Интерфейс:

- заголовок;
- ползунок с 13 моментами;
- график давления по расстоянию;
- логарифмическая ось расстояния;
- подписи осей и единицы;
- выбранное время.

Callback получает номер выбранного момента, находит соответствующее время, отбирает семь строк и возвращает фигуру Plotly.

Запуск:

```powershell
python homeworks/hw05/dashboard.py
```

Проверьте:

- первый момент;
- один промежуточный момент;
- последний момент.

Значения должны совпадать с соответствующими строками `pressure_field`.

## 5. Сравните статическое и динамическое представление

В `../hw04/answers.md` сравните:

- тепловую карту ДЗ №4;
- изолинии ДЗ №4;
- анимацию;
- интерактивный график.

Укажите, какое представление удобнее для:

1. обзора всего поля сразу;
2. чтения конкретного уровня;
3. наблюдения последовательности изменений;
4. самостоятельного выбора момента времени.

## Короткие вопросы

1. Что считается кадром?
2. Почему пределы оси Y должны быть постоянными?
3. Что делает функция `update`?
4. Чем анимация отличается от интерактивного графика?
5. Зачем нужен длинный формат таблицы?
6. Что делает callback?
7. Почему приложение читает CSV, а не содержит числа внутри кода?
8. Что легче увидеть на тепловой карте, а что — в анимации?

## Чеклист

- [ ] Загружен и проверен `field_data.npz`.
- [ ] Проверен рисунок ДЗ №4.
- [ ] Создана таблица из 91 строки.
- [ ] Сохранён и повторно загружен `pressure_long.csv`.
- [ ] Создана анимация из 13 кадров.
- [ ] Пределы оси постоянны.
- [ ] GIF открывается.
- [ ] Создано приложение Dash.
- [ ] Ползунок изменяет данные.
- [ ] Проверены три положения ползунка.
- [ ] Сравнены четыре способа представления.
- [ ] Написаны ответы.
- [ ] Сделаны commit и push.

## Что сдавать

```text
homeworks/hw05/solution.py
homeworks/hw05/dashboard.py
homeworks/hw05/answers.md
homeworks/hw05/pressure_long.csv
figures/hw05/pressure_animation.gif
```

Перед сдачей:

```powershell
python homeworks/hw05/solution.py
python homeworks/hw05/dashboard.py
git add homeworks/hw05 figures/hw05
git commit -m "Complete homework 5"
git push
```

## Индивидуальная сдача

Студент должен:

1. показать связь кадра со строкой массива;
2. объяснить постоянные пределы осей;
3. изменить положение ползунка;
4. показать, как callback выбирает семь строк;
5. сравнить тепловую карту, изолинии и анимацию.
