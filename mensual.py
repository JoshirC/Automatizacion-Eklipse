import flet as ft
import pandas as pd

class Consolidado(ft.Container):
    def __init__(self):
        super().__init__(
            width=650, 
            height=600, 
            bgcolor=ft.colors.BLACK,
        )