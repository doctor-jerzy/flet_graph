# Flet 0.85.3 — Dialogs and Pickers

> Источник: [flet.dev/docs/services/filepicker](https://flet.dev/docs/services/filepicker) (PDF стр. 799–800)

## ft.FilePicker

Сервис для выбора файлов, сохранения и выбора каталога через системный диалог.

**Важно:** на Linux в desktop-режиме может потребоваться `zenity`. В браузере — не требуется.

### Методы

| Метод | Назначение |
|-------|------------|
| `pick_files(...)` | Выбор одного или нескольких файлов |
| `save_file(...)` | Диалог «Сохранить как» |
| `get_directory_path(...)` | Выбор каталога |
| `upload(...)` | Загрузка выбранных файлов на URL |

В 0.85.3 методы **async** — вызывать с `await`.

### Минимальный пример (как в проекте)

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
    name = files[0].name
```

Полный поток в [src/main.py](../../src/main.py): `pd.read_csv(files[0].path)` → смена экрана.

### Параметры pick_files

- `allow_multiple` — несколько файлов
- `allowed_extensions` — список расширений без точки, напр. `["csv", "xlsx"]`
- `dialog_title` — заголовок диалога

### Регистрация на странице (для upload)

Если нужен `on_upload` или повторное использование одного экземпляра:

```python
file_picker = ft.FilePicker()
page.services.append(file_picker)
```

Для простого `await ft.FilePicker().pick_files()` в обработчике кнопки отдельная регистрация не обязательна.

### save_file и get_directory_path

```python
save_path = await ft.FilePicker().save_file()
dir_path = await ft.FilePicker().get_directory_path()
```

`save_file` на web может быть недоступен (`disabled=page.web`).

## Диалоги (кратко)

```python
page.show_dialog(ft.AlertDialog(title=ft.Text("Заголовок"), content=ft.Text("Текст")))
page.close_dialog()
```

Cupertino-стиль: `page.show_dialog(ft.CupertinoBottomSheet(...))`.

## См. также

- [async-and-events.md](async-and-events.md) — async-обработчики
- [getting-started.md](getting-started.md) — смена экранов после выбора файла
