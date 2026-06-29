# actions.py
import flet as ft
import flet_charts as fch
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
        df = dtw.load_csv_with_dtypes(path)
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
    bld.append_to_log(f"Файл загружен: {path}\nСтрок: {len(df)}, Столбцов: {len(df.columns)}")

async def save_file(e):
    """Обработчик сохранения датасета и его типов."""
    if dtw.var.work_df is None or dtw.var.work_df.empty:
        bld.append_to_log("Нечего сохранять: датасет пуст или не загружен.", type='error')
        return

    # Открываем диалог сохранения
    file = await ft.FilePicker().save_file(
        file_name="saved_data.csv",
        allowed_extensions=cfg.CSV_EXTENSIONS,
        dialog_title="Сохранить датасет и типы столбцов",
    )
    
    if not file:
        return # Пользователь отменил

    path = file
    try:
        # Вызываем функцию из datawork
        dtw.save_df_with_dtypes(dtw.var.work_df, path)
        bld.append_to_log(f"Успешно сохранено: {path}\n(и файл типов .dtypes.json)")
    except Exception as ex:
        bld.append_to_log(f"Ошибка при сохранении: {ex}", type='error')

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
    col_name = bld.app.column_dropdown.value
    df = dtw.var.work_df.drop(columns=[col_name])
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
    bld.append_to_log(f"Удалён столбец: '{col_name}'")

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
        content=gui.create_parameters()
    )
    bld.append_to_log("Изменения откатаны до исходного состояния")

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
        bld.append_to_log("Датасет не загружен или пуст.", type='error')
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
            bld.append_to_log(info_str)
        except Exception as info_error:
            # Обработка возможных ошибок при получении информации
            bld.append_to_log(f"Ошибка при получении информации о датасете: {info_error}", type='error')

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
    bld.append_to_log(f"Удалено строк: {removed_count} из {initial_count}, стало {len(df)}")

def open_add_col_params(e):
    """Открывает панель параметров для добавления колонки."""
    # Инициализируем элементы и сохраняем их в слоты builder
    bld.app.col_name_input = gui.create_col_name_input()
    bld.app.col_type_dropdown = gui.create_col_type_dropdown()
    bld.app.col_value_input = gui.create_col_value_input()
    bld.app.col_submit_btn = gui.create_add_col_submit_btn()
    
    # Привязываем обработчик к кнопке "Добавить"
    bld.app.col_submit_btn.on_click = submit_add_col

    # Собираем UI в слоте параметров
    bld.refresh_container(
        bld.app.parameters_slot,
        content=ft.Column(
            controls=[
                bld.app.col_name_input,
                bld.app.col_type_dropdown,
                bld.app.col_value_input,
                bld.app.col_submit_btn
            ],
            spacing=15,
            expand=True
        )
    )

def submit_add_col(e):
    """Обработчик нажатия кнопки 'Добавить' в панели параметров."""
    col_name = bld.app.col_name_input.value
    col_type = bld.app.col_type_dropdown.value
    expr = bld.app.col_value_input.value

    # Валидация ввода
    if not col_name or not col_name.strip():
        bld.append_to_log("Ошибка: Введите имя колонки.", type='error')
        return
    if not expr or not expr.strip():
        bld.append_to_log("Ошибка: Введите значение или выражение.", type='error')
        return

    col_name = col_name.strip()
    
    # Вызываем функцию из datawork
    new_df, success, msg = dtw.add_column_with_expr(
        dtw.var.work_df, col_name, col_type, expr
    )

    if success:
        # Если всё прошло успешно, обновляем данные и интерфейс
        dtw.var.work_df = new_df
        set_work_params(new_df, dtw.var.work_page)
        set_view_params(dtw.var.work_page)
        
        bld.refresh_container(bld.app.table, content=gui.create_table(dtw.var.view_df, dtw.var.curr_page))
        bld.refresh_container(bld.app.page_info, content=gui.create_page_info(dtw.var.curr_page, dtw.var.tot_pages))
        
        bld.append_to_log(msg)
        
        # Очищаем поля ввода для удобства
        bld.app.col_name_input.value = ""
        bld.app.col_value_input.value = ""
        bld.app.col_name_input.update()
        bld.app.col_value_input.update()
    else:
        # Если произошла ошибка (неверный тип, синтаксис и т.д.) - пишем в лог
        bld.append_to_log(msg, type='error')



