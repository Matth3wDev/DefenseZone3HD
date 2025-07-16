import pygame

class Enemigo:
    def __init__(self, nombre, salud, velocidad, daño):
        self.nombre = nombre
        self.salud = salud
        self.velocidad = velocidad
        self.daño = daño

    def recibir_daño(self, cantidad):
        self.salud -= cantidad
        if self.salud <= 0:
            self.morir()

    def morir(self):
        print(f"¡{self.nombre} ha sido derrotado!")

class Soldado(Enemigo):
    def __init__(self):
        super().__init__(nombre="Soldado", salud=100, velocidad=2, daño=10)

class Tanque(Enemigo):
    def __init__(self):
        super().__init__(nombre="Tanque", salud=300, velocidad=1, daño=30)

class EnemigoRapido(Enemigo):
    def __init__(self):
        super().__init__(nombre="Enemigo Rápido", salud=50, velocidad=4, daño=5)

def crear_enemigo(tipo_enemigo):
    if tipo_enemigo == "soldado":
        return Soldado()
    elif tipo_enemigo == "tanque":
        return Tanque()
    elif tipo_enemigo == "rapido":
        return EnemigoRapido()
    else:
        raise ValueError("Tipo de enemigo desconocido")