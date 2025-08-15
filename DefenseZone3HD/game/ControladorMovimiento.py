import pygame

class ControladorMovimiento:
    def __init__(self, lista_torres=None):  # Hacer parámetro opcional
        self.lista_torres = lista_torres if lista_torres else []
        self.velocidad = 5
        self.teclas_activas = {
            'izquierda': [pygame.K_LEFT, pygame.K_a],
            'derecha': [pygame.K_RIGHT, pygame.K_d],
            'arriba': [pygame.K_UP, pygame.K_w],
            'abajo': [pygame.K_DOWN, pygame.K_s]
        }

    def mover_torres(self, teclas):
        """Mueve todas las torres según las teclas presionadas"""
        for torre in self.lista_torres:
            if any(teclas[k] for k in self.teclas_activas['izquierda']):
                torre.x -= self.velocidad
            if any(teclas[k] for k in self.teclas_activas['derecha']):
                torre.x += self.velocidad
            if any(teclas[k] for k in self.teclas_activas['arriba']):
                torre.y -= self.velocidad
            if any(teclas[k] for k in self.teclas_activas['abajo']):
                torre.y += self.velocidad

    def manejar_disparo(self, eventos):
        """Gestiona los eventos de disparo"""
        for event in eventos:
            if (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE) or \
               (event.type == pygame.MOUSEBUTTONDOWN and event.button == 3):
                for torre in self.lista_torres:
                    torre.disparar()