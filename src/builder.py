# builder.py (Сборщик / Архитектор)
# Правило: Импортирует flet и ui. НЕ импортирует pandas и data.
# Задача: Собирать экраны из кирпичиков ui.py. Хранить ссылки на элементы, которые нужно будет обновлять (слоты). Принимать "коллбэки" (функции-обработчики кликов) извне.
import flet as ft
from dataclasses import dataclass
import datetime

import gui
import config as cfg

# сюда надо подавать элементы интерфейса, которые будут изменяться в процессе программы
@dataclass
class AppState:
    page: ft.Page = None
    table = None
    page_info = None
    slider = None
    table_slot = None
    parameters_slot = None
    output_slot = None
    chart_slot = None
    workspace=None
    column_dropdown = None
    
    col_name_input = None
    col_type_dropdown = None
    col_value_input = None
    col_submit_btn = None

    # --- Графики ---
    current_chart_type = None      # текущий выбранный тип графика
    chart_type_dropdown = None
    chart_columns_container = None # контейнер для выбора столбцов (обновляется)
    chart_build_btn = None
    chart_category_dropdown = None # для гистограммы и scatter
    chart_col_dd = None
    # - Работа с выбросами -
    outliers_checkboxes = None
    btn_find_outliers = None
    btn_remove_outliers = None

# сюда надо подать элементы интерфейса, которые должны быть привязаны к конкретным действиям изначально
@dataclass
class Button:
    # кнопки загрузочного экрана
    load_butt = gui.create_load_button()
    # кнопки тулбара
    load_icon = gui.create_load_icon()
    checkpoint = gui.create_save_state_icon()
    save_icon = gui.create_save_icon()
    revert_icon = gui.create_revert_icon()
    add_col_icon = gui.create_add_col_icon()
    del_col_icon = gui.create_del_col_icon()
    info_icon = gui.create_info_button()
    stats_icon = gui.create_stats_icon()
    del_dup_icon = gui.create_del_dup_icon()
    charts_icon = gui.create_charts_icon()
    outliers_icon = gui.create_outliers_icon()
    
    # кнопки переключения страниц
    to_begin = gui.create_to_begin_button()
    backward = gui.create_backward_button()
    forward = gui.create_forward_button()
    to_end = gui.create_to_end_button()

    # кнопки не требующие инициализации
    del_col = None

# Экземпляры интерфейса и кнопок
app = AppState()
btn = Button()

def show_screen(screen):
    """Обновляет экран."""
    app.page.controls = screen
    app.page.update()

def load_screen(error=None):
    """Собирает экран загрузки."""
    load_text = gui.create_load_text()
    load_desc = gui.create_load_description(error)
    
    # Упаковывание элементов в колонку
    load_column = ft.Column(
        controls=[load_text, load_desc, btn.load_butt],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=14,
    )
    # Возвращение контейнера
    return ft.Container(
        content=load_column,
        align=ft.Alignment.CENTER,
        expand=True,
        padding=cfg.LOAD_SCREEN_PADDING,
    )

def main_screen(df, curr_page, tot_pages):
    """Собирает главный экран."""
    # Тулбар
    toolbar = ft.Container(
        content=gui.create_toolbar(
            # Группа 1: Работа с файлами
            [btn.load_icon, btn.checkpoint, btn.save_icon, btn.revert_icon],
            # Группа 2: Манипуляции с данными (структура и очистка)
            [btn.add_col_icon, btn.del_col_icon, btn.del_dup_icon, btn.outliers_icon],
            # Группа 3: Анализ и визуализация
            [btn.charts_icon, btn.stats_icon, btn.info_icon]
        ),
        padding=cfg.TOOLBAR_PADDING,
        bgcolor=cfg.TOOLBAR_BGCOLOR
    )
    
    # Таблица
    app.table = ft.Container(
        content=gui.create_table(df, curr_page),
        border=ft.Border.only(
            bottom=ft.BorderSide(cfg.TABLE_OUTER_BORDERS_WIDTH, cfg.TABLE_BORDER_COLOR)
        ),
        clip_behavior=ft.ClipBehavior.HARD_EDGE
    )
  
    app.page_info = ft.Container(
        content=gui.create_page_info(curr_page, tot_pages)
    )
    
    # Слайдер для таблицы
    app.slider = ft.Container(
        content=gui.create_slider(
            btn.to_begin,
            btn.backward,
            app.page_info,
            btn.forward,
            btn.to_end
        ),
        padding=cfg.SLIDER_PADDING
    )
    
    # слот таблицы со слайдером
    app.table_slot = ft.Container(
        ft.Column(
            controls=[app.table, app.slider],
            spacing=0
        ),
        border=ft.Border.all(cfg.SLOT_BORDER_WIDTH, color=cfg.SLOT_BORDER_COLOR)
    )

    # Слоты параметров и вывода
    app.parameters_slot = ft.Container(
        content=gui.create_parameters(),
        height=cfg.PARAMETERS_SLOT_HEIGHT,
        width=cfg.PARAMETERS_SLOT_WIDTH,
        border=ft.Border.all(width=cfg.SLOT_BORDER_WIDTH, color=cfg.SLOT_BORDER_COLOR),
        padding=cfg.SLOT_PADDING,
        alignment=ft.Alignment.TOP_LEFT
    )
    
    app.output_slot = ft.Container(
        content=gui.create_output(),
        height=cfg.OUTPUT_SLOT_HEIGHT,
        # width=cfg.OUTPUT_SLOT_WIDTH,
        border=ft.Border.all(width=cfg.SLOT_BORDER_WIDTH, color=cfg.SLOT_BORDER_COLOR),
        padding=cfg.SLOT_PADDING,
        alignment=ft.Alignment.TOP_LEFT,
        expand=True
    )

    # Слот для графиков (изначально пустой, без высоты)
    app.chart_slot = ft.Container(
        height=cfg.CHART_SLOT_HEIGHT,
        width=cfg.CHART_SLOT_WIDTH,
        border=ft.Border.all(cfg.CHART_SLOT_BORDER_WIDTH, color=cfg.CHART_SLOT_BORDER_COLOR),
        padding=cfg.CHART_SLOT_PADDING,
        alignment=ft.Alignment.TOP_LEFT,
    )

    
    # Рабочая зона
    app.workspace = ft.Container(
        content=gui.create_workspace(
            app.table_slot,
            ft.Row(
                [app.parameters_slot, app.output_slot],
                expand=True,
                # scroll=ft.ScrollMode.AUTO
            ),
            app.chart_slot
        ),
        expand=True,
        padding=cfg.WORKSPACE_PADDING
    )
    
    return ft.Container(
        content=ft.Column([toolbar, app.workspace], spacing=0),
        expand=True,
        padding=cfg.MAIN_SCREEN_PADDING,
    )

def refresh_container(container, content=None):
    container.content = content
    container.update()

def append_to_log(message: str, type=None):
    """Добавляет новую запись в output_slot, не удаляя предыдущие."""
    timestamp = datetime.datetime.now().strftime("%H:%M:%S")
    # Если content ещё не инициализирован (маловероятно, но на всякий случай)
    if app.output_slot.content is None:
        app.output_slot.content = gui.create_output()
    entry = gui.create_log_entry(message, timestamp)
    if type == 'error':
        entry.color = cfg.COLOR_ERROR
    app.output_slot.content.controls.controls.append(entry)
    app.output_slot.update()