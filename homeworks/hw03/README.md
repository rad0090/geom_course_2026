# ДЗ №3. Несколько способов показать одни данные

**Темы:** line plot, scatter plot, bar chart, boxplot, violin plot, `subplots`, цветовая шкала.

## Цель

Научиться выбирать тип графика по структуре данных и собирать несколько связанных графиков в одну композицию.

Задание продолжает ДЗ №2. Перед началом должны существовать его результаты:

```text
figures/hw02/pressure_over_time.svg
figures/hw02/pressure_by_radius.svg
```

Также используются таблицы, подготовленные в ДЗ №1:

```text
data/raw/hw01/pumping_test.txt
data/processed/hw01/wells_clean.csv
```

Если файлов нет, сначала заново запустите решения ДЗ №1 и ДЗ №2.

## 1. Проверьте предыдущие результаты

Проверьте существование двух SVG:

```python
for path in required_figures:
    assert path.exists()
    assert path.stat().st_size > 0
```

Загрузите таблицы:

```python
pumping_test = pd.read_csv(pumping_path, sep="\t")
wells = pd.read_csv(wells_path)
```

Проверьте:

```python
assert pumping_test.shape == (13, 4)
assert wells.shape[0] == 7
assert not pumping_test.isna().any().any()
assert not wells.isna().any().any()
```

## 2. Подготовьте массивы

Из `pumping_test` получите:

```python
time_h = pumping_test["time_h"].to_numpy()
boundary_pressure_mpa = pumping_test["boundary_pressure_mpa"].to_numpy()
well_pressure_mpa = pumping_test["well_pressure_mpa"].to_numpy()
```

Из `wells_clean.csv` получите:

```python
well_id = wells["well_id"].to_numpy()
radius_m = wells["radius_m"].to_numpy()
observation_pressure_mpa = wells["pressure_mpa"].to_numpy()
```

Отсортируйте скважины по `radius_m`. Все три массива скважин должны сортироваться одним и тем же порядком:

```python
order = np.argsort(radius_m)
well_id = well_id[order]
radius_m = radius_m[order]
observation_pressure_mpa = observation_pressure_mpa[order]
```

Рассчитайте:

```python
pressure_drop_mpa = boundary_pressure_mpa - well_pressure_mpa
observation_drop_mpa = 12.0 - observation_pressure_mpa
```

## 3. Создайте композицию 2 × 2

```python
fig, axes = plt.subplots(
    2,
    2,
    figsize=(12, 8),
    constrained_layout=True,
)
```

### Панель A. Линейный график

Покажите два временных ряда:

- давление на границе;
- давление в скважине.

Моменты времени можно соединять линией, потому что они имеют определённый порядок.

### Панель B. Точечная диаграмма

Покажите давление в наблюдательных скважинах:

- X — `radius_m`;
- Y — `observation_pressure_mpa`;
- цвет точки — давление.

Добавьте цветовую шкалу `Давление, МПа`. Точки не соединяйте: скважины являются отдельными объектами.

### Панель C. Столбчатая диаграмма

Покажите `observation_drop_mpa` для семи скважин. На оси X должны находиться `well_id`.

### Панель D. Диаграмма размаха

Сравните два набора:

```text
boundary_pressure_mpa
well_pressure_mpa
```

Используйте `boxplot`. Вычислять квартили вручную не требуется: их рассчитывает Matplotlib.

Обозначьте панели буквами `A`, `B`, `C`, `D`.

## 4. Сравните boxplot и violin plot

Создайте второй рисунок:

- слева — `boxplot`;
- справа — `violinplot`.

Обе панели должны показывать одни и те же два временных ряда.

Круговую диаграмму строить не нужно: давления не являются долями одного целого.

## 5. Сохраните рисунки

```text
figures/hw03/pressure_overview.png
figures/hw03/pressure_overview.svg
figures/hw03/distributions.png
figures/hw03/distributions.svg
```

У каждой панели должны быть заголовок, подписи осей и единицы. Проверьте, что подписи не обрезаны.

## 6. Подготовьте данные для ДЗ №4

Создайте:

```text
homeworks/hw03/viz_data.npz
```

```python
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
```

Загрузите файл обратно. Проверьте ключи, формы и значения.

## Короткие вопросы

1. Почему моменты времени можно соединять линией?
2. Почему наблюдательные скважины не нужно соединять?
3. Когда уместна столбчатая диаграмма?
4. Что показывает линия внутри boxplot?
5. Чем violin plot отличается от boxplot?
6. Почему круговая диаграмма не подходит?
7. Зачем все связанные массивы сортировать одним порядком?

## Чеклист

- [ ] Проверены результаты ДЗ №2.
- [ ] Загружены две таблицы.
- [ ] Связанные массивы скважин отсортированы вместе.
- [ ] Создана композиция 2 × 2.
- [ ] Построены line, scatter, bar и box plot.
- [ ] Создано сравнение boxplot и violin plot.
- [ ] Панели подписаны буквами.
- [ ] Указаны величины и единицы.
- [ ] Созданы два PNG и два SVG.
- [ ] Создан и проверен `viz_data.npz`.
- [ ] Написаны ответы.
- [ ] Сделаны commit и push.

## Что сдавать

```text
homeworks/hw03/solution.py
homeworks/hw03/answers.md
homeworks/hw03/viz_data.npz
figures/hw03/pressure_overview.png
figures/hw03/pressure_overview.svg
figures/hw03/distributions.png
figures/hw03/distributions.svg
```

Перед сдачей:

```powershell
python homeworks/hw03/solution.py
git add homeworks/hw03 figures/hw03
git commit -m "Complete homework 3"
git push
```

## Индивидуальная сдача

Студент должен объяснить выбор каждого типа графика, показать создание сетки `Axes` и найти код, который формирует цветовую шкалу.
