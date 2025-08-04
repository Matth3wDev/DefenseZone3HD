import pygame
import os
class Enemigo(pygame.sprite.Sprite):
    def __init__(self, nombre, salud, velocidad, daño, sprite_path, x, y):
        super().__init__()
        self.nombre = nombre
        self.salud = salud
        self.velocidad = velocidad
        self.daño = daño
        self.sprite_path = sprite_path
        self.original_salud = salud
        self.original_image = pygame.image.load(sprite_path).convert_alpha()
        self.image = pygame.trnasform.scale(self.original_image, (15, 15 ))
        self.rect = self.image.get_rect(topleft=(x, y))
        
    def atacar(self):
        return f"{self.nombre} inflingio {self.daño} -PS"

    def recibir_daño(self, cantidad):
        self.salud -= cantidad
        if self.salud <= 0:
            self.morir()
            return f"{self.nombre} pal lobby"
        else:
            return f"{self.nombre} {self.salud}  ya casi se palma"

    def dibujar(self, superficie)
        superficie.blint(self.image, self.rect)
        salud_porcentaje = self.salud / self.original_salud
        pygame.draw.rect(superficie, ROJO, (self.rect.x, self.rect.y - 10, self.rect.width, 5))
        pygame.draw.rect(superficie, VERDE, (self.rect.x, self.rect.y - 10, self.rect.width * salud_porcentaje, 5))

    def __str__ (self):
        return (f"{self.nombre} (Salud: {self.salud}, Daño: {self.daño}), " f"Sprite: {os.path.basename(self.sprite_path)})")

    def morir(self):
        print(f"¡{self.nombre} MANCO!")

class Soldado(Enemigo):
    def __init__(self, nombre, salud, daño, velocidad, sprite.path):
        super().__init__(nombre="Soldado", salud=100, velocidad=2, daño=10, sprite_path)
        
class Tanque(Enemigo):
    def __init__(self, nombre, salud, daño, velocidad, sprite.path):
        super().__init__(nombre="Tanque", salud=300, velocidad=1, daño=30, sprite_path)

class soldado_razo(Enemigo):
    def __init__(self, nombre, salud, daño, velocidad, sprite.path):
        super().__init__(nombre="Soldado Razo", salud=50, velocidad=4, daño=4.5, sprite_path)

def crear_enemigo(tipo_enemigo):
    if tipo_enemigo == "soldado":     
        return Soldado()
    elif tipo_enemigo == "tanque":
        return Tanque()
    elif tipo_enemigo == "Soldado razo":
        return EnemigoRapido()
    else:
        raise ValueError("Tipo de enemigo desconocido")