# =================== ГРАФИКИ ===================

def open_chart_params(e):
    """Открывает меню выбора типа графика в parameters_slot."""
    if dtw.var.work_df is None or dtw.var.work_df.empty:
        bld.append_to_log("Сначала загрузите датасет.", type='error')
        return

    bld.app.current_chart_type = None
    bld.app.chart_type_dropdown = gui.create_chart_type_dropdown()
    bld.app.chart_type_dropdown.on_select = on_chart_type_select

    # Контейнер для динамического содержимого (выбор столбцов)
    bld.app.chart_columns_container = ft.Container()
    bld.app.chart_category_dropdown = None
    bld.app.chart_build_btn = None

    bld.refresh_container(
        bld.app.parameters_slot,
        content=ft.Column(
            controls=[
                ft.Text("Построение графика", weight=ft.FontWeight.BOLD),
                bld.app.chart_type_dropdown,
                bld.app.chart_columns_container,
            ],
            spacing=15,
            scroll=ft.ScrollMode.AUTO,
            expand=True
        )
    )

def on_chart_type_select(e):
    """Реагирует на смену типа графика — перестраивает UI выбора столбцов."""
    chart_type = e.control.value
    bld.app.current_chart_type = chart_type
    bld.app.chart_category_dropdown = None
    bld.app.chart_stacked_checkbox = None
    bld.app.chart_stacked_container = None

    df = dtw.var.work_df
    controls = []

    if chart_type == "hist":
        if not dtw.get_numeric_columns(df):
            controls.append(ft.Text(cfg.TXT_NO_NUMERIC_COLS, color=cfg.COLOR_ERROR))
        else:
            bld.app.chart_col_dd = gui.create_numeric_column_dropdown(df)
            controls.append(bld.app.chart_col_dd)
            # Доп. опция — категориальный столбец для группировки
            bld.app.chart_category_dropdown = gui.create_category_dropdown(df)
            bld.app.chart_category_dropdown.on_select = on_hist_category_select
            controls.append(bld.app.chart_category_dropdown)
            # Пустой контейнер, куда позже положим чекбокс
            bld.app.chart_stacked_container = ft.Container()
            controls.append(bld.app.chart_stacked_container)

    elif chart_type == "box":
        if not dtw.get_numeric_columns(df):
            controls.append(ft.Text(cfg.TXT_NO_NUMERIC_COLS, color=cfg.COLOR_ERROR))
        else:
            controls.append(ft.Text(cfg.LBL_SELECT_COLUMNS))
            bld.app.chart_checkboxes = gui.create_numeric_columns_checkboxes(df)
            controls.append(bld.app.chart_checkboxes)

    elif chart_type == "bar":
        if not dtw.get_categorical_columns(df):
            controls.append(ft.Text(cfg.TXT_NO_CATEGORICAL_COLS, color=cfg.COLOR_ERROR))
        else:
            controls.append(ft.Text(cfg.LBL_SELECT_COLUMNS))
            bld.app.chart_checkboxes = gui.create_categorical_columns_checkboxes(df)
            controls.append(bld.app.chart_checkboxes)

    elif chart_type == "scatter":
        if len(dtw.get_numeric_columns(df)) < 2:
            controls.append(ft.Text("Нужно минимум 2 числовых столбца", color=cfg.COLOR_ERROR))
        else:
            scatter_row = gui.create_scatter_column_row(df)
            bld.app.chart_dd_x = scatter_row.controls[0]
            bld.app.chart_dd_y = scatter_row.controls[1]
            controls.append(scatter_row)
            # Доп. опция — категориальный столбец для раскраски
            bld.app.chart_category_dropdown = gui.create_category_dropdown(df)
            controls.append(bld.app.chart_category_dropdown)

    # Кнопка "Построить"
    bld.app.chart_build_btn = gui.create_build_chart_button()
    bld.app.chart_build_btn.on_click = build_chart
    controls.append(bld.app.chart_build_btn)

    bld.refresh_container(
        bld.app.chart_columns_container,
        content=ft.Column(controls=controls, spacing=10)
    )

