# Flet 0.85.3 — Getting Started

> Источник: [flet.dev/docs](https://flet.dev/docs/) (PDF стр. 2, 28–29). Полный архив: [docs/flet-docs.pdf](../flet-docs.pdf)

## ft.run и точка входа

```python
import flet as ft

def main(page: ft.Page):
    page.title = "Моё приложение"
    page.padding = 0
    page.theme_mode = ft.ThemeMode.LIGHT
    page.add(ft.Text("Привет"))

ft.run(main)
```

Запуск из терминала: `python src/main.py` или `flet run src/main.py`.

Опции `ft.run`:

```python
ft.run(main, host="127.0.0.1", port=8550, view=ft.AppView.FLET_APP)
```

Веб-режим: `flet run --web counter.py`.

## Page — корневой контрол

- Все видимые контролы добавляются в `page` или внутрь других контролов.
- `page.add(control)` — сокращение для `page.controls.append` + `page.update()`.
- После изменения свойств уже добавленных контролов — `page.update()` (отправляет только дельту).

Частые свойства `page`:

| Свойство | Назначение |
|----------|------------|
| `title` | Заголовок окна |
| `padding` | Отступы страницы |
| `theme_mode` | `ft.ThemeMode.LIGHT` / `DARK` |
| `vertical_alignment` | Выравнивание по вертикали |
| `horizontal_alignment` | Выравнивание по горизонтали |
| `scroll` | `ft.ScrollMode.AUTO` для прокрутки всей страницы |

## Императивная модель UI

Flet — императивный UI: вы создаёте контролы, меняете их свойства и вызываете `update()`. Это отличается от декларативного Flutter.

```python
t = ft.Text()
page.add(t)
for i in range(10):
    t.value = f"Шаг {i}"
    page.update()
```

## Паттерн проекта flet_graph

См. [src/main.py](../../src/main.py):

1. Настройка `page` (title, padding, theme).
2. Экран загрузки через `create_load_screen`.
3. После выбора CSV — `page.controls.clear()`, `page.add(create_main_screen(...))`, `page.update()`.

## См. также

- [controls.md](controls.md) — вёрстка
- [async-and-events.md](async-and-events.md) — обработчики и async
- [dialogs-and-pickers.md](dialogs-and-pickers.md) — FilePicker
