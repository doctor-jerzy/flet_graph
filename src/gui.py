# ui.py
import flet as ft

import datawork as dtw
import config as cfg

def create_load_text():
    """Создание заголовка загрузочного экрана"""
    return ft.Text(
        value=cfg.TXT_LOAD_TITLE,
        size=cfg.LOAD_TITLE_SIZE,
        weight=ft.FontWeight.BOLD
    )

def create_load_description(error: Exception | str | None):
    """Создание описания загрузочного экрана"""
    # Если информации об ошибке не поступило, обычная надпись
    if error is None:
        desc = ft.Text(cfg.TXT_LOAD_DESC_DEFAULT)
    # Если поступила, то надпись другая и красная
    else:
        desc = ft.Text(f"{cfg.TXT_LOAD_DESC_ERROR_PREFIX}{error}")
        desc.color = cfg.COLOR_ERROR
    return desc

def create_load_button():
    """Создание кнопки загрузки на загрузочном экране"""
    return ft.FilledButton(
        content=cfg.TXT_LOAD_BUTTON,
        icon=ft.Icons.UPLOAD_FILE
    )

def create_toolbar(*toolbar_icons):
    return ft.Row(
        list(toolbar_icons),
        spacing=cfg.TOOLBAR_ELEMENTS_SPACING,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
    )

def create_load_icon():
    return ft.FilledIconButton(
        icon=ft.Icons.FOLDER_OPEN,
        tooltip=cfg.TIP_OPEN_CSV
    )

def create_revert_icon():
    return ft.OutlinedIconButton(
        icon=ft.Icons.RESTART_ALT,
        tooltip=cfg.TIP_REVERT
    )

def create_del_col_icon():
    return ft.OutlinedIconButton(
        icon=ft.Icons.REMOVE_ROAD,
        tooltip=cfg.TIP_DEL_COL
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
        border=ft.Border.only(
            bottom=ft.BorderSide(cfg.TABLE_OUTER_BORDERS_WIDTH, cfg.TABLE_BORDER_COLOR),
            right=ft.BorderSide(cfg.TABLE_OUTER_BORDERS_WIDTH, cfg.TABLE_BORDER_COLOR)
        ),
        horizontal_lines=ft.BorderSide(cfg.TABLE_INNER_HORIZONTAL_BORDERS_WIDTH, cfg.TABLE_BORDER_COLOR),
        vertical_lines=ft.BorderSide(cfg.TABLE_INNER_VERTICAL_BORDERS_WIDTH, cfg.TABLE_BORDER_COLOR),
        show_bottom_border=False,
        data_row_max_height=cfg.CELL_HEIGHT,
        heading_row_color=cfg.TABLE_HEADER_BG_COLOR,
        heading_row_height=cfg.HEADER_HEIGHT
    )
    
    table_column = ft.Column(
        table,
        expand=False
    )
    
    return ft.Row(
        table_column,
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
        tooltip=cfg.TIP_TO_BEGIN
    )

def create_backward_button():
    return ft.OutlinedIconButton(
        icon=ft.Icons.KEYBOARD_ARROW_LEFT,
        tooltip=cfg.TIP_BACKWARD
    )

def create_forward_button():
    return ft.OutlinedIconButton(
        icon=ft.Icons.KEYBOARD_ARROW_RIGHT,
        tooltip=cfg.TIP_FORWARD
    )

def create_to_end_button():
    return ft.OutlinedIconButton(
        icon=ft.Icons.KEYBOARD_DOUBLE_ARROW_RIGHT,
        tooltip=cfg.TIP_TO_END
    )

def create_page_info(curr_page, tot_pages):
    return ft.Text(f"Страница {curr_page} из {tot_pages}")

def create_parameters(content=None):
    if content is None:
        return ft.Text("Параметры")

def create_output():
    """Создание контейнера для лога вывода (вертикальная прокрутка)."""
    return ft.Row(
        ft.Column(
            scroll=ft.ScrollMode.AUTO,
            auto_scroll=True,   # автоматически прокручивает вниз при новых записях
            expand=True
        ),
        scroll=ft.ScrollMode.AUTO,
        expand=True
    )

def create_log_entry(message: str, timestamp: str) -> ft.Text:
    """
    Создание одной строки лога.
    Row даёт горизонтальную прокрутку для длинных сообщений.
    """
    return ft.Text(
                f"[{timestamp}]\n{message}",
                font_family=cfg.FONT_MONOSPACE,
                size=cfg.LOG_TEXT_SIZE,
                selectable=True,
                no_wrap=True,# не переносить строки
    )

def create_workspace(*workspace_args):
    return ft.Column(
        list(workspace_args),
        scroll=ft.ScrollMode.AUTO,
    )

def create_column_dropdown(df):
    """Создаёт список колонок переданного датасета"""
    column_dropdown = ft.Dropdown(
        label=cfg.LBL_COLUMN_DROPDOWN,
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
        tooltip=cfg.TIP_DELETE_FIELD,
        bgcolor=cfg.COLOR_ERROR,
    )

def create_info_button():
    """Создание иконки для получения информации о датасете."""
    return ft.OutlinedIconButton(
        icon=ft.Icons.INFO,
        tooltip=cfg.TIP_INFO
    )

def create_dataset_info_display(info_string):
    """
    Создание контейнера с отформатированной информацией о датасете.
    info_string: строка, полученная из df.info(buf=None, verbose=True, show_counts=True)
    """
    # Преобразование в текст
    info_text = ft.Text(info_string, selectable=True, font_family=cfg.FONT_MONOSPACE)
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
        tooltip=cfg.TIP_STATS
    )

