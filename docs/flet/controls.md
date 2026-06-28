# Flet 0.85.3 — Controls (layout и ввод)

> Источник: [flet.dev/docs/controls](https://flet.dev/docs/controls/) (PDF стр. 144, 150, 278, 514, 598)

## ft.Column

Вертикальная раскладка дочерних контролов.

```python
ft.Column(
    [
        ft.Text("Заголовок", size=28, weight=ft.FontWeight.BOLD),
        ft.Text("Подзаголовок"),
        ft.Button("Действие", on_click=handler),
    ],
    alignment=ft.MainAxisAlignment.CENTER,
    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    spacing=14,
    expand=True,
)
```

Ключевые свойства: `controls` (или позиционный список), `spacing`, `alignment`, `horizontal_alignment`, `expand`, `wrap`, `scroll`.

Проект: [create_load_screen](../../src/ui_components.py) — центрированная колонка на экране загрузки.

## ft.Row

Горизонтальная раскладка. В проекте — тулбар и прокручиваемая таблица.

```python
ft.Row(
    [btn1, btn2, dropdown],
    spacing=10,
    wrap=True,
    vertical_alignment=ft.CrossAxisAlignment.CENTER,
    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
    scroll=ft.ScrollMode.AUTO,
)
```

## ft.Container

Обёртка: отступы, выравнивание, фон, граница, слот для динамического контента.

```python
ft.Container(
    content=column_or_row,
    align=ft.Alignment.CENTER,
    expand=True,
    padding=32,
)
```

Проект: `table_slot = ft.Container(expand=True)` — контейнер, в который подставляется таблица при `refresh()`.

## ft.SafeArea

Избегает системных вырезов (статус-бар, notch).

```python
ft.SafeArea(
    content=ft.Container(content=main_column, expand=True, padding=24),
    expand=True,
)
```

Проект: обёртка главного экрана в `create_main_screen`.

## ft.Text

```python
ft.Text("Текст", size=24, weight=ft.FontWeight.BOLD, color=ft.Colors.ON_SURFACE_VARIANT)
```

## Кнопки (0.85.x)

| Класс | Когда использовать |
|-------|-------------------|
| `ft.Button` | Обычная кнопка |
| `ft.FilledButton` | Основное действие |
| `ft.OutlinedButton` | Вторичные действия |
| `ft.IconButton` | Только иконка |

```python
ft.FilledButton("Открыть CSV", icon=ft.Icons.FOLDER_OPEN, on_click=on_open)
ft.OutlinedButton("Сбросить", icon=ft.Icons.RESTART_ALT, on_click=reset)
```

Не использовать устаревшие `ElevatedButton`, `TextButton` из старых туториалов.

## ft.Dropdown

```python
dropdown = ft.Dropdown(
    label="Столбец",
    width=240,
    dense=True,
    enable_search=True,
    options=[ft.dropdown.Option(str(col)) for col in columns],
    value=None,
)
```

Обновление опций: присвоить `dropdown.options`, затем `dropdown.update()`.

## ft.TextField

```python
ft.TextField(
    label="Строка",
    width=120,
    dense=True,
    keyboard_type=ft.KeyboardType.NUMBER,
    hint_text="1",
)
```

## disabled

Свойство `disabled` наследуется вниз по дереву. Можно отключить `ft.Column` со всеми полями формы.

## См. также

- [async-and-events.md](async-and-events.md)
- [datatable.md](datatable.md)
- Примеры в [src/ui_components.py](../../src/ui_components.py)
