import flet as ft
from consolidado import Consolidado
from mensual import Mensual
from reposiciones import Reposiciones
from compra_local import CompraLocal
from bodega import Bodega
from unificar import Unificar

class Menu(ft.Container):
    """
    Clase que representa el menú principal de la aplicación.

    Attributes:
        main_content (ft.Container): Contenedor principal que muestra el contenido principal de la aplicación.
    Methods:
        __init__: Constructor de la clase.
        create_row: Método para crear la interfaz de usuario del menú principal.
        show_consolidado: Método para mostrar la vista de Consolidado.
        show_mensual: Método para mostrar la vista Mensual.
        show_reposiciones: Método para mostrar la vista de Reposiciones.
        show_compra_local: Método para mostrar la vista de Compra Local.
        show_bodega: Método para mostrar la vista de Bodega.
        show_unificar: Método para mostrar la vista de Unificar.
    """
    def __init__(self):
        """
        Inicializa una instancia de la clase Menu.

        Returns:
            None
        """
        self.main_content = ft.Container(
            width=750, 
            height=600,
            padding=10,
           #bgcolor=ft.colors.BLUE
            content=ft.Column([
                ft.Container(
                    content=ft.Image(src=f"/fondo.jpg", width=700, height=400)
                ),
                ft.Text("Bienvenido a EKLIPSE", size=60, weight=ft.FontWeight.W_900, selectable=True), #Titulo
                ft.Row([
                    ft.Icon(ft.icons.COPYRIGHT_SHARP, size=15, color=ft.colors.BLACK),
                    ft.Text("2024 - Desarrollado por Joshir", size=12, color=ft.colors.BLACK),
                    ft.Icon(ft.icons.EMAIL_OUTLINED, size=15, color=ft.colors.BLACK),
                    ft.Text("joshir.contreras@gmail.com", size=12, color=ft.colors.BLACK),
                ]),
            ])

        )  # Inicialmente mostrara la informacion de la APP
        super().__init__(
            width=1000,
            height=600,
            content=self.create_row(self.main_content)
        )
    def create_row(self, main_content):
         """
        Crea la interfaz de usuario del menú principal.

        Args:
            main_content (ft.Container): Contenedor principal que muestra el contenido principal de la aplicación.

        Returns:
            ft.Row: Fila que contiene el menú y el contenido principal.
        """
         return ft.Row([
            ft.Container(
                    width=250,
                    height=600,
                    bgcolor='#FF8412',
                    padding=20,
                    #alignment=ft.alignment.center,
                    content=ft.Column([
                        ft.Image(src=f"/logo_eklipse.png", width=220, height=150),
                        ft.ElevatedButton(
                            content= ft.Container(
                                width=250,
                                height=45,
                                alignment=ft.alignment.center,
                                content=ft.Text("RECTIFICACIÓN", color=ft.colors.BLACK, size=15),
                            ),
                            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
                            on_click=self.show_consolidado
                        ),
                        ft.ElevatedButton(
                            content= ft.Container(
                                width=200,
                                height=45,
                                alignment=ft.alignment.center,
                                content=ft.Text("MENSUAL", color=ft.colors.BLACK, size=15),
                            ),
                            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
                            on_click=self.show_mensual
                        ),
                        ft.ElevatedButton(
                            content= ft.Container(
                                width=200,
                                height=45,
                                alignment=ft.alignment.center,
                                content=ft.Text("COMPRA LOCAL", color=ft.colors.BLACK, size=15),
                            ),
                            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
                            on_click=self.show_compra_local
                        ),
                        ft.ElevatedButton(
                            content= ft.Container(
                                width=200,
                                height=45,
                                alignment=ft.alignment.center,
                                content=ft.Text("BODEGA", color=ft.colors.BLACK, size=15),
                            ),
                            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
                            on_click=self.show_bodega
                        ),
                        ft.ElevatedButton(
                            content= ft.Container(
                                width=200,
                                height=45,
                                alignment=ft.alignment.center,
                                content=ft.Text("REPOSICIONES", color=ft.colors.BLACK, size=15),
                            ),
                            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
                            on_click=self.show_reposiciones
                        ),
                        ft.ElevatedButton(
                            content= ft.Container(
                                width=200,
                                height=45,
                                alignment=ft.alignment.center,
                                content=ft.Text("UNIFICAR", color=ft.colors.WHITE, size=15),
                            ),
                            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
                            bgcolor='#FB4308',
                            on_click=self.show_unificar
                        ),
                    ], alignment=ft.MainAxisAlignment.START),
                ),
                main_content # Inicialmente mostrar la vista de Consolidado
            ])

    def show_consolidado(self, button):
        """
        Muestra la vista de Consolidado al hacer clic en el botón correspondiente.

        Args:
            button: Botón que activa la vista de Consolidado.

        Returns:
            None
        """
        self.main_content = Consolidado()
        self.content = self.create_row(self.main_content)
        self.update()

    def show_mensual(self, button):
        """
        Muestra la vista Mensual al hacer clic en el botón correspondiente.

        Args:
            button: Botón que activa la vista Mensual.

        Returns:
            None
        """
        self.main_content = Mensual()
        self.content = self.create_row(self.main_content)
        self.update()

    def show_reposiciones(self, button):
        """
        Muestra la vista de Reposiciones al hacer clic en el botón correspondiente.

        Args:
            button: Botón que activa la vista de Reposiciones.

        Returns:
            None
        """
        self.main_content = Reposiciones()
        self.content = self.create_row(self.main_content)
        self.update()
    def show_compra_local(self, button):
        """
        Muestra la vista de Compra Local al hacer clic en el botón correspondiente.

        Args:
            button: Botón que activa la vista de Compra Local.

        Returns:
            None
        """
        self.main_content = CompraLocal()
        self.content = self.create_row(self.main_content)
        self.update()
    def show_bodega(self, button):
        """
        Muestra la vista de Bodega al hacer clic en el botón correspondiente.

        Args:
            button: Botón que activa la vista de Bodega.

        Returns:
            None
        """
        self.main_content = Bodega()
        self.content = self.create_row(self.main_content)
        self.update()
    def show_unificar(self,buton):
        """
        Muestra la vista de Unificar al hacer clic en el botón correspondiente.

        Args:
            buton: Botón que activa la vista de Unificar.

        Returns:
            None
        """
        self.main_content = Unificar()
        self.content = self.create_row(self.main_content)
        self.update()