import os
import pygame
from interfaz import interfaz  
from gestor_recursos import gestor_recursos
from motorgrafico import motorgrafico 
from enemigos import enemigos 
from jugador import jugador  
from nivel import nivel 
from torre import torre 
from menu_principal import menu_principal 


class MenuPrincipal:
    def __init__(self, pantalla):
        self.pantalla = pantalla
        self.font = pygame.font.SysFont("consolas", 36)
        self.botones = {}
        self.seleccion = None
        self.crear_botones()

    def crear_botones(self):
        nombres = ["Jugar", "Opciones", "Salir"]
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


def verificar_recursos():
    base = os.path.join(os.path.dirname(__file__), 'assets')
    rutas = {
        "fondo.jpg": os.path.join(base, 'imagen', 'fondo.jpg'),
        "disparo.wav": os.path.join(base, 'sonidos', 'disparo.wav')
    }
    for nombre, ruta in rutas.items():
        if not os.path.exists(ruta):
            print(f"[Diagnóstico] Recurso faltante: {nombre} → {ruta}")
        else:
            print(f"[Diagnóstico]  Recurso encontrado: {nombre}")


pygame.init()
pygame.font.init()
pantalla = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
ANCHO, ALTO = pantalla.get_width(), pantalla.get_height()
pygame.display.set_caption("Defense Zone 3HD") 
verificar_recursos()

reloj = pygame.time.Clock()
menu = MenuPrincipal(pantalla)
interfaz = interfaz(pantalla)
recursos = gestor_recursos()
jugador = jugador(100, 100, interfaz.ancho_panel, ANCHO, ALTO)

# Fondo
try:
    fondo = recursos.cargar_imagen("fondo.jpg")
except pygame.error:
    print("[Main] Cargando fondo.jpg desde gestor de recursos...")
    fondo = pygame.Surface((ANCHO, ALTO))
    fondo.fill((30, 30, 30))
    fuente = pygame.font.SysFont("arial", 24)
    texto = fuente.render("Fondo no encontrado", True, (255, 255, 255))
    fondo.blit(texto, (ANCHO // 2 - texto.get_width() // 2, ALTO // 2 - texto.get_height() // 2))

vidas = 5
puntos = 0
nivel = 1


en_menu = True
corriendo = True
while corriendo:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT or (evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE):
            corriendo = False

        if en_menu:
            seleccion = menu.manejar_evento(evento)
            if seleccion == "Jugar":
                en_menu = False
            elif seleccion == "Salir":
                corriendo = False
        else:
            seleccion = interfaz.manejar_evento(evento)
            if seleccion:
                print(f"[Main] Acción seleccionada: {seleccion}")

    if en_menu:
        menu.dibujar()
    else:
        teclas = pygame.key.get_pressed()
        jugador.mover(teclas)

        pantalla.blit(fondo, (0, 0))
        jugador.dibujar(pantalla)
        interfaz.dibujar_panel(vidas, puntos, nivel)

    pygame.display.flip()
    reloj.tick(60)

pygame.quit()