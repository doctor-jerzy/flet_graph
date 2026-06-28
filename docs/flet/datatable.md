# Flet 0.85.3 — DataTable

> Источник: [flet.dev/docs/controls/datatable](https://flet.dev/docs/controls/datatable) (PDF стр. 232–238, 237)

## ft.DataTable

Material-таблица: колонки (`DataColumn`) + строки (`DataRow` / `DataCell`).

```python
columns = [
    ft.DataColumn(ft.Text(str(col), weight=ft.FontWeight.BOLD))
    for col in dataframe.columns
]
rows = [
    ft.DataRow(
        cells=[
            ft.DataCell(ft.Text("" if v is None else str(v), no_wrap=True))
            for v in row
        ]
    )
    for _, row in dataframe.iterrows()
]
table = ft.DataTable(
    columns=columns,
    rows=rows,
    heading_row_color=ft.Colors.SURFACE_CONTAINER_HIGHEST,
)
```

## Прокрутка широкой таблицы

```python
ft.Row(table, scroll=ft.ScrollMode.AUTO, align=ft.Alignment.TOP_LEFT)
```

Проект: [create_data_table](../../src/ui_components.py).

## DataColumn

- `label` — заголовок (`ft.Text` или строка)
- `numeric=True` — выравнивание чисел вправо
- `on_sort` — сортировка по клику на заголовок

## DataCell

- `content` — обычно `ft.Text` или другой контрол
- `placeholder=True` — для пустых ячеек-заглушек
- События: `on_tap`, `on_double_tap`, `on_long_press`

## Полезные свойства DataTable

| Свойство | Назначение |
|----------|------------|
| `heading_row_color` | Фон строки заголовков |
| `data_row_min_height` / `data_row_max_height` | Высота строк |
| `column_spacing` | Расстояние между колонками |
| `border` | Рамка таблицы |
| `show_checkbox_column` | Чекбоксы для выбора строк |
| `sort_column_index`, `sort_ascending` | Состояние сортировки |

## flet-datatable2

Для больших таблиц — пакет `flet-datatable2` (уже в [requirements.txt](../../requirements.txt)):

- липкие заголовки
- фиксированные строки/колонки
- настройка ширины колонок

```python
import flet_datatable2 as ftd
# см. документацию flet-datatable2 при необходимости
```

В проекте пока используется встроенный `ft.DataTable`; `ftd` импортирован для будущего расширения.

## Динамическое обновление

При смене данных пересоздайте таблицу и обновите контейнер-слот:

```python
table_slot.content = create_data_table(current_dataframe)
table_slot.update()
```

Проект: функция `refresh()` в `create_main_screen`.

## См. также

- [controls.md](controls.md) — `ft.Row`, `ft.Container`
- [async-and-events.md](async-and-events.md)