def _create_toggle_icon(icon, tooltip):
    return ft.OutlinedIconButton(
        icon=icon,
        tooltip=tooltip,
        selected=False,  # Изначально не зажата
        style=ft.ButtonStyle(
            bgcolor={
                ft.ControlState.DEFAULT: cfg.COLOR_OUTLINE_BUTTON_BG, # Цвет по умолчанию
                ft.ControlState.SELECTED: cfg.COLOR_SELECTED_OUTLINE_BUTTON_BG,    # Цвет когда зажата
            },
            color={
                ft.ControlState.DEFAULT: cfg.COLOR_OUTLINE_BUTTON, # Цвет по умолчанию
                ft.ControlState.SELECTED: cfg.COLOR_SELECTED_OUTLINE_BUTTON,    # Цвет когда зажата
            }
        )
    )

def create_del_dup_icon():
    """Создание иконки для удаления дубликатов."""
    return ft.OutlinedIconButton(
        icon=ft.Icons.DELETE_SWEEP, # Иконка "метлы" / очистки
        tooltip=cfg.TIP_DEL_DUP
    )

def create_add_col_icon():
    """Иконка для тулбара: Добавить поле"""
    return ft.OutlinedIconButton(
        icon=ft.Icons.ADD_CHART,
        tooltip=cfg.TIP_ADD_COL
    )

def create_col_name_input():
    """Поле для ввода имени новой колонки"""
    return ft.TextField(
        label=cfg.LBL_COL_NAME, 
        expand=True,
        hint_text=cfg.HINT_COL_NAME
    )

def create_col_type_dropdown():
    """Дропдаун для выбора типа данных"""
    options = [
        ft.dropdown.Option(key=k, text=v) for k, v in cfg.COLUMN_TYPES.items()
    ]
    return ft.Dropdown(
        label=cfg.LBL_COL_TYPE,
        options=options,
        value="int64", # Значение по умолчанию
        expand=True,
        dense=True
    )

def create_col_value_input():
    """Поле для ввода значения или выражения"""
    return ft.TextField(
        label=cfg.LBL_COL_VALUE,
        expand=True,
        multiline=True,
        min_lines=1,
        max_lines=7,
        hint_text=cfg.HINT_COL_VALUE
    )

def create_add_col_submit_btn():
    """Кнопка подтверждения добавления"""
    return ft.FilledButton(
        content=cfg.TXT_SUBMIT_ADD_COL,
        icon=ft.Icons.CHECK
    )

def create_charts_icon():
    """Иконка в тулбар для открытия меню графиков."""
    return ft.OutlinedIconButton(
        icon=ft.Icons.SHOW_CHART,
        tooltip=cfg.TIP_CHARTS
    )

def create_chart_type_dropdown():
    """Дропдаун выбора типа графика."""
    options = [ft.dropdown.Option(key=k, text=v) for k, v in cfg.CHART_TYPES.items()]
    return ft.Dropdown(
        label=cfg.LBL_CHART_TYPE,
        options=options,
        expand=True,
        dense=True
    )

def create_numeric_column_dropdown(df):
    """Один числовой столбец (для гистограммы)."""
    cols = dtw.get_numeric_columns(df)
    options = [ft.dropdown.Option(c) for c in cols]
    return ft.Dropdown(
        label=cfg.LBL_SELECT_COLUMN,
        options=options,
        expand=True,
        dense=True
    )

def create_numeric_columns_checkboxes(df):
    """Чекбоксы для выбора нескольких числовых столбцов (для box)."""
    cols = dtw.get_numeric_columns(df)
    return ft.Column(
        controls=[ft.Checkbox(label=c) for c in cols],
        scroll=ft.ScrollMode.AUTO,
        expand=False,
        height=150,
        spacing=0
    )

def create_categorical_columns_checkboxes(df):
    """Чекбоксы для выбора нескольких категориальных столбцов (для bar)."""
    cols = dtw.get_categorical_columns(df)
    return ft.Column(
        controls=[ft.Checkbox(label=c) for c in cols],
        scroll=ft.ScrollMode.AUTO,
        expand=False,
        height=150,
        spacing=0
    )

def create_scatter_column_row(df):
    """Два дропдауна для выбора X и Y в scatter."""
    cols = dtw.get_numeric_columns(df)
    options = [ft.dropdown.Option(c) for c in cols]
    dd_x = ft.Dropdown(label=cfg.LBL_SCATTER_X, options=list(options), expand=True, dense=True)
    dd_y = ft.Dropdown(label=cfg.LBL_SCATTER_Y, options=list(options), expand=True, dense=True)
    return ft.Row([dd_x, dd_y], spacing=10)

def create_category_dropdown(df):
    """Дропдаун для выбора категориальной переменной (группировка)."""
    cols = dtw.get_categorical_columns(df)
    options = [ft.dropdown.Option(key="none", text="Не выбрано")] + [ft.dropdown.Option(c) for c in cols]
    return ft.Dropdown(
        label=cfg.LBL_CATEGORY_VAR,
        options=options,
        value="none",  # Изначально выбрано "Не выбрано"
        expand=True,
        dense=True
    )

def create_stacked_checkbox():
    """Чекбокс для переключения между графиками в ряд и с накоплением."""
    return ft.Checkbox(
        label=cfg.LBL_STACKED_HIST,
        value=False
    )

def create_build_chart_button():
    """Кнопка 'Построить'."""
    return ft.FilledButton(
        content=cfg.TXT_BUILD_CHART,
        icon=ft.Icons.SHOW_CHART
    )

def create_save_icon():
    return ft.IconButton(
        icon=ft.Icons.SAVE_ALT, # Или ft.Icons.SAVE
        tooltip=cfg.TIP_SAVE_CSV_WITH_TYPES
    )