import flet as ft
import flet_datatable2 as ftd
import pandas as pd

from ui_components import (
    create_load_screen,
    create_data_table,
    create_main_screen
)

def main(page: ft.Page):
    # Параметры страницы
    page.title = "Анализ рынка недвижимости №13"
    
    # Переменные
    df = None
    
    async def on_file_picked(e):

        nonlocal df
        
        file = await ft.FilePicker().pick_files(
            allow_multiple=False,           # только 1 файл
            allowed_extensions=["csv"],     # только CSV
            dialog_title="Выберите файл с данными"
        )

        if file:
            file_path = file[0].path 
            
            try:
                df = pd.read_csv(file_path)
                
                load_screen.visible = False
                main_screen = create_main_screen(df)
                page.add(main_screen)
                
            except Exception as ex:
                create_load_screen(on_click=on_file_picked, error_status=ex)
            
            page.update()
    
    # Базовые элементы экрана (кнопки и тп)
    load_screen = create_load_screen(on_click=on_file_picked)
    
    
    # Комплексные элементы экрана (области, контейнеры)
    

    
    
    # Отображение
    page.add(load_screen)

ft.run(main)