def on_hist_category_select(e):
    """Реагирует на выбор категориального столбца для гистограммы."""
    # Если выбрана конкретная категория (не "none") — показываем чекбокс
    if e.control.value and e.control.value != "none":
        bld.app.chart_stacked_checkbox = gui.create_stacked_checkbox()
        bld.refresh_container(
            bld.app.chart_stacked_container,
            content=bld.app.chart_stacked_checkbox
        )
    else:
        # Если выбрано "Не выбрано" — убираем чекбокс
        bld.refresh_container(
            bld.app.chart_stacked_container,
            content=None
        )
        bld.app.chart_stacked_checkbox = None

def build_chart(e):
    """Считывает выбор пользователя и строит график."""
    chart_type = bld.app.current_chart_type
    df = dtw.var.work_df

    fig = None
    msg = ""

    try:
        if chart_type == "hist":
            col = bld.app.chart_col_dd.value
            if not col:
                bld.append_to_log(cfg.TXT_SELECT_AT_LEAST_ONE, type='error')
                return
            # Обработка "Не выбрано"
            hue_col = bld.app.chart_category_dropdown.value
            if hue_col == "none" or not hue_col:
                hue_col = None
            
            # Проверяем состояние чекбокса (если он существует)
            is_stacked = False
            if hasattr(bld.app, 'chart_stacked_checkbox') and bld.app.chart_stacked_checkbox is not None:
                is_stacked = bld.app.chart_stacked_checkbox.value

            fig = dtw.build_hist_figure(df, col, hue_col, stacked=is_stacked)
            # Формируем сообщение для лога
            msg = f"Построена гистограмма: {col}"
            if hue_col:
                msg += f" (группировка: {hue_col})"
                if is_stacked:
                    msg += " [с накоплением]"

        elif chart_type == "box":
            selected = [cb.label for cb in bld.app.chart_checkboxes.controls if cb.value]
            if not selected:
                bld.append_to_log(cfg.TXT_SELECT_AT_LEAST_ONE, type='error')
                return
            fig = dtw.build_box_figure(df, selected)
            msg = f"Построен box plot: {', '.join(selected)}"

        elif chart_type == "bar":
            selected = [cb.label for cb in bld.app.chart_checkboxes.controls if cb.value]
            if not selected:
                bld.append_to_log(cfg.TXT_SELECT_AT_LEAST_ONE, type='error')
                return
            fig = dtw.build_bar_figure(df, selected)
            msg = f"Построен bar plot: {', '.join(selected)}"

        elif chart_type == "scatter":
            col_x = bld.app.chart_dd_x.value
            col_y = bld.app.chart_dd_y.value
            if not col_x or not col_y:
                bld.append_to_log(cfg.TXT_SELECT_TWO_COLS, type='error')
                return
            if col_x == col_y:
                bld.append_to_log("Оси X и Y должны различаться", type='error')
                return
            hue_col = bld.app.chart_category_dropdown.value
            if hue_col == "none" or not hue_col:
                hue_col = None
            fig = dtw.build_scatter_figure(df, col_x, col_y, hue_col)
            msg = f"Построен scatter: {col_x} vs {col_y}" + (f" (hue: {hue_col})" if hue_col else "")

        # Выводим график в chart_slot
        bld.refresh_container(
            bld.app.chart_slot,
            content=fch.MatplotlibChart(figure=fig, expand=True)
        )
        bld.append_to_log(msg)

    except Exception as ex:
        bld.append_to_log(f"Ошибка построения графика: {ex}", type='error')
