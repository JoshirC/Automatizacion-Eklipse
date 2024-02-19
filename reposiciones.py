import flet as ft
import pandas as pd

class Reposiciones(ft.Container):
    def __init__(self):
        super().__init__(
            width=750, 
            height=600, 
            bgcolor=ft.colors.BLACK,
        )