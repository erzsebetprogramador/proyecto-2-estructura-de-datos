import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
import os
from PIL import Image, ImageTk
from listacircular import ListaCircularDoble

class ReproductorGUI:
    def __init__(self, root, reproductor):
        self.reproductor = reproductor
        self.root = root
        self.root.title("Gestión de Canciones")
        self.root.configure(bg="#36454F")

        # Entrada de canción
        self.entry_cancion = tk.Entry(root, width=50)
        self.entry_cancion.grid(row=0, column=0, columnspan=2, padx=5, pady=5)

        # Frame para botones de Seleccionar, Agregar y Eliminar
        frame_botones_superiores = tk.Frame(root, bg="#FF6F61")
        frame_botones_superiores.grid(row=1, column=0, columnspan=2, pady=5)

        btn_seleccionar = tk.Button(frame_botones_superiores, text="Seleccionar Canción", command=self.seleccionar_documento, bg="#FF6F61", fg="white", activebackground="#FF6F61", activeforeground="white")
        btn_seleccionar.pack(side="left", padx=5)

        btn_agregar = tk.Button(frame_botones_superiores, text="Agregar Canción", command=self.agregar_desde_gui, bg="#FF6F61", fg="white", activebackground="#FF6F61", activeforeground="white")
        btn_agregar.pack(side="left", padx=5)

        btn_eliminar = tk.Button(frame_botones_superiores, text="Eliminar Canción", command=self.eliminar_desde_gui, bg="#FF6F61", fg="white", activebackground="#FF6F61", activeforeground="white")
        btn_eliminar.pack(side="left", padx=5)

        frame_botones = tk.Frame(root, bg="#FF6F61")
        frame_botones.grid(row=2, column=0, columnspan=4, pady=10)

        self.btn_anterior = tk.Button(frame_botones, text="⏮️", command=self.anterior_cancion, bg="#FF6F61", fg="white", activebackground="#FF6F61", activeforeground="white")
        self.btn_anterior.pack(side="left", padx=5)

        self.btn_play_pause = tk.Button(frame_botones, text="▶️", command=self.toggle_play_pause, bg="#FF6F61", fg="white", activebackground="#FF6F61", activeforeground="white")
        self.btn_play_pause.pack(side="left", padx=5)

        btn_stop = tk.Button(frame_botones, text="⏹️", command=self.detener, bg="#FF6F61", fg="white", activebackground="#FF6F61", activeforeground="white")
        btn_stop.pack(side="left", padx=5)

        self.btn_siguiente = tk.Button(frame_botones, text="⏭️", command=self.siguiente_cancion, bg="#FF6F61", fg="white", activebackground="#FF6F61", activeforeground="white")
        self.btn_siguiente.pack(side="left", padx=5)

        self.btn_mostrar = tk.Button(root, text="📄 Mostrar Canciones", command=self.mostrar_canciones, bg="#FF6F61", fg="white", activebackground="#FF6F61", activeforeground="white")
        self.btn_mostrar.grid(row=3, column=0, columnspan=4, pady=10)

       # Frame para contener listbox e imagen
        frame_contenido = tk.Frame(root)
        frame_contenido.grid(row=6, column=0, columnspan=4, padx=0, pady=0)

        # Etiqueta de títulos dentro de frame_contenido, encima del listbox
        self.label_titulos = tk.Label(frame_contenido, text="Nombre\t\tArtista\t\tDuración", font=("Arial", 12, "bold"), bg="#FF6F61", fg="white", activebackground="#FF6F61", activeforeground="white")
        self.label_titulos.pack(pady=0)

        # Listbox de canciones dentro del frame_contenido
        self.listbox_canciones = tk.Listbox(frame_contenido, width=40, height=10, bg="#36454F", fg="white", selectbackground="#FF6F61", selectforeground="black")
        self.listbox_canciones.pack(padx=5, pady=5)

        # Frame para la imagen dentro del frame_contenido (al lado del listbox)
        frame_imagen = tk.Frame(frame_contenido)
        frame_imagen.pack(side="top", pady=5)

        # Label para mostrar la imagen, centrado dentro del frame_imagen
        self.label_imagen = tk.Label(frame_imagen,  bg="#FF6F61", fg="white", activebackground="#FF6F61", activeforeground="white")
        self.label_imagen.pack(anchor="center")


        # Asociamos evento de selección
        self.listbox_canciones.bind('<<ListboxSelect>>', self.reproducir_cancion_seleccionada)
        self.verificar_reproduccion()
        
        self.label_estado = tk.Label(root, text="Estado: Esperando", font=("Arial", 12), bg="#FF6F61", fg="white", activebackground="#FF6F61", activeforeground="white")
        self.label_estado.grid(row=7, column=0, columnspan=4, pady=10)


    def seleccionar_documento(self):
        archivo = filedialog.askopenfilename(title="Seleccionar archivo de canción", filetypes=[("Archivos de audio", "*.mp3 *.wav")])
        self.entry_cancion.delete(0, tk.END)
        self.entry_cancion.insert(0, archivo)

    def agregar_desde_gui(self):
        ruta_archivo = self.entry_cancion.get()

        if not ruta_archivo or not os.path.exists(ruta_archivo):
            messagebox.showerror("Error", f"Archivo '{ruta_archivo}' no encontrado.")
            return

        nombre_cancion = simpledialog.askstring("Entrada", "Ingrese el nombre de la canción:")
        artista = simpledialog.askstring("Entrada", "Ingrese el nombre del artista:")
        imagen_cancion = filedialog.askopenfilename(title="Seleccionar imagen de la canción", filetypes=[("Imágenes", "*.png *.jpg *.jpeg")])

        if not nombre_cancion or not artista:
            messagebox.showwarning("Advertencia", "Debe ingresar el nombre de la canción y el artista.")
            return

        self.reproductor.agregar(ruta_archivo, nombre_cancion, artista, imagen_cancion)

        # Limpiar el Entry después de agregar la canción
        self.entry_cancion.delete(0, tk.END)

        # Ocultar el Entry
        self.entry_cancion.grid_forget()


    def eliminar_desde_gui(self):
        nombre_cancion = simpledialog.askstring("Eliminar", "Ingrese el nombre de la canción a eliminar:")
        artista = simpledialog.askstring("Eliminar", "Ingrese el artista de la canción:")

        if not nombre_cancion or not artista:
            messagebox.showwarning("Advertencia", "Debe ingresar el nombre y el artista.")
            return

        self.reproductor.eliminar(nombre_cancion, artista)

    def toggle_play_pause(self):
        if not self.reproductor.actual:
            self.label_estado.config(text="Estado: No hay canción seleccionada")
            return
        if self.reproductor.en_pausa:
            self.reproductor.continuar()
            self.btn_play_pause.config(text="⏸️")
            self.label_estado.config(text=f"Estado: Reproduciendo {self.reproductor.actual.nombre_cancion}")
            self.mostrar_imagen_actual()
        elif pygame.mixer.music.get_busy():
            self.reproductor.pausar()
            self.btn_play_pause.config(text="▶️")
            self.label_estado.config(text=f"Estado: Pausado {self.reproductor.actual.nombre_cancion}")
            self.mostrar_imagen_actual()
        else:
            self.reproductor.reproducir_actual()
            self.btn_play_pause.config(text="⏸️")
            self.label_estado.config(text=f"Estado: Reproduciendo {self.reproductor.actual.nombre_cancion}")
            self.mostrar_imagen_actual()

    def detener(self):
        self.reproductor.detener()
        self.reproductor.en_pausa = False
        self.reproductor.reproduciendo = False
        self.btn_play_pause.config(text="▶️")
        self.label_estado.config(text=f"Estado: Detenido {self.reproductor.actual.nombre_cancion}")


    def siguiente_cancion(self):
        if not self.reproductor.actual:
            messagebox.showinfo("Info", "No hay canciones en la lista.")
            return

        self.reproductor.siguiente_cancion()
        self.btn_play_pause.config(text="⏸️")  # Porque al cambiar de canción, empieza a reproducirse
        self.label_estado.config(text=f"Estado: Reproduciendo {self.reproductor.actual.nombre_cancion}")
        self.mostrar_imagen_actual()
    def anterior_cancion(self):
        if not self.reproductor.actual:
            messagebox.showinfo("Info", "No hay canciones en la lista.")
            return

        self.reproductor.anterior_cancion()
        self.btn_play_pause.config(text="⏸️")  # Igual, reproduce la canción anterior
        self.label_estado.config(text=f"Estado: Reproduciendo {self.reproductor.actual.nombre_cancion}")
        self.mostrar_imagen_actual()
    def mostrar_canciones(self):
        self.listbox_canciones.delete(0, tk.END)  # Borra lo anterior

        canciones = self.reproductor.mostrar_canciones()

        if canciones:
            for cancion in canciones:
                self.listbox_canciones.insert(tk.END, cancion)
        else:
            self.listbox_canciones.insert(tk.END, "No hay canciones para mostrar.")

        # Programamos que se vuelva a llamar a sí mismo en 2 segundos (2000 ms)
        self.root.after(2000, self.mostrar_canciones)


    def reproducir_cancion_seleccionada(self, event):
        seleccion = self.listbox_canciones.curselection()
        if seleccion:
            indice = seleccion[0]
            temp = self.reproductor.actual
            for _ in range(indice):
                temp = temp.siguiente
            self.reproductor.actual = temp
            self.reproductor.reproducir_actual()
            self.btn_play_pause.config(text="⏸️")
            self.label_estado.config(text=f"Estado: Reproduciendo {self.reproductor.actual.nombre_cancion}")
            self.mostrar_imagen_actual()

    def verificar_reproduccion(self):
        """Verifica si la canción actual terminó, y si es así pasa a la siguiente."""
        if self.reproductor.actual and self.reproductor.reproduciendo and not pygame.mixer.music.get_busy() and not self.reproductor.en_pausa:
            # Si ya terminó la canción y no estaba pausada
            self.reproductor.actual = self.reproductor.actual.siguiente
            self.reproductor.reproducir_actual()
            self.btn_play_pause.config(text="⏸️")
            self.label_estado.config(text=f"Estado: Reproduciendo {self.reproductor.actual.nombre_cancion}")
            self.mostrar_imagen_actual()
        self.root.after(1000, self.verificar_reproduccion)
    
    
    def mostrar_imagen_actual(self):
        if self.reproductor.actual and self.reproductor.actual.imagen_cancion:
            try:
                # Cargamos con PIL directamente la ruta guardada
                imagen = Image.open(self.reproductor.actual.imagen_cancion)
                imagen = imagen.resize((150, 150))  # Redimensiona la imagen si quieres
                self.imagen_tk = ImageTk.PhotoImage(imagen)
                self.label_imagen.config(image=self.imagen_tk)
            except Exception as e:
                print(f"Error al cargar imagen: {e}")
                self.label_imagen.config(image="")
        else:
            self.label_imagen.config(image="")
    
    def siguiente_cancion(self):
        if not self.reproductor.actual:
            messagebox.showinfo("Info", "No hay canciones en la lista.")
            return

        self.reproductor.siguiente_cancion()
        self.reproductor.reproducir_actual()
        self.btn_play_pause.config(text="⏸️")
        self.label_estado.config(text=f"Estado: Reproduciendo {self.reproductor.actual.nombre_cancion}")
        self.mostrar_imagen_actual()  # <<<<<< NUEVO



if __name__ == "__main__":
    import pygame  # Asegúrate de tener pygame instalado
    root = tk.Tk()
    reproductor = ListaCircularDoble()
    app = ReproductorGUI(root, reproductor)
    root.mainloop()

