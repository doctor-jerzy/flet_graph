# builder.py (Сборщик / Архитектор)
# Правило: Импортирует flet и ui. НЕ импортирует pandas и data.
# Задача: Собирать экраны из кирпичиков ui.py. Хранить ссылки на элементы, которые нужно будет обновлять (слоты). Принимать "коллбэки" (функции-обработчики кликов) извне.
import flet as ft
from dataclasses import dataclass

import gui

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
    workspace=None
    column_dropdown = None

# сюда надо подать элементы интерфейса, которые должны быть привязаны к конкретным действиям изначально
@dataclass
class Button:
    # кнопки загрузочного экрана
    load_butt = gui.create_load_button()
    # кнопки тулбара
    load_icon = gui.create_load_icon()
    revert_icon = gui.create_revert_icon()
    del_col_icon = gui.create_del_col_icon()
    info_icon = gui.create_info_button()
    stats_icon = gui.create_stats_icon()
    del_dup_icon = gui.create_del_dup_icon()
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
        padding=30,
    )

def main_screen(df, curr_page, tot_pages):
    """Собирает главный экран."""
    # Тулбар
    toolbar = ft.Container(
        content=gui.create_toolbar(
            btn.load_icon,
            btn.revert_icon,
            btn.del_col_icon,
            btn.info_icon,
            btn.stats_icon,
            btn.del_dup_icon
        ),
        padding=ft.Padding(0, 10, 0, 10),
    )

    
    # Таблица
    app.table = ft.Container(
        content=gui.create_table(df, curr_page),
        border=ft.Border.all(0.5, ft.Colors.ON_SURFACE_VARIANT),
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
        )
    )
    
    # слот таблицы со слайдером
    app.table_slot = ft.Container(
        ft.Column(
            controls=[app.table, app.slider]
        )
    )

    # Слоты параметров и вывода
    app.parameters_slot = ft.Container(
        content=gui.create_parameters(),
        height=360,
        width=450,
        border=ft.Border.all(width=1, color='outline'),
        padding=10,
        alignment=ft.Alignment.TOP_LEFT
    )
    
    app.output_slot = ft.Container(
        content=gui.create_output(),
        height=360,
        width=640,
        border=ft.Border.all(width=1, color='outline'),
        padding=10,
        alignment=ft.Alignment.TOP_LEFT
    )
    
    # Рабочая зона
    app.workspace = ft.Container(
        content=gui.create_workspace(
            app.table_slot,
            ft.Row(
                [app.parameters_slot, app.output_slot],
                expand=True,
                scroll=ft.ScrollMode.AUTO
            )
        ),
        expand=True
    )
    
    return ft.Container(
        content=ft.Column([toolbar, app.workspace]),
        expand=True,
        padding=10,
    )

def refresh_container(container, content=None):
    container.content = content
    container.update()

import datawork as dtw

def refresh_table():
    refresh_container(
        app.table,
        content=gui.create_table(dtw.var.view_df, dtw.var.curr_page)
    )