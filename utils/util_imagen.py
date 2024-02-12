from PIL import Image, ImageTk

def cargar_imagen(ruta, tamano):
    return ImageTk.PhotoImage(Image.open(ruta).resize(tamano, Image.ADAPTIVE))