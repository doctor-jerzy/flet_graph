import flet as ft
import flet_datatable2 as ftd


MAX_VISIBLE_ROWS = 500


def create_load_screen(on_click, error_status=None):
    pick_button = ft.FilledButton(
        "Выбрать CSV",
        icon=ft.Icons.UPLOAD_FILE,
        on_click=on_click,
    )

    if error_status is None:
        text = ft.Text("Откройте CSV-файл, чтобы увидеть таблицу и очистить данные.")
    else:
        text = ft.Text(f"Ошибка чтения CSV: {error_status}")
        text.color = ft.Colors.RED

    load_column = ft.Column(
        [
            ft.Text("Данные рынка недвижимости", size=28, weight=ft.FontWeight.W_600),
            text,
            pick_button,
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=14,
    )

    return ft.Container(
        content=load_column,
        align=ft.Alignment.CENTER,
        expand=True,
        padding=32,
    )


def create_data_table(dataframe):
    visible_dataframe = dataframe.head(MAX_VISIBLE_ROWS)
    columns = [
        ftd.DataColumn2(ft.Text(str(col), weight=ft.FontWeight.W_600), fixed_width=160)
        for col in visible_dataframe.columns
    ]
    rows = [
        ftd.DataRow2(
            cells=[
                ft.DataCell(ft.Text("" if value is None else str(value), no_wrap=True))
                for value in row
            ]
        )
        for _, row in visible_dataframe.iterrows()
    ]

    table = ftd.DataTable2(
        columns=columns,
        rows=rows,
        heading_row_height=44,
        data_row_height=40,
        column_spacing=18,
        horizontal_margin=16,
        border_radius=8,
        heading_row_color=ft.Colors.SURFACE_CONTAINER_HIGHEST,
        horizontal_lines=ft.BorderSide(1, ft.Colors.OUTLINE_VARIANT),
        show_bottom_border=True,
        visible_horizontal_scroll_bar=True,
        visible_vertical_scroll_bar=True,
        min_width=max(len(columns) * 160, 720),
        expand=True,
    )

    return ft.Container(
        content=table,
        expand=True,
        clip_behavior=ft.ClipBehavior.HARD_EDGE,
        border=ft.Border.all(1, ft.Colors.OUTLINE_VARIANT),
        border_radius=8,
    )


def create_main_screen(dataframe, on_open):
    source_dataframe = dataframe.copy()
    current_dataframe = dataframe.copy()

    title = ft.Text("Таблица CSV", size=24, weight=ft.FontWeight.W_600)
    subtitle = ft.Text(color=ft.Colors.ON_SURFACE_VARIANT)
    status = ft.Text(color=ft.Colors.ON_SURFACE_VARIANT)
    table_slot = ft.Container(expand=True)

    column_dropdown = ft.Dropdown(
        label="Столбец",
        width=240,
        dense=True,
        enable_search=True,
    )
    row_number = ft.TextField(
        label="Строка",
        width=120,
        dense=True,
        keyboard_type=ft.KeyboardType.NUMBER,
        hint_text="1",
    )

    def show_message(message, color=ft.Colors.ON_SURFACE_VARIANT):
        status.value = message
        status.color = color
        status.update()

    def refresh():
        column_dropdown.options = [
            ft.dropdown.Option(str(column)) for column in current_dataframe.columns
        ]
        if column_dropdown.value not in [option.key for option in column_dropdown.options]:
            column_dropdown.value = None

        subtitle.value = (
            f"{len(current_dataframe)} строк, {len(current_dataframe.columns)} столбцов"
        )
        shown = min(len(current_dataframe), MAX_VISIBLE_ROWS)
        status.value = f"Показано {shown} из {len(current_dataframe)} строк"
        status.color = ft.Colors.ON_SURFACE_VARIANT
        table_slot.content = create_data_table(current_dataframe)

    def delete_column(_):
        nonlocal current_dataframe
        if not column_dropdown.value:
            show_message("Выберите столбец для удаления.", ft.Colors.RED)
            return

        current_dataframe = current_dataframe.drop(columns=[column_dropdown.value])
        refresh()
        table_slot.update()
        column_dropdown.update()
        subtitle.update()
        status.update()

    def delete_row(_):
        nonlocal current_dataframe
        try:
            index = int(row_number.value) - 1
        except ValueError:
            show_message("Введите номер строки.", ft.Colors.RED)
            return

        if index < 0 or index >= len(current_dataframe):
            show_message("Такой строки нет.", ft.Colors.RED)
            return

        current_dataframe = current_dataframe.drop(
            current_dataframe.index[index]
        ).reset_index(drop=True)
        row_number.value = ""
        refresh()
        table_slot.update()
        row_number.update()
        column_dropdown.update()
        subtitle.update()
        status.update()

    def reset(_):
        nonlocal current_dataframe
        current_dataframe = source_dataframe.copy()
        row_number.value = ""
        refresh()
        table_slot.update()
        row_number.update()
        column_dropdown.update()
        subtitle.update()
        status.update()

    refresh()

    toolbar = ft.Container(
        content=ft.Row(
            [
                ft.FilledButton(
                    "Открыть CSV",
                    icon=ft.Icons.FOLDER_OPEN,
                    on_click=on_open,
                ),
                ft.OutlinedButton("Сбросить", icon=ft.Icons.RESTART_ALT, on_click=reset),
                column_dropdown,
                ft.OutlinedButton(
                    "Удалить столбец",
                    icon=ft.Icons.VIEW_COLUMN,
                    on_click=delete_column,
                ),
                row_number,
                ft.OutlinedButton(
                    "Удалить строку",
                    icon=ft.Icons.TABLE_ROWS,
                    on_click=delete_row,
                ),
            ],
            spacing=10,
            wrap=True,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        padding=ft.Padding(0, 10, 0, 10),
    )

    return ft.SafeArea(
        content=ft.Container(
            content=ft.Column(
                [
                    ft.Row(
                        [ft.Column([title, subtitle], spacing=2), status],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        vertical_alignment=ft.CrossAxisAlignment.END,
                    ),
                    toolbar,
                    table_slot,
                ],
                expand=True,
                spacing=8,
            ),
            expand=True,
            padding=24,
        ),
        expand=True,
    )
