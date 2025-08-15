import pygame
import math

class torre:
    
    def __init__(self, x, y, nombre, costo, rango, cadencia_fuego, daño, imagen_torre):
        self.x = x
        self.y = y
        self.nombre = nombre
        self.costo = costo
        self.rango = rango
        self.cadencia_fuego = cadencia_fuego
        self.daño = daño
        self.imagen = pygame.image.load(imagen_torre).convert_alpha()
        self.rect = self.imagen.get_rect(center=(x, y))
        self.ultimo_disparo = pygame.time.get_ticks()
        self.enemigo_actual = None
    
    def dibujar(self, pantalla):
        
        pantalla.blit(self.imagen, self.rect)
        
        pygame.draw.circle(pantalla, (255, 255, 255, 50), self.rect.center, self.rango, 1)

    def buscar_objetivo(self, enemigos):
        
        enemigo_mas_cercano = None
        distancia_minima = float('inf')

        for enemigo in enemigos:
            
            distancia = math.hypot(self.x - enemigo.x, self.y - enemigo.y)
            
            if distancia <= self.rango:
                if distancia < distancia_minima:
                    distancia_minima = distancia
                    enemigo_mas_cercano = enemigo
        self.enemigo_actual = enemigo_mas_cercano

    def disparar(self):
        
        tiempo_actual = pygame.time.get_ticks()
        if self.enemigo_actual and tiempo_actual - self.ultimo_disparo >= self.cadencia_fuego:
            self.ultimo_disparo = tiempo_actual
            return True 
        return False
    