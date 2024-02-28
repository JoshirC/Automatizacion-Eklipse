import flet as ft
import pandas as pd

class Unificar(ft.Container):
    def __init__(self):
        super().__init__(
            width=750, 
            height=600,
            padding=10,
            bgcolor=ft.colors.RED, 
            #content= self.create_unificar()
        )