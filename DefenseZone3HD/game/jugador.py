import pygame

class jugador:
    def __init__(self, x, y, ancho_panel, ancho_pantalla, alto_pantalla):
        self.rect = pygame.Rect(x, y, 40, 40)
        self.color = (200, 100, 100)
        self.velocidad = 5
        self.limite_x = ancho_pantalla - ancho_panel
        self.limite_y = alto_pantalla

    def mover(self, teclas):
        if teclas[pygame.K_w] and self.rect.top > 0:
            self.rect.y -= self.velocidad
        if teclas[pygame.K_s] and self.rect.bottom < self.limite_y:
            self.rect.y += self.velocidad
        if teclas[pygame.K_a] and self.rect.left > 0:
            self.rect.x -= self.velocidad
        if teclas[pygame.K_d] and self.rect.right < self.limite_x:
            self.rect.x += self.velocidad

    def dibujar(self, pantalla):
        pygame.draw.rect(pantalla, self.color, self.rect)