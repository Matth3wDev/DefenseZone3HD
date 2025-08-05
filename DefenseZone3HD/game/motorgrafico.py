import pygame

class motorgrafico:
    def __init__(self, pantalla):
        self.pantalla = pantalla
        self.capas = {
            "fondo": [],
            "torres": [],
            "disparos": [],
            "ui": []
        }
        self.cursor_img = None
        self.cursor_visible = True

    def cargar_cursor(self, ruta):
        try:
            self.cursor_img = pygame.image.load(ruta).convert_alpha()
            pygame.mouse.set_visible(False)
        except Exception as e:
            print(f"Error al cargar cursor: {e}")

    def limpiar(self):
        for clave in self.capas:
            self.capas[clave] = []

    def agregar(self, objeto, capa):
        if capa in self.capas:
            self.capas[capa].append(objeto)

    def renderizar(self, vidas, puntuacion, nivel):
        self.pantalla.fill((10, 10, 20))
        for capa in ["fondo", "torres", "disparos", "ui"]:
            for obj in self.capas[capa]:
                obj.dibujar(self.pantalla)

        if self.cursor_img and self.cursor_visible:
            x, y = pygame.mouse.get_pos()
            self.pantalla.blit(self.cursor_img, (x - 16, y - 16))