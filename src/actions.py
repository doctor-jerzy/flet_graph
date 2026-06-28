# actions.py
import flet as ft
from dataclasses import dataclass
import io
import sys

import builder as bld
import gui
import datawork as dtw
import config as cfg

# def example(e):
#   проводим внутренние манипуляции
#   обновляем данные bld
#   обновляем данные dtw

def toggle_button(e):
    if e is not None:
        e.control.selected = not e.control.selected
        e.control.update()
    return e

def off_button(e):
    if e is not None:
        e.control.selected = False
        e.control.update()
    return e

def e_selected(e: ft.ControlEventHandler | None):
    if e is None:
        return False
    else:
        return e.control.selected

@dataclass
class Handler:
    show_stats: ft.ControlEventHandler | None = None

on = Handler()

def set_work_params(df, curr_page=1):
    dtw.var.work_df = df.copy()
    dtw.var.work_page, dtw.var.tot_pages = dtw.get_pages(df, curr_page)

def set_view_params(curr_page=1):
    if e_selected(on.show_stats):
        # Считаем статистику заново (чтобы она была актуальной после удалений)
        # reset_index() превращает индекс (count, mean...) в обычный столбец
        if not dtw.var.work_df.empty:
            view_df = dtw.var.work_df.describe().round(2).reset_index().rename(columns={'index': 'Метрика'})
        else:
            view_df = dtw.var.work_df
        dtw.var.work_page = dtw.var.curr_page
        curr_page = 1
    else:
        view_df = dtw.var.work_df.copy()
        dtw.var.work_page = curr_page
    
    dtw.var.view_df = view_df
    dtw.var.curr_page, dtw.var.tot_pages = dtw.get_pages(view_df, curr_page)

async def choose_file(e):
    # внутртенние манипуляции: обработка файла, получение пути и датафрейма
    file = await ft.FilePicker().pick_files(
        allow_multiple=False,
        allowed_extensions=cfg.CSV_EXTENSIONS,
        dialog_title=cfg.CSV_DIALOG_TITLE,
    )
    if not file:
        return
    path = file[0].path
    try:
        # если какая-то ошибка при загрузке датафрейма, это всплывёт
        df = dtw.load_csv(path)
    except Exception as ex:
        # если ошибка, dtw не обновляется, сразу загрузочный экран с ошибкой
        screen = bld.load_screen(error=ex)
        bld.show_screen(screen)
        return
    # если ошибки не было — обновление и данных,..
    dtw.var.orig_df = df.copy()
    set_work_params(df, 1)
    set_view_params(1)
    # ...и скрина
    screen = bld.main_screen(df, dtw.var.curr_page, dtw.var.tot_pages)
    bld.show_screen(screen)


def open_del_col_params(e):
    bld.app.column_dropdown = gui.create_column_dropdown(dtw.var.work_df)
    
    bld.btn.del_col = gui.create_delete_button()
    bld.btn.del_col.on_click = delete_column
    
    bld.refresh_container(
        bld.app.parameters_slot,
        content=ft.Row([bld.app.column_dropdown, bld.btn.del_col])
    )


def delete_column(e):
    if bld.app.column_dropdown.value is None:
        return
    # обновление dtw
    # рабочий датафрейм
    df = dtw.var.work_df.drop(columns=[bld.app.column_dropdown.value])
    set_work_params(df, dtw.var.work_page)
    set_view_params(dtw.var.work_page)
    
    # обнови слот параметров, чтоб лишнюю колонку убрать
    bld.app.column_dropdown = gui.create_column_dropdown(dtw.var.work_df)
    bld.refresh_container(
        bld.app.parameters_slot,
        content=ft.Row([bld.app.column_dropdown, bld.btn.del_col])
    )

    bld.refresh_container(
        bld.app.table,
        content=gui.create_table(dtw.var.view_df, dtw.var.curr_page)
    )
    bld.refresh_container(
        bld.app.page_info,
        content=gui.create_page_info(dtw.var.curr_page, dtw.var.tot_pages)
    )

def revert(e):
    # возврат к оригинальным данным dtw
    on.show_stats = off_button(on.show_stats)
    
    set_work_params(dtw.var.orig_df, 1)
    set_view_params(1)
    
    bld.refresh_container(
        bld.app.table,
        content=gui.create_table(dtw.var.view_df, dtw.var.curr_page)
    )
    bld.refresh_container(
        bld.app.page_info,
        content=gui.create_page_info(dtw.var.curr_page, dtw.var.tot_pages)
    )
    # И слоты с параметрами и выхлопом тоже обновить надо, чтобы они вернулись к изначальному состоянию
    # здесь я просто заглушку текста сделал, НАДО БУДЕТ ЧЕРЕЗ КОНФИГИ ЭТО НАСТРОИТЬ
    bld.refresh_container(
        bld.app.parameters_slot,
        content=ft.Text("Откатилось")
    )
    bld.refresh_container(
        bld.app.output_slot,
        content=ft.Text("Откатилось")
    )

