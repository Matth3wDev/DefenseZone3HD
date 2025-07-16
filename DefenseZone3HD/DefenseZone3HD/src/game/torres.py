import pygame

class Torre:
    def __init__(self, nombre, daño, alcance, velocidad_disparo):
        self.nombre = nombre
        self.daño = daño
        self.alcance = alcance
        self.velocidad_disparo = velocidad_disparo

    def atacar(self, enemigo):
        if self.esta_en_alcance(enemigo):
            enemigo.recibir_daño(self.daño)

    def esta_en_alcance(self, enemigo):
        # Lógica de cálculo de alcance (placeholder)
        return True

class TorreFrancotirador(Torre):
    def __init__(self):
        super().__init__(nombre="Torre Francotirador", daño=50, alcance=300, velocidad_disparo=1.5)

class TorreAmetralladora(Torre):
    def __init__(self):
        super().__init__(nombre="Torre Ametralladora", daño=10, alcance=150, velocidad_disparo=0.5)

class TorreLlamas(Torre):
    def __init__(self):
        super().__init__(nombre="Torre de Llamas", daño=20, alcance=100, velocidad_disparo=0.8)

def crear_torre(tipo_torre):
    if tipo_torre == "francotirador":
        return TorreFrancotirador()
    elif tipo_torre == "ametralladora":
        return TorreAmetralladora()
    elif tipo_torre == "llamas":
        return TorreLlamas()
    else:
        raise ValueError("Tipo de torre desconocido")