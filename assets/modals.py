import flet as ft

modal_error = ft.Container(
        width=250,
        height=50,
        bgcolor=ft.colors.RED,
        padding=5,
        border_radius=15,
        alignment=ft.alignment.center,
        content=ft.Row([
            ft.Icon(ft.icons.ERROR_OUTLINE, color=ft.colors.WHITE, size=30),
            ft.Text("Ocurrió un error", color=ft.colors.WHITE, size=20)          
        ], alignment=ft.MainAxisAlignment.CENTER)
    );    
modal_correcto = ft.Container(
    width=250,
    height=50,
    bgcolor=ft.colors.GREEN,
    padding=5,
    border_radius=15,
    alignment=ft.alignment.center,
    content=ft.Row([
        ft.Icon(ft.icons.CHECK_CIRCLE_OUTLINED, color=ft.colors.WHITE, size=30),
        ft.Text("Archivo Creado", color=ft.colors.WHITE, size=20)          
    ], alignment=ft.MainAxisAlignment.CENTER)
);