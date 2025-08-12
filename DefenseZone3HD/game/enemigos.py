import pygame
import random
import math
import os

ROJO = (200, 0, 0)
VERDE = (0, 200, 0)

class enemigos(pygame.sprite.Sprite):
    def __init__(self, nombre, salud, velocidad, daño, sprite_path, x, y):
        super().__init__()
        self.nombre = nombre
        self.salud = salud
        self.velocidad = velocidad
        self.daño = daño
        self.sprite_path = sprite_path
        self.original_salud = salud
        self.estado = "avanzando"  
        self.objetivo = None
        self.tiempo_ultimo_ataque = 0
        self.cooldown_ataque = 1000  

        self.original_image = pygame.image.load(sprite_path).convert_alpha()
        self.image = pygame.transform.scale(self.original_image, (40, 40))
        self.rect = self.image.get_rect(topleft=(x, y))

    def update(self):
        if self.estado == "avanzando":
            self.rect.x -= self.velocidad
        elif self.estado == "esquivando":
            #
            self.rect.y += random.choice([-2, 2])
            self.rect.x -= self.velocidad * 0.5

    def atacar(self, torre=None):
        tiempo_actual = pygame.time.get_ticks()
        if tiempo_actual - self.tiempo_ultimo_ataque > self.cooldown_ataque:
            if torre:
                self.tiempo_ultimo_ataque = tiempo_actual
                resultado = torre.recibir_daño(self.daño)
                return f"{self.nombre} atacó a la torre e infligió {self.daño} de daño. {resultado}"
        return None

    def recibir_daño(self, cantidad):
        self.salud -= cantidad
        
        if random.random() < (self.velocidad / 20):
            self.estado = "esquivando"
        
        if self.salud <= 0:
            self.morir()
            return f"{self.nombre} pal lobby"
        else:
            return f"{self.nombre} {self.salud} ya casi se palma"

    def dibujar(self, superficie):
        superficie.blit(self.image, self.rect)
        salud_porcentaje = max(0, self.salud / self.original_salud)
        pygame.draw.rect(superficie, ROJO, (self.rect.x, self.rect.y - 10, self.rect.width, 5))
        pygame.draw.rect(superficie, VERDE, (self.rect.x, self.rect.y - 10, self.rect.width * salud_porcentaje, 5))

    def morir(self):
        print(f"¡{self.nombre} ha sido derrotado!")
        print(f"¡{self.nombre} MANCO!")

    def __str__(self):
        return f"{self.nombre} (Salud: {self.salud}, Daño: {self.daño}), Sprite: {os.path.basename(self.sprite_path)})"


