# Flet 0.85.3 — Async and Events

> Источник: [flet.dev/docs](https://flet.dev/docs/) (PDF стр. 28–29, 799–800)

## page.update()

После любого изменения UI отправьте обновление клиенту:

- `page.update()` — вся страница (только дельта с прошлого вызова)
- `control.update()` — один контрол, уже добавленный на страницу

```python
page.controls.clear()
page.add(new_screen)
page.update()
```

## Обработчики событий

Сигнатура: `def handler(e)` или `async def handler(e)`.

```python
def delete_column(e):
    # логика
    table_slot.update()
    status.update()

ft.OutlinedButton("Удалить столбец", on_click=delete_column)
```

Тип события: `ft.Event[ft.Button]`, `ft.ControlEvent`, и т.д.

## Async-обработчики

FilePicker и часть сервисов требуют `async`:

```python
async def on_file_picked(e):
    files = await ft.FilePicker().pick_files(...)
    if not files:
        return
    # ...

ft.Button("Выбрать файл", on_click=on_file_picked)
```

Внутри async-обработчика можно вызывать `await control.focus()` (см. пример To-Do в документации).

## Обновление отдельных контролов vs страницы

Паттерн проекта ([ui_components.py](../../src/ui_components.py)):

```python
def show_message(message, color=ft.Colors.ON_SURFACE_VARIANT):
    status.value = message
    status.color = color
    status.update()  # только статус

def refresh():
    table_slot.content = create_data_table(current_dataframe)
    subtitle.value = f"{len(df)} строк, ..."
    # после refresh() вызывают update() у затронутых контролов
```

После `refresh()` в обработчиках вызывается несколько `.update()` — это нормально для локальных изменений.

## Замыкания и состояние экрана

`create_main_screen` хранит `current_dataframe` через `nonlocal` в обработчиках. Альтернатива — класс или `page.session`.

## disabled

```python
control.disabled = True
control.update()
```

Распространяется на дочерние контролы контейнера.

## Типичные ошибки

| Проблема | Решение |
|----------|---------|
| UI не меняется | Забыли `page.update()` или `control.update()` |
| FilePicker не открывается | Нужен `async def` и `await pick_files()` |
| Старый экран виден после смены | `page.controls.clear()` перед `page.add()` |

## См. также

- [dialogs-and-pickers.md](dialogs-and-pickers.md)
- [getting-started.md](getting-started.md)