def slide_table_begin(e):
    set_view_params(1)
    
    bld.refresh_container(
        bld.app.table,
        content=gui.create_table(dtw.var.view_df, dtw.var.curr_page)
    )
    bld.refresh_container(
        bld.app.page_info,
        content=gui.create_page_info(dtw.var.curr_page, dtw.var.tot_pages)
    )

def slide_table_back(e):
    set_view_params(dtw.var.curr_page - 1)
    
    bld.refresh_container(
        bld.app.table,
        content=gui.create_table(dtw.var.view_df, dtw.var.curr_page)
    )
    bld.refresh_container(
        bld.app.page_info,
        content=gui.create_page_info(dtw.var.curr_page, dtw.var.tot_pages)
    )

def slide_table_for(e):
    set_view_params(dtw.var.curr_page + 1)
    
    bld.refresh_container(
        bld.app.table,
        content=gui.create_table(dtw.var.view_df, dtw.var.curr_page)
    )
    bld.refresh_container(
        bld.app.page_info,
        content=gui.create_page_info(dtw.var.curr_page, dtw.var.tot_pages)
    )

def slide_table_end(e):
    set_view_params(dtw.var.tot_pages)

    bld.refresh_container(
        bld.app.table,
        content=gui.create_table(dtw.var.view_df, dtw.var.curr_page)
    )
    bld.refresh_container(
        bld.app.page_info,
        content=gui.create_page_info(dtw.var.curr_page, dtw.var.tot_pages)
    )

def table_info(e):
    """Обработчик нажатия на кнопку информации о датасете."""
    if dtw.var.work_df is None or dtw.var.work_df.empty:
        # Если датафрейм пуст или не загружен, сообщение
        info_content = ft.Text("Датасет не загружен или пуст.", color=ft.Colors.RED)
    else:
        try:
            # Перехват вывода info() в строку
            buffer = io.StringIO()
            # sys.stdout для перенаправления вывода info()
            old_stdout = sys.stdout
            sys.stdout = buffer
            dtw.var.work_df.info() # подробная информация
            sys.stdout = old_stdout # восстановление вывода
            info_str = buffer.getvalue()

            # создание текстового контейнера
            info_content = gui.create_dataset_info_display(info_str)
        except Exception as info_error:
            # Обработка возможных ошибок при получении информации
            info_content = ft.Text(f"Ошибка при получении информации о датасете: {info_error}", color=ft.Colors.ERROR)

    # Обновление слота параметров с новым содержимым
    bld.refresh_container(
        bld.app.parameters_slot,
        content=info_content
    )

def show_statistics(e):
    on.show_stats = toggle_button(e)
    
    set_view_params(dtw.var.work_page)
    
    # Перерисовываем таблицу с учётом нового состояния
    bld.refresh_container(
        bld.app.table,
        content=gui.create_table(dtw.var.view_df, dtw.var.curr_page)
    )
    bld.refresh_container(
        bld.app.page_info,
        content=gui.create_page_info(dtw.var.curr_page, dtw.var.tot_pages)
    )

def remove_duplicates(e):
    """Обработчик удаления дубликатов."""
    if dtw.var.work_df is None or dtw.var.work_df.empty:
        return

    # 1. Считаем, сколько было строк до очистки
    initial_count = len(dtw.var.work_df)
    
    # 2. Применяем логику из datawork
    df = dtw.drop_duplicates(dtw.var.work_df)
    removed_count = initial_count - len(df)

    # 3. Обновляем рабочие и просмотровые данные
    set_work_params(df, dtw.var.work_page)
    set_view_params(dtw.var.work_page)

    # 4. Обновляем таблицу и информацию о страницах
    bld.refresh_container(
        bld.app.table,
        content=gui.create_table(dtw.var.view_df, dtw.var.curr_page)
    )
    bld.refresh_container(
        bld.app.page_info,
        content=gui.create_page_info(dtw.var.curr_page, dtw.var.tot_pages)
    )

    # 5. Пишем результат в слот вывода
    bld.refresh_container(
        bld.app.output_slot,
        content=ft.Text(f"Удалено дубликатов: {removed_count}", color=ft.Colors.GREEN)
    )




