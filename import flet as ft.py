import flet as ft

def main(page: ft.Page):
    page.title = "Clickable DataTable Example"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    # Action to run when a row is clicked
    def row_clicked(e, item_id, item_name):
        print(f"Clicked Item ID: {item_id}, Name: {item_name}")
        page.snack_bar = ft.SnackBar(ft.Text(f"Selected: {item_name}"))
        page.snack_bar.open = True
        page.update()

    # Data to display
    rows_data = [
        {"id": 1, "name": "Flet Framework", "category": "GUI"},
        {"id": 2, "name": "Python", "category": "Language"},
        {"id": 3, "name": "VS Code", "category": "Editor"}
    ]

    # Dynamically generate rows
    data_rows = []
    for row in rows_data:
        data_rows.append(
            ft.DataRow(
                cells=[
                    ft.DataCell(
                        ft.Container(
                            content=ft.Text(str(row["id"])),
                            on_click=lambda e, r=row: row_clicked(e, r["id"], r["name"])
                        )
                    ),
                    ft.DataCell(
                        ft.Container(
                            content=ft.Text(row["name"]),
                            on_click=lambda e, r=row: row_clicked(e, r["id"], r["name"])
                        )
                    ),
                    ft.DataCell(
                        ft.Container(
                            content=ft.Text(row["category"]),
                            on_click=lambda e, r=row: row_clicked(e, r["id"], r["name"])
                        )
                    ),
                ],
            )
        )

    table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("ID")),
            ft.DataColumn(ft.Text("Name")),
            ft.DataColumn(ft.Text("Category")),
        ],
        rows=data_rows,
    )

    page.add(table)

ft.app(target=main)