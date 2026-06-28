---
name: flet
description: Guides Flet 0.85.3 UI development for this project — Page lifecycle, controls, FilePicker, DataTable, charts. Use when writing or editing Flet Python code, flet_graph app screens, or when the user mentions Flet, ft., page.update, or UI components.
---

# Flet 0.85.3 — проект flet_graph

## Версии

- `flet==0.85.3`, `flet-datatable2==0.85.3`, `flet-web==0.85.3`
- Полная документация: `docs/flet/*.md`, архив `docs/flet-docs.pdf`

## API 0.85.x (не путать со старыми туториалами)

| Старый стиль | Актуальный (0.85.3) |
|--------------|---------------------|
| `ElevatedButton` | `ft.Button`, `ft.FilledButton`, `ft.OutlinedButton` |
| `icons.XXX` | `ft.Icons.XXX` |
| `colors.XXX` | `ft.Colors.XXX` |
| `alignment=ft.alignment.center` | `align=ft.Alignment.CENTER` |

## Каркас приложения

```python
import flet as ft

def main(page: ft.Page):
    page.title = "..."
    page.padding = 0
    page.theme_mode = ft.ThemeMode.LIGHT
    page.add(...)  # или page.controls.clear(); page.add(...)
    page.update()  # после смены экрана

ft.run(main)
# ft.run(main, host="127.0.0.1", port=8550, view=ft.AppView.FLET_APP)
```

Паттерн проекта ([src/main.py](src/main.py)):

1. Экран загрузки → `create_load_screen`
2. `async` FilePicker → `pd.read_csv`
3. Экран данных → `create_main_screen` в [src/ui_components.py](src/ui_components.py)

## Обновление UI

- После `page.controls.clear()` и `page.add()` — вызвать `page.update()`
- Для отдельных контролов с уже добавленным на страницу — `control.update()`
- В обработчиках внутри `create_main_screen` обновляются `table_slot`, `status`, `subtitle` и т.д.

## Частые контролы в проекте

| Контрол | Назначение |
|---------|------------|
| `ft.Column` / `ft.Row` | Вёрстка, `expand=True`, `spacing`, `wrap=True` |
| `ft.Container` | Отступы, `expand`, слот для динамического контента |
| `ft.SafeArea` | Обёртка главного экрана |
| `ft.Text` | Заголовки, статус; `weight=ft.FontWeight.BOLD`, `color=ft.Colors.*` |
| `ft.Button` / `ft.FilledButton` / `ft.OutlinedButton` | Действия, `icon=ft.Icons.*` |
| `ft.Dropdown` | Выбор столбца; `ft.dropdown.Option(str(col))` |
| `ft.TextField` | Ввод номера строки; `keyboard_type=ft.KeyboardType.NUMBER` |
| `ft.DataTable` | Таблица CSV |
| `ft.FilePicker` | Выбор файла (async) |

## FilePicker (async)

```python
async def on_file_picked(e):
    files = await ft.FilePicker().pick_files(
        allow_multiple=False,
        allowed_extensions=["csv"],
        dialog_title="Выберите файл с данными",
    )
    if not files:
        return
    path = files[0].path
```

Подробнее: [docs/flet/dialogs-and-pickers.md](../../docs/flet/dialogs-and-pickers.md)

## DataTable

```python
columns = [ft.DataColumn(ft.Text(str(col), weight=ft.FontWeight.BOLD)) for col in df.columns]
rows = [
    ft.DataRow(cells=[ft.DataCell(ft.Text(str(v))) for v in row])
    for _, row in df.iterrows()
]
ft.DataTable(columns=columns, rows=rows, heading_row_color=ft.Colors.SURFACE_CONTAINER_HIGHEST)
```

Обёртка в `ft.Row(..., scroll=ft.ScrollMode.AUTO)` для горизонтальной прокрутки.

Подробнее: [docs/flet/datatable.md](../../docs/flet/datatable.md)

## Графики

Для анализа недвижимости — `ft.BarChart`, `ft.LineChart`, `ft.PieChart` (модуль `flet.charts`).

Подробнее: [docs/flet/charts.md](../../docs/flet/charts.md)

## Справочники по темам

| Файл | Тема |
|------|------|
| [docs/flet/getting-started.md](../../docs/flet/getting-started.md) | `ft.run`, Page, тема |
| [docs/flet/controls.md](../../docs/flet/controls.md) | Column, Container, Button, Dropdown |
| [docs/flet/dialogs-and-pickers.md](../../docs/flet/dialogs-and-pickers.md) | FilePicker, диалоги |
| [docs/flet/datatable.md](../../docs/flet/datatable.md) | DataTable |
| [docs/flet/charts.md](../../docs/flet/charts.md) | BarChart, LineChart, PieChart |
| [docs/flet/async-and-events.md](../../docs/flet/async-and-events.md) | async, on_click, update |
| [docs/flet/README.md](../../docs/flet/README.md) | Как работать с агентом |
