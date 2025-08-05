import pygame

class nivel:
    def __init__(self, numero_nivel, dificultad):
        self.numero_nivel = numero_nivel
        self.dificultad = dificultad
        self.enemigos = []
        self.torres = []

    def agregar_enemigo(self, enemigo):
        self.enemigos.append(enemigo)

    def agregar_torre(self, torre):
        self.torres.append(torre)

    def obtener_cantidad_enemigos(self):
        return len(self.enemigos)

    def obtener_cantidad_torres(self):
        return len(self.torres)

class GestorNiveles:
    def __init__(self):
        self.niveles = []

    def crear_nivel(self, numero_nivel, dificultad):
        nivel = nivel(numero_nivel, dificultad)
        self.niveles.append(nivel)
        return nivel

    def obtener_nivel(self, numero_nivel):
        for nivel in self.niveles:
            if nivel.numero_nivel == numero_nivel:
                return nivel
        return None

    def obtener_todos_niveles(self):
        return self.niveles

def inicializar_niveles():
    gestor_niveles = GestorNiveles()
    gestor_niveles.crear_nivel(1, 'fácil')
    gestor_niveles.crear_nivel(2, 'medio')
    gestor_niveles.crear_nivel(3, 'difícil')
    return