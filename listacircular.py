from nodo import Nodo
import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
import os
import pygame
import json
import os
from mutagen.mp3 import MP3

def obtener_duracion(cancion):
    """ Obtiene la duración del archivo de audio. """
    if not os.path.exists(cancion):
        print("Archivo no encontrado.")
        return None

    extension = os.path.splitext(cancion)[1].strip().lower()
    if extension == ".wav":
        pygame.mixer.init()
        sonido = pygame.mixer.Sound(cancion)
        return sonido.get_length()
    elif extension == ".mp3":
        audio = MP3(cancion)
        return audio.info.length
    else:
        print(f"Formato '{extension}' no compatible para obtener duración.")
        return None

class ListaCircularDoble:
    def __init__(self, archivo_json="canciones.json"):
        self.lista = None
        self.actual = None
        self.archivo_json = archivo_json
        self.en_pausa = False
        pygame.init()
        pygame.mixer.init()
        self.cargar_desde_json()

    def guardar_en_json(self):
        """ Guarda la lista y el estado actual en JSON. """
        datos = {
            "canciones": [],
            "actual": None
        }

        if self.lista:
            actual = self.lista
            while True:
                datos["canciones"].append({
                    "nombre": actual.nombre_cancion,
                    "artista": actual.artista,
                    "duracion": actual.duracion,
                    "ruta": actual.data,
                    "imagen": actual.imagen_cancion
                })
                actual = actual.siguiente
                if actual == self.lista:
                    break

            datos["actual"] = datos["canciones"].index({
                "nombre": self.actual.nombre_cancion,
                "artista": self.actual.artista,
                "duracion": self.actual.duracion,
                "ruta": self.actual.data,
                "imagen": self.actual.imagen_cancion
            })

        with open(self.archivo_json, "w") as archivo:
            json.dump(datos, archivo, indent=4)

        print("Lista y estado actual guardados en JSON.")

    def cargar_desde_json(self):
        """ Carga la lista y el estado desde JSON. """
        if not os.path.exists(self.archivo_json):
            print("Archivo JSON no encontrado, iniciando lista vacía.")
            return
        
        with open(self.archivo_json, "r") as archivo:
            datos = json.load(archivo)

        for cancion in datos["canciones"]:
            self.agregar(cancion["ruta"], cancion["nombre"], cancion["artista"], cancion["imagen"], guardar=False)

        if datos["actual"] is not None:
            temp = self.lista
            for _ in range(datos["actual"]):
                temp = temp.siguiente
            self.actual = temp

        print("Lista cargada desde JSON y estado restaurado.")

    def agregar(self, ruta_archivo, nombre_cancion, artista, imagen_cancion, guardar=True):
        if not os.path.exists(ruta_archivo):
            messagebox.showwarning("Advertencia", f"Archivo de canción '{ruta_archivo}' no encontrado.")
            return

        duracion = obtener_duracion(ruta_archivo)
        if duracion is None:
            messagebox.showerror("Error", "No se pudo obtener la duración del archivo.")
            return

        nodo = Nodo(nombre_cancion, artista, duracion, ruta_archivo, imagen_cancion)

        if self.lista is None:
            self.lista = nodo
            self.lista.anterior = nodo
            self.lista.siguiente = nodo
            self.actual = nodo
        else:
            ultimo = self.lista.anterior
            ultimo.siguiente = nodo
            nodo.anterior = ultimo
            nodo.siguiente = self.lista
            self.lista.anterior = nodo

        if guardar:
            self.guardar_en_json()

        messagebox.showinfo("Éxito", f"Canción '{nombre_cancion}' de '{artista}' agregada con duración {duracion:.2f} segundos.")

    def eliminar(self, nombre_cancion, artista):
        if self.lista is None:
            messagebox.showinfo("Información", "La lista está vacía.")
            return

        actual = self.lista
        encontrado = False

        while True:
            if actual.nombre_cancion == nombre_cancion and actual.artista == artista:
                encontrado = True
                break
            actual = actual.siguiente
            if actual == self.lista:
                break

        if not encontrado:
            messagebox.showwarning("No encontrado", f"No se encontró '{nombre_cancion}' de '{artista}'.")
            return

        if actual.siguiente == actual:
            self.lista = None
            self.actual = None
        else:
            actual.anterior.siguiente = actual.siguiente
            actual.siguiente.anterior = actual.anterior

            if actual == self.lista:
                self.lista = actual.siguiente
            if actual == self.actual:
                self.actual = actual.siguiente

        self.guardar_en_json()
        messagebox.showinfo("Éxito", f"Canción '{nombre_cancion}' eliminada correctamente.")

    def __getattr__(self, nombre):
        if nombre in ("en_pausa", "reproduciendo", "actual"):
            setattr(self, nombre, False)
            return False
        raise AttributeError(f"'ListaCircularDoble' object has no attribute '{nombre}'")
    
    def reproducir_actual(self):
        if self.actual:
            pygame.mixer.music.load(self.actual.data)
            pygame.mixer.music.play()
            self.en_pausa = False
            self.reproduciendo = True

        
    def pausar(self):
        pygame.mixer.music.pause()
        self.en_pausa = True
       
    def continuar(self):
        pygame.mixer.music.unpause()
        self.en_pausa = False

    def detener(self):
        pygame.mixer.music.stop()
        self.en_pausa = False
        
    def siguiente_cancion(self):
        """ Pasa a la siguiente canción y la reproduce. """
        if self.actual:
            self.actual = self.actual.siguiente
            self.reproducir_actual()
        else:
            messagebox.showwarning("Atención", "Lista vacía.")

    def anterior_cancion(self):
        """ Regresa a la canción anterior y la reproduce. """
        if self.actual:
            self.actual = self.actual.anterior
            self.reproducir_actual()
        else:
            messagebox.showwarning("Atención", "Lista vacía.")

    # Otros métodos de la lista
    def mostrar_canciones(self):
        """ Muestra todas las canciones guardadas. """
        if not self.lista:
            print("Lista vacía.")
            return

        temp = self.actual
        inicio = temp

        canciones = []
        while True:
            canciones.append(f"Cancion '{temp.nombre_cancion}' - '{temp.artista}' - '{temp.duracion:.2f} seg.'")
            temp = temp.siguiente
            if temp == inicio:
                break
        
        return canciones
   

        