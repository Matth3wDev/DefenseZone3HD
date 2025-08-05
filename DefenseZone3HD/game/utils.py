import pygame

def cargar_imagen(ruta_archivo):
    # Función para cargar una imagen desde la ruta especificada
    pass

def cargar_sonido(ruta_archivo):
    # Función para cargar un sonido desde la ruta especificada
    pass

def limitar(valor, valor_minimo, valor_maximo):
    # Función para limitar un valor entre un mínimo y un máximo
    return max(min(valor, valor_maximo), valor_minimo)

def calcular_distancia(punto1, punto2):
    # Función para calcular la distancia entre dos puntos
    return ((punto1[0] - punto2[0]) ** 2 + (punto1[1] - punto2[1]) ** 2) ** 0.5

def formatear_tiempo(segundos):
    # Función para formatear el tiempo en segundos a una cadena (MM:SS)
    minutos = segundos // 60
    segundos = segundos % 60
    return