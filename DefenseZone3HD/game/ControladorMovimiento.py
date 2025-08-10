import pygame

class ControladorMovimiento:
    def __init__(self, lista_torres):
        self.lista_torres = lista_torres
        self.velocidad = 5  

    def mover_torres(self, teclas):
        for torre in self.lista_torres:
            if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
                torre.x -= self.velocidad
            if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
                torre.x += self.velocidad
            if teclas[pygame.K_UP] or teclas[pygame.K_w]:
                torre.y -= self.velocidad
            if teclas[pygame.K_DOWN] or teclas[pygame.K_s]:
                torre.y += self.velocidad

    def manejar_disparo(self, eventos):
        for event in eventos:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                for torre in self.lista_torres:
                    torre.disparar()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:  
                for torre in self.lista_torres:
                    torre.disparar()