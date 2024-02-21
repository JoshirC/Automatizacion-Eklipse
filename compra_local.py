import flet as ft
import pandas as pd

class CompraLocal(ft.Container):
    def __init__(self):
        super().__init__(
            width=750, 
            height=600, 
            bgcolor=ft.colors.RED,
        )