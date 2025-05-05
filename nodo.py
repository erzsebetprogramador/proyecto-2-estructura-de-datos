class Nodo:
    def __init__(self, nombre_cancion, artista, duracion, data, imagen_cancion):
        self.nombre_cancion = nombre_cancion
        self.artista = artista
        self.duracion = duracion
        self.data = data
        self.imagen_cancion = imagen_cancion
        self.siguiente = None
        self.anterior = None