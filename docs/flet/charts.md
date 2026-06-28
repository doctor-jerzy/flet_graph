# Flet 0.85.3 — Charts

> Источник: [flet.dev/docs/controls/charts](https://flet.dev/docs/controls/charts/) (PDF стр. 2184, 2194)

## Пакет flet-charts

В Flet 0.85 графики вынесены в отдельный пакет:

```bash
pip install flet-charts
```

```python
import flet as ft
import flet_charts as fch
```

Добавьте `flet-charts` в `requirements.txt`, когда начнёте строить графики.

## BarChart

```python
fch.BarChart(
    border=ft.Border.all(1, ft.Colors.GREY_400),
    min_y=0,
    max_y=100,
    groups=[
        fch.BarChartGroup(
            x=0,
            bar_rods=[
                fch.BarChartRod(from_y=0, to_y=40, color=ft.Colors.BLUE_GREY_200),
            ],
        ),
    ],
    bottom_axis=fch.ChartAxis(labels=[fch.ChartAxisLabel(value=0, label=ft.Text("A"))]),
    left_axis=fch.ChartAxis(labels=[...]),
)
```

Свойства: `groups`, `group_spacing`, `interactive` (tooltips при наведении), `on_event`.

## LineChart

```python
fch.LineChart(
    min_y=0,
    max_y=3,
    min_x=0,
    max_x=5,
    data_series=[
        fch.LineChartData(
            color=ft.Colors.BLUE_GREY_500,
            curved=True,
            points=[
                fch.LineChartDataPoint(1, 0.5),
                fch.LineChartDataPoint(2, 1.5),
            ],
        ),
    ],
)
```

## PieChart

```python
fch.PieChart(
    sections=[
        fch.PieChartSection(value=40, title="A", color=ft.Colors.BLUE),
        fch.PieChartSection(value=30, title="B", color=ft.Colors.GREEN),
    ],
)
```

## Интеграция с pandas (flet_graph)

Типичный поток для анализа недвижимости:

1. Агрегировать `dataframe` (groupby по району, средняя цена).
2. Собрать `BarChartGroup` / `LineChartDataPoint` из значений.
3. Добавить график в `ft.Column` главного экрана рядом с таблицей.
4. При смене данных — пересоздать chart и `update()` родительский контейнер.

## Оси и сетка

- `bottom_axis`, `left_axis`, `right_axis`, `top_axis` — подписи и заголовки
- `horizontal_grid_lines`, `vertical_grid_lines` — линии сетки
- `animation` — плавная анимация при смене данных

## См. также

- [controls.md](controls.md) — размещение графика в Column/Container
- [datatable.md](datatable.md) — таблица рядом с графиком
- Онлайн-примеры: [flet.dev/docs/controls/charts/barchart](https://flet.dev/docs/controls/charts/barchart)
