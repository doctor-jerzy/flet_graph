# Документация Flet для агента

Локальный справочник Flet **0.85.3** для проекта [flet_graph](../../README.md).

## Файлы по темам

| Файл | Когда подключать (`@`) |
|------|------------------------|
| [getting-started.md](getting-started.md) | `ft.run`, Page, смена экранов |
| [controls.md](controls.md) | Column, Row, Container, кнопки, Dropdown, TextField |
| [dialogs-and-pickers.md](dialogs-and-pickers.md) | FilePicker, диалоги |
| [datatable.md](datatable.md) | Таблица CSV, DataTable |
| [charts.md](charts.md) | BarChart, LineChart, графики анализа |
| [async-and-events.md](async-and-events.md) | `on_click`, async, `update()` |

## Как формулировать запросы агенту

**Хорошо:**

```
Добавь столбчатый график средней цены по району
@src/ui_components.py @docs/flet/charts.md
```

```
Почему не обновляется таблица после удаления строки?
@src/ui_components.py @docs/flet/async-and-events.md
```

**Плохо:**

- Прикреплять весь `flet-docs.pdf`
- «Сделай как в документации» без указания темы
- Ссылаться на туториалы Flet 0.20.x

## Код проекта как эталон

- [src/main.py](../../src/main.py) — точка входа, FilePicker, навигация экранов
- [src/ui_components.py](../../src/ui_components.py) — UI-компоненты, таблица, тулбар

## Автоматический контекст

- Skill: [.cursor/skills/flet/SKILL.md](../../.cursor/skills/flet/SKILL.md)
- Правило для Python: [.cursor/rules/flet.mdc](../../.cursor/rules/flet.mdc)

## Полный архив

[docs/flet-docs.pdf](../flet-docs.pdf) — полная выгрузка flet.dev (2554 стр.). Используйте только если нужного нет в тематических `.md`.
