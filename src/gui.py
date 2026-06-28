# ui.py
import flet as ft

import datawork as dtw
import config as cfg

def create_load_text():
    """Создание заголовка загрузочного экрана"""
    return ft.Text(
        value="Данные для анализа",
        size=28,
        weight=ft.FontWeight.BOLD
    )

def create_load_description(error: Exception | str | None):
    """Создание описания загрузочного экрана"""
    # Если информации об ошибке не поступило, обычная надпись
    if error is None:
        desc = ft.Text("Откройте CSV-файл, чтобы приступить к работе с данными.")
    # Если поступила, то надпись другая и красная
    else:
        desc = ft.Text(f"Ошибка чтения CSV: {error}")
        desc.color = ft.Colors.RED
    return desc


def create_load_button():
    """Создание кнопки загрузки на загрузочном экране"""
    return ft.FilledButton(
        content="Выбрать файл",
        icon=ft.Icons.UPLOAD_FILE
    )

def create_toolbar(*toolbar_icons):
    return ft.Row(
        list(toolbar_icons),
        spacing=10,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
    )


def create_load_icon():
    return ft.FilledIconButton(
        icon=ft.Icons.FOLDER_OPEN,
        tooltip="Открыть CSV"
    )


def create_revert_icon():
    return ft.OutlinedIconButton(
        icon=ft.Icons.RESTART_ALT,
        tooltip="Сбросить изменения"
    )


def create_del_col_icon():
    return ft.OutlinedIconButton(
        icon=ft.Icons.REMOVE_ROAD,
        tooltip="Удалить столбец"
    )

def create_table(df, curr_page):
    """Создаёт ВИДИМУЮ часть таблицы на основе переданного датафрейма"""
    if df.empty:
        return ft.Text("ДАТАФРЕЙМ ПУСТ", height=cfg.TABLE_HEIGHT)
    
    slice_df = dtw.get_rows_from_page(df, curr_page)
    
    columns = [
        ft.DataColumn(ft.Text(col, weight=ft.FontWeight.BOLD))
        for col in slice_df.columns
    ]
    
    rows = [
        ft.DataRow(
            cells=[
                ft.DataCell(
                    ft.Container(
                        ft.Text(str(value), selectable=True),
                        expand=True,
                        align=ft.Alignment.TOP_CENTER,
                        alignment=ft.Alignment.CENTER_RIGHT,
                        height=cfg.CELL_HEIGHT,
                        # border=ft.Border.all(width=1),
                        clip_behavior=ft.ClipBehavior.HARD_EDGE
                    )
                ) for value in row[1:]
            ]
        )
        for row in slice_df.itertuples()
    ]
    
    table = ft.DataTable(
        columns=columns,
        rows=rows,
        vertical_lines=ft.BorderSide(0.5, ft.Colors.ON_SURFACE_VARIANT),
        data_row_max_height=cfg.CELL_HEIGHT,
        heading_row_color=ft.Colors.SURFACE_CONTAINER_HIGHEST,
        heading_row_height=cfg.HEADER_HEIGHT
    )
    
    table_with_border = ft.Container(
        table,
        border=ft.Border.all(0.5, ft.Colors.ON_SURFACE_VARIANT)
    )
    
    table_with_no_expand = ft.Column(
        table_with_border,
        expand=False
    )
    
    return ft.Row(
        table_with_no_expand,
        height=cfg.TABLE_HEIGHT,
        scroll=ft.ScrollMode.AUTO,
        align=ft.Alignment.TOP_LEFT,
        vertical_alignment=ft.CrossAxisAlignment.STRETCH,
    )

def create_slider(*slide_buttons):
    return ft.Row(
        controls=list(slide_buttons),
        alignment=ft.MainAxisAlignment.CENTER
    )

def create_to_begin_button():
    return ft.OutlinedIconButton(
        icon=ft.Icons.KEYBOARD_DOUBLE_ARROW_LEFT,
        tooltip="В начало"
    )

def create_backward_button():
    return ft.OutlinedIconButton(
        icon=ft.Icons.KEYBOARD_ARROW_LEFT,
        tooltip="Назад"
    )

def create_forward_button():
    return ft.OutlinedIconButton(
        icon=ft.Icons.KEYBOARD_ARROW_RIGHT,
        tooltip="Вперёд"
    )

def create_to_end_button():
    return ft.OutlinedIconButton(
        icon=ft.Icons.KEYBOARD_DOUBLE_ARROW_RIGHT,
        tooltip="В конец"
    )

def create_page_info(curr_page, tot_pages):
    return ft.Text(f"Страница {curr_page} из {tot_pages}")

def create_parameters(content=None):
    if content is None:
        return ft.Text("Параметры")

def create_output(content=None):
    if content is None:
        return ft.Text("Вывод")

def create_workspace(*workspace_args):
    return ft.Column(
        list(workspace_args),
        scroll=ft.ScrollMode.AUTO,
    )

def create_column_dropdown(df):
    """Создаёт список колонок переданного датасета"""
    column_dropdown = ft.Dropdown(
        label="Столбец",
        expand=True,
        dense=True,
        enable_search=True,
    )
    if not df.empty:
        column_dropdown.options = [
            ft.dropdown.Option(str(column)) for column in df.columns
        ]
    return column_dropdown

def create_delete_button():
    return ft.FilledIconButton(
        icon=ft.Icons.DELETE,
        tooltip="Удалить поле",
        bgcolor=ft.Colors.ERROR,
    )

def create_info_button():
    """Создание иконки для получения информации о датасете."""
    return ft.OutlinedIconButton(
        icon=ft.Icons.INFO,
        tooltip="Информация о датасете"
    )

def create_dataset_info_display(info_string):
    """
    Создание контейнера с отформатированной информацией о датасете.
    info_string: строка, полученная из df.info(buf=None, verbose=True, show_counts=True)
    """
    # Преобразование в текст
    info_text = ft.Text(info_string, selectable=True, font_family='Consolas')
    # Преобразование в строку, чтобы она расширилась до контейнера по горизонтали
    info_row = ft.Row(info_text, expand=True)
    # Преобразование в колонку, чтобы по вертикали расширилась и добавить прокрутку
    return ft.Column(
        controls=info_row,
        scroll=ft.ScrollMode.AUTO,
        expand=True
    )

def create_stats_icon():
    """Создание иконки-переключателя для показа статистики."""
    return _create_toggle_icon(
        icon=ft.Icons.QUERY_STATS, 
        tooltip="Показать/скрыть статистику"
    )

def _create_toggle_icon(icon, tooltip):
    return ft.OutlinedIconButton(
        icon=ft.Icons.QUERY_STATS,
        tooltip="Показать/скрыть статистику",
        selected=False,  # Изначально не зажата
        style=ft.ButtonStyle(
            color={
                ft.ControlState.SELECTED: ft.Colors.ON_SECONDARY,    # Цвет когда зажата
                ft.ControlState.DEFAULT: ft.Colors.ON_SURFACE, # Цвет по умолчанию
            },
            bgcolor={
                ft.ControlState.SELECTED: ft.Colors.SECONDARY,    # Цвет когда зажата
                ft.ControlState.DEFAULT: ft.Colors.SURFACE, # Цвет по умолчанию
            }
        )
    )