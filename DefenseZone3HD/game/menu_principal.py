import pygame
from gestor_recursos import gestor_recursos

class MenuPrincipal(gestor_recursos): 
 def __init__(self, pantalla):
        super().__init__()
        self.pantalla = pantalla
        self.font = pygame.font.SysFont("consolas", 36)
        self.botones = {}
        self.seleccion = None
        self.fondo = self.cargar_imagen("fondo.jpg") 
        self.crear_botones()

def crear_botones(self):
        nombres = ["Jugar", "Salir"]
        ancho = 300
        alto = 60
        x = (self.pantalla.get_width() - ancho) // 2 
        for i, nombre in enumerate(nombres):
            y = 250 + i * 100
            rect = pygame.Rect(x, y, ancho, alto)
            self.botones[nombre] = rect

def dibujar(self):
        self.pantalla.fill((20, 20, 40))
        titulo = self.font.render("Menú Principal", True, (255, 255, 255))
        self.pantalla.blit(titulo, ((self.pantalla.get_width() - titulo.get_width()) // 2, 100))

        for nombre, rect in self.botones.items():
            pygame.draw.rect(self.pantalla, (70, 100, 160), rect)
            pygame.draw.rect(self.pantalla, (255, 255, 255), rect, 2)
            texto = self.font.render(nombre, True, (255, 255, 255))
            self.pantalla.blit(texto, (rect.x + 20, rect.y + 10))

def manejar_evento(self, evento):
        if evento.type == pygame.MOUSEBUTTONDOWN:
            pos = evento.pos
            for nombre, rect in self.botones.items():
                if rect.collidepoint(pos):
                    self.seleccion = nombre
                    print(f"[MenuPrincipal] Selección: {nombre}")
                    return nombre
        return None