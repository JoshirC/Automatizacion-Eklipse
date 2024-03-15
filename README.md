# Automatización Eklipse

### Descripción del Proyecto
Eklipse es una empresa dedicada a los servicios de alimentacion para grandes y pequeñas empresas.
Este proyecto esta enfocado en manejar las plantillas de los productos y/o reposiciones que son solicitadas por los clientes, las cuales estan en el formato de archivo Microsoft Excel. Estos archivos son cargados dentro del software creado y unifica los datos de las plantillas en un nuevo archivo Excel.

### Lenguajes Utilizados
- Python

### Librerias importadas
- openpyxl ( https://openpyxl.readthedocs.io/en/stable/index.html )
- Pandas ( https://pandas.pydata.org/pandas-docs/stable/index.html )

### Entorno de desarrollo
- Flet ( https://flet.dev )

### Manual de uso
[Manual de uso Automatización Eklipse.pdf](https://github.com/JoshirC/Automatizacion-Eklipse/files/14615390/Manual.de.uso.Automatizacion.Eklipse.pdf)

### Generar Aplicación
Una vez que hayas descargado la carpeta y hayas instalado las librerías necesarias, para generar la aplicación debes ejecutar el siguiente comando:
- flet pack app.py --add-data "assets;assets" --icon assets\logoapp.png  --name Automatizacion_EKL
