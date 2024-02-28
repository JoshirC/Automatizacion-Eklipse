import flet as ft

from menu import Menu
def main(page: ft.Page):
    page.title = "EKLIPSE - Sistema de Información de Compras y Reposiciones"
    page.window_width = 1000
    page.window_height = 600
    page.window_resizable = False
    page.window_maximizable = False
    page.padding = 0
    page.theme_mode = ft.ThemeMode.LIGHT
    page.update()

    menu = Menu()
    # add application's root control to the page
    page.add(
        menu,
        ) 

ft.app(target=main)
