import flet as ft
import pandas as pd

from ui_components import (
    create_load_screen,
    create_main_screen
)

def main(page: ft.Page):
    page.title = "Анализ рынка недвижимости №13"
    page.padding = 0
    page.theme_mode = ft.ThemeMode.LIGHT

    async def on_file_picked(e):
        files = await ft.FilePicker().pick_files(
            allow_multiple=False,
            allowed_extensions=["csv"],
            dialog_title="Выберите файл с данными",
        )

        if not files:
            return

        try:
            dataframe = pd.read_csv(files[0].path)
        except Exception as ex:
            page.controls.clear()
            page.add(create_load_screen(on_click=on_file_picked, error_status=ex))
            page.update()
            return

        page.controls.clear()
        page.add(create_main_screen(dataframe, on_open=on_file_picked))
        page.update()

    page.add(create_load_screen(on_click=on_file_picked))

# ft.run(main, host="127.0.0.1", port=8550, view=ft.AppView.FLET_APP)
ft.run(main)