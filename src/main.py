# main.py
# Здесь происходит старт и фиксирование базовых параметров страницы.
# Всё что бы избежать циклического импорта между builder и actions.
import flet as ft

import builder as bld
import config as cfg
import actions as do

def start(page: ft.Page):
    # в билдер передаётся текущая страница и информация о ней
    bld.app.page = page
    bld.app.page.title = cfg.APP_TITLE
    bld.app.page.padding = cfg.PAGE_PADDING
    bld.app.page.theme_mode = ft.ThemeMode.LIGHT
    
    # инициализация элементов интерфейса
    bld.btn.load_butt.on_click = do.choose_file
    bld.btn.load_icon.on_click = do.choose_file
    bld.btn.revert_icon.on_click = do.revert
    bld.btn.del_col_icon.on_click = do.open_del_col_params
    bld.btn.info_icon.on_click = do.table_info
    bld.btn.stats_icon.on_click = do.show_statistics
    bld.btn.del_dup_icon.on_click = do.remove_duplicates

    bld.btn.to_begin.on_click = do.slide_table_begin
    bld.btn.backward.on_click = do.slide_table_back
    bld.btn.forward.on_click = do.slide_table_for
    bld.btn.to_end.on_click = do.slide_table_end
    
    # инициализация загрузочного экрана
    load_screen = bld.load_screen()
    bld.show_screen(load_screen)


# пуск
if __name__ == "__main__":
    ft.run(start)