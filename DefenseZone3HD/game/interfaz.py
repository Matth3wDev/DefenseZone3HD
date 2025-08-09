import pygame

class interfaz:
    def __init__(self, pantalla, ancho_panel=250):
        self.pantalla = pantalla
        self.ancho_panel = ancho_panel
        self.font = pygame.font.SysFont("consolas", 24)
        self.botones = {}
        self.seleccion_actual = None
        self.crear_botones()

    def crear_botones(self):
        nombres = ["Nivel 1", "Nivel 2", "Nivel 3", "Salir"]
        for i, nombre in enumerate(nombres):
            x = self.pantalla.get_width() - self.ancho_panel + 20
            y = 150 + i * 70
            rect = pygame.Rect(x, y, 200, 50)
            self.botones[nombre] = rect

    def dibujar_panel(self, vidas, puntuacion, nivel):
        panel_rect = pygame.Rect(
            self.pantalla.get_width() - self.ancho_panel,
            0,
            self.ancho_panel,
            self.pantalla.get_height()
        )
        pygame.draw.rect(self.pantalla, (40, 40, 60), panel_rect)

        self.pantalla.blit(self.font.render(f"Vidas: {vidas}", True, (200, 200, 200)), (panel_rect.x + 20, 20))
        self.pantalla.blit(self.font.render(f"Puntos: {puntuacion}", True, (200, 200, 200)), (panel_rect.x + 20, 60))
        self.pantalla.blit(self.font.render(f"Nivel: {nivel}", True, (200, 200, 200)), (panel_rect.x + 20, 100))

        for nombre, rect in self.botones.items():
            color = (80, 120, 180) if nombre == self.seleccion_actual else (60, 60, 90)
            pygame.draw.rect(self.pantalla, color, rect)
            pygame.draw.rect(self.pantalla, (200, 200, 200), rect, 2)
            texto = self.font.render(nombre, True, (255, 255, 255))
            self.pantalla.blit(texto, (rect.x + 10, rect.y + 10))

    def manejar_evento(self, evento):
        if evento.type == pygame.MOUSEBUTTONDOWN:
            pos = evento.pos
            for nombre, rect in self.botones.items():
                if rect.collidepoint(pos):
                    self.seleccion_actual = nombre
                    print(f"[Interfaz] Botón seleccionado: {nombre}")
                    return nombre
        return None