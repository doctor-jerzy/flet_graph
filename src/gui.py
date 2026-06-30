# ui.py
import flet as ft

import datawork as dtw
import config as cfg

# --- Вспомогательная функция для создания минималистичных иконок ---
def _create_icon(icon, tooltip):
    return ft.IconButton(
        icon=icon,
        tooltip=tooltip,
        icon_size=cfg.TOOLBAR_ICON_SIZE,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=8),
            padding=10,
            color={
                ft.ControlState.DEFAULT: cfg.COLOR_OUTLINE_BUTTON,
                ft.ControlState.HOVERED: ft.Colors.PRIMARY, # При наведении иконка становится цветной
            },
            bgcolor={
                ft.ControlState.HOVERED: cfg.COLOR_HOVER_BG, # Легкий фон при наведении
            }
        )
    )

# --- Стиль для кнопки-переключателя (Статистика) ---
def _create_toggle_icon(icon, tooltip):
    return ft.IconButton(
        icon=icon,
        tooltip=tooltip,
        selected=False,
        icon_size=cfg.TOOLBAR_ICON_SIZE,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=8),
            padding=10,
            color={
                ft.ControlState.DEFAULT: cfg.COLOR_OUTLINE_BUTTON,
                ft.ControlState.HOVERED: ft.Colors.PRIMARY,
                ft.ControlState.SELECTED: cfg.COLOR_SELECTED_OUTLINE_BUTTON
            },
            bgcolor={
                ft.ControlState.HOVERED: cfg.COLOR_HOVER_BG,
                ft.ControlState.SELECTED: cfg.COLOR_SELECTED_OUTLINE_BUTTON_BG
            }
        )
    )

def _create_dropdown(options:list|None=None, label: str|None = None, value=None):
    """Создаёт дропдаун"""
    return ft.Dropdown(
        value=value,
        options=options,
        leading_icon=ft.Icons.SEARCH,
        label=label,
        label_style=ft.TextStyle(size=14),
        editable=True,
        enable_search=True,
        enable_filter=True,
        text_size=14,
        menu_height=200,
        dense=True,
        content_padding=0,
        expand=True
    )

def _create_textfield(label:str, hint_text:str|None=None, **kwargs):
    return ft.TextField(
        label=label, 
        label_style=ft.TextStyle(size=14),
        hint_text=hint_text,
        text_size=14,
        expand=True
    )

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

def create_toolbar(*icon_groups):
    """Создает тулбар, разделяя иконки на логические группы вертикальными разделителями."""
    controls = []
    for group in icon_groups:
        for i in group:
            controls.append(i)
        controls.append(
            ft.Container(ft.VerticalDivider(color=cfg.TOOLBAR_DIVIDER_COLOR), height=24)
        )
    controls = controls[:-1]
    return ft.Row(
        controls=controls,
        spacing=cfg.TOOLBAR_ELEMENTS_SPACING,
        vertical_alignment=ft.CrossAxisAlignment.CENTER
    )

# --- Иконки тулбара (заменяем OutlinedIconButton на _create_minimalist_icon) ---
def create_load_icon():
    # Кнопка открытия файла остается выделенной (Filled), это главное действие
    return ft.FilledIconButton(
        icon=ft.Icons.FOLDER_OPEN,
        tooltip=cfg.TIP_OPEN_CSV,
        icon_size=cfg.TOOLBAR_ICON_SIZE,
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8), padding=10)
    )

def create_save_state_icon():
    """Иконка для фиксации текущего состояния датасета как исходного."""
    return _create_icon(icon=ft.Icons.SAVE_AS, tooltip=cfg.TIP_SAVE_STATE)

def create_save_icon():
    return _create_icon(ft.Icons.SAVE_ALT, cfg.TIP_SAVE_CSV_WITH_TYPES)

def create_revert_icon():
    return _create_icon(ft.Icons.RESTART_ALT, cfg.TIP_REVERT)

def create_del_col_icon():
    return _create_icon(ft.Icons.REMOVE, cfg.TIP_DEL_COL)

def create_info_button():
    return _create_icon(ft.Icons.INFO_OUTLINE, cfg.TIP_INFO)

def create_stats_icon():
    """Создание иконки-переключателя для показа статистики."""
    return _create_toggle_icon(ft.Icons.QUERY_STATS, cfg.TIP_STATS)

def create_del_dup_icon():
    """Создание иконки для удаления дубликатов."""
    return _create_icon(ft.Icons.DELETE_SWEEP, cfg.TIP_DEL_DUP)

def create_add_col_icon():
    """Иконка для тулбара: Добавить поле"""
    return _create_icon(ft.Icons.ADD, cfg.TIP_ADD_COL)

def create_charts_icon():
    """Иконка в тулбар для открытия меню графиков."""
    return _create_icon(ft.Icons.INSERT_CHART_OUTLINED_OUTLINED, cfg.TIP_CHARTS)

def create_outliers_icon():
    """Иконка в тулбар для работы с выбросами."""
    return _create_icon(
        ft.Icons.SCATTER_PLOT, # Или ft.Icons.FILTER_ALT, ft.Icons.WARNING_AMBER_ROUNDED
        cfg.TIP_OUTLIERS
    )

def create_table(df, curr_page):
    """Создаёт ВИДИМУЮ часть таблицы на основе переданного датафрейма"""
    if df.empty:
        return ft.Container(
            content=ft.Text(
                "ДАТАФРЕЙМ ПУСТ", 
                size=26,  # Увеличиваем размер шрифта
                weight=ft.FontWeight.BOLD,
                color=cfg.SLOT_BORDER_COLOR  # Мягкий серый цвет для состояния "пусто"
            ),
            height=cfg.TABLE_HEIGHT,
            alignment=ft.Alignment.CENTER,  # Центрирует текст внутри контейнера
            expand=True,  # Растягивает контейнер на всю ширину слота, чтобы центрирование сработало и по горизонтали
        )
    
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
        return ft.Text("Параметры", size=cfg.SLOT_TITLE_TEXT_SIZE, color=cfg.SLOT_BORDER_COLOR)

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
                color=ft.Colors.ON_SURFACE_VARIANT,
                selectable=True,
                no_wrap=True# не переносить строки
    )

def create_workspace(*workspace_args):
    return ft.Column(
        list(workspace_args),
        scroll=ft.ScrollMode.AUTO,
    )

def create_del_col_dropdown(df):
    """Создаёт список колонок переданного датасета"""
    if not df.empty:
        options = [ft.dropdown.Option(str(column)) for column in df.columns]
    else:
        options=None
    return _create_dropdown(options, label=cfg.LBL_DEL_COL_DROPDOWN)

def create_delete_button():
    return ft.FilledIconButton(
        icon=ft.Icons.DELETE,
        tooltip=cfg.TIP_DELETE_FIELD,
        bgcolor=cfg.COLOR_ERROR,
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



def create_col_name_input():
    """Поле для ввода имени новой колонки"""
    return _create_textfield(cfg.LBL_COL_NAME_INPUT, cfg.HINT_COL_NAME_INPUT)

def create_col_type_dropdown():
    """Дропдаун для выбора типа данных"""
    options = [
        ft.dropdown.Option(key=k, text=v) for k, v in cfg.COLUMN_TYPES.items()
    ]
    return _create_dropdown(options, label=cfg.LBL_COL_TYPE_DROPDOWN, value=list(cfg.COLUMN_TYPES.keys()))

def create_col_value_input():
    """Поле для ввода значения или выражения"""
    return _create_textfield(
        label=cfg.LBL_COL_VALUE_INPUT,
        hint_text=cfg.HINT_COL_VALUE_INPUT,
        multiline=True,
        min_lines=1,
        max_lines=7
    )

def create_add_col_submit_btn():
    """Кнопка подтверждения добавления"""
    return ft.FilledButton(
        content=cfg.TXT_SUBMIT_ADD_COL,
        icon=ft.Icons.CHECK
    )

def create_chart_type_dropdown():
    """Дропдаун выбора типа графика."""
    options = [ft.dropdown.Option(key=k, text=v) for k, v in cfg.CHART_TYPES.items()]
    return _create_dropdown(options, label=cfg.LBL_CHART_TYPE_DROPDOWN)

def create_numeric_column_dropdown(df):
    """Один числовой столбец (для гистограммы)."""
    cols = dtw.get_numeric_columns(df)
    options = [ft.dropdown.Option(c) for c in cols]
    return _create_dropdown(options, label=cfg.LBL_SELECT_COLUMN_DROPDOWN)

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
    dd_x = _create_dropdown(options, cfg.LBL_SCATTER_X_DROPDOWN)
    dd_y = _create_dropdown(options, cfg.LBL_SCATTER_X_DROPDOWN)
    return ft.Row([dd_x, dd_y], spacing=10)

def create_category_dropdown(df):
    """Дропдаун для выбора категориальной переменной (группировка)."""
    cols = dtw.get_categorical_columns(df)
    options = [ft.dropdown.Option(key="none", text="Не выбрано")] + [ft.dropdown.Option(c) for c in cols]
    return _create_dropdown(options, cfg.LBL_CATEGORY_COL_DROPDOWN)

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

def create_find_outliers_btn():
    """Кнопка 'Определить выбросы'."""
    return ft.FilledButton(
        content=cfg.TXT_FIND_OUTLIERS,
        icon=ft.Icons.SEARCH,
        
    )

def create_remove_outliers_btn():
    """Кнопка 'Удалить выбросы'."""
    return ft.FilledButton(
        content=cfg.TXT_REMOVE_OUTLIERS,
        icon=ft.Icons.DELETE_SWEEP,
        bgcolor=cfg.COLOR_ERROR # Если у тебя есть красный цвет для опасных действий
    )