import pygame
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

        self.original_image = pygame.image.load(sprite_path).convert_alpha()
        self.image = pygame.transform.scale(self.original_image, (40, 40))
        self.rect = self.image.get_rect(topleft=(x, y))

    def update(self):
        self.rect.x -= self.velocidad  

    def atacar(self):
        return f"{self.nombre} infligió {self.daño} -PS"

    def recibir_daño(self, cantidad):
        self.salud -= cantidad
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

# Subclases
class Soldado(enemigos):
    def __init__(self, sprite_path, x, y):
        super().__init__("Soldado", 100, 2, 10, sprite_path, x, y)

class Tanque(enemigos):
    def __init__(self, sprite_path, x, y):
        super().__init__("Tanque", 300, 1, 30, sprite_path, x, y)

class EnemigoRapido(enemigos):
    def __init__(self, sprite_path, x, y):
        super().__init__("Enemigo Rápido", 50, 4, 5, sprite_path, x, y)

class SoldadoRazo(enemigos):
    def __init__(self, sprite_path, x, y):
        super().__init__("Soldado Razo", 50, 4.5, 4.5, sprite_path, x, y)


enemigos = [
    Soldado("", 1024, 550),
    Tanque("recursos/img/Tanque.png", 1224, 550), 
    EnemigoRapido("", 1424, 550)
]