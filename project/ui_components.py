import flet as ft
import flet_datatable2 as ftd

def create_load_screen(on_click, error_status=None):
    
    pick_button = ft.Button("Выбрать данные", on_click=on_click)    
    
    if error_status is None:
        text = ft.Text("Формат CSV")
    else:
        text = ft.Text(f"❌ Ошибка чтения файла: {error_status}")
        text.color = ft.Colors.RED
    
    load_column = ft.Column(
        [pick_button, text],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=10
    )
    load_container = ft.Container(
        content=load_column,
        align=ft.Alignment.CENTER,
        expand=True
    )
    return load_container

def create_toolbar():
    btn_open = ft.Button(
        "Открыть новый датасет", 
        on_click=None, 
        icon=ft.Icons.FOLDER_OPEN
    )
    btn_save = ft.Button(
        "Сохранить датасет", 
        on_click=None, 
        icon=ft.Icons.SAVE
    )
    
    toolbar = ft.Container(
        content=ft.Row([btn_open, btn_save], spacing=10),
        padding=10,
        bgcolor=ft.Colors.GREY_200,  # Светло-серый фон для "ленты"
        border_radius=5,
        margin=ft.Margin.only(bottom=10)  # Отступ снизу, чтобы лента не липла к таблице
    )
    
    return toolbar

def create_data_table(dataframe):
    columns = [
        ftd.DataColumn2(ft.Text(col), fixed_width=100) for col in dataframe.columns
    ]

    rows = [
            ftd.DataRow2(
                cells=[ft.DataCell(ft.Text(val)) for val in row]
            ) for _, row in dataframe.iterrows()
        ]
    
    data_table = ftd.DataTable2(columns=columns, rows=rows, checkbox_alignment=ft.Alignment.CENTER_LEFT)

    table_row = ft.Row(
        [data_table],
        scroll=ft.ScrollMode.AUTO,
        alignment=ft.MainAxisAlignment.START,
        vertical_alignment=ft.CrossAxisAlignment.START,
        expand=True  # Позволяет строке занять всё место и работать горизонтальному скроллу
    )

    table_container = ft.Container(
                content=table_row,
                expand=True,
                height=300,
                clip_behavior=ft.ClipBehavior.HARD_EDGE,
                border=ft.Border.all(width=2, color=ft.Colors.BLUE),
            )

    return table_container

def create_main_screen(dataframe):
    toolbar = create_toolbar()
    data_table = create_data_table(dataframe)
    
    screen = ft.Row(ft.Column([toolbar, data_table]))

    screen_container = ft.Container(
        content=screen,
        expand=True,
        clip_behavior=ft.ClipBehavior.HARD_EDGE,
        border=ft.Border.all(width=2, color=ft.Colors.RED)
    )

    return screen_container