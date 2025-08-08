import os
import pygame

class gestor_recursos:
    def __init__(self):
        self.carpeta_base = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'assets/imagen')
        print(f"[GestorRecursos] Carpeta base: {self.carpeta_base}")

    def cargar_imagen(self, nombre_archivo):
        print(f"[GestorRecursos] Cargando imagen: '{nombre_archivo}'")
        if not nombre_archivo or not isinstance(nombre_archivo, str):
            raise ValueError("[GestorRecursos] Nombre de imagen vacío o inválido.")
        ruta = os.path.join(self.carpeta_base, nombre_archivo) 
        if not os.path.exists(ruta):
            raise FileNotFoundError(f"[GestorRecursos] Imagen no encontrada: {ruta}")
        return pygame.image.load(ruta).convert_alpha()

    def cargar_sonido(self, nombre_archivo):
        print(f"[GestorRecursos] Cargando sonido: '{nombre_archivo}'")
        if not nombre_archivo or not isinstance(nombre_archivo, str):
            raise ValueError("[GestorRecursos] Nombre de sonido vacío o inválido.")
        ruta = os.path.join(self.carpeta_base, 'sonidos', nombre_archivo)
        if not os.path.exists(ruta):
            raise FileNotFoundError(f"[GestorRecursos] Sonido no encontrado: {ruta}")
        return pygame.mixer.Sound(ruta)

    def cargar_fuente(self, nombre_archivo, tamaño):
        print(f"[GestorRecursos] Cargando fuente: '{nombre_archivo}' tamaño {tamaño}")
        if not nombre_archivo or not isinstance(nombre_archivo, str):
            raise ValueError("[GestorRecursos] Nombre de fuente vacío o inválido.")
        ruta = os.path.join(self.carpeta_base, 'fuentes', nombre_archivo)
        if not os.path.exists(ruta):
            raise FileNotFoundError(f"[GestorRecursos] Fuente no encontrada: {ruta}")
        return pygame.font.Font(ruta, tamaño)