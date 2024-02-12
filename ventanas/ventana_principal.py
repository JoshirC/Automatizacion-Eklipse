import tkinter as tk
import customtkinter as ctk

import utils.util_imagen as u_i

class VentanaPrincipal(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.logo = u_i.cargar_imagen('./imagenes/Logo-Eklipse-02-1.png', (200, 200))
        self.title('CONSOLIDADO EKLIPSE')
        self.iconbitmap('./imagenes/Logo-Eklipse-02-1.png')
        self.geometry('1200x700')
        self.config(bg='white')