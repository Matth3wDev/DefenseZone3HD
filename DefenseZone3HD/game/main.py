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
from ControladorMovimiento import ControladorMovimiento


def verificar_recursos():
    base = os.path.join(os.path.dirname(__file__), 'assets')
    rutas = {
        "Mapa.png": os.path.join(base, 'Mapa', 'Mapa.png'),
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
menu = menu_principal(pantalla)
interfaz = interfaz(pantalla)
recursos = gestor_recursos()
jugador = jugador(100, 100, interfaz.ancho_panel, ANCHO, ALTO)

# Fondo
try:
    fondo = recursos.cargar_imagen("Mapa.png")
except pygame.error:
    print("[Main] Cargando Mapa.png desde gestor de recursos...")
    fondo = pygame.Surface((ANCHO, ALTO))
    fondo.fill((30,30,30))
    fuente = pygame.font.SysFont("arial", 24)
    texto = fuente.render("Fondo no encontrado", True, (255, 255, 255))
    fondo.blit(texto, (ANCHO // 2 - texto.get_width() // 2, ALTO // 2 - texto.get_height() // 2))

vidas = 3
puntos = 0
nivel = 3

en_menu = True
corriendo = True
while corriendo:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT or (evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE):
            corriendo = False

        if en_menu:
            seleccion = menu.manejar_evento(evento)
            
            # Manejar selección de niveles
            if seleccion == "selector_niveles":
                # Se abrió el selector de niveles, no hacer nada
                pass
            elif seleccion == "iniciar_nivel_1":
                # Iniciar juego con nivel 1
                nivel = 1
                vidas = 3  # Reiniciar vidas
                puntos = 0  # Reiniciar puntos
                en_menu = False
                print("[Main] Iniciando juego - Nivel 1")
            elif seleccion == "iniciar_nivel_2":
                # Iniciar juego con nivel 2
                nivel = 2
                vidas = 3
                puntos = 0
                en_menu = False
                print("[Main] Iniciando juego - Nivel 2")
            elif seleccion == "iniciar_nivel_3":
                # Iniciar juego con nivel 3
                nivel = 3
                vidas = 3
                puntos = 0
                en_menu = False
                print("[Main] Iniciando juego - Nivel 3")
            elif seleccion == "volver":
                # Volver al menú principal desde selector
                print("[Main] Regresando al menú principal")
            elif seleccion == "Salir":
                corriendo = False
        else:
            seleccion = interfaz.manejar_evento(evento)
            if seleccion:
                print(f"[Main] Acción seleccionada: {seleccion}")
                if seleccion == "Salir":
                    en_menu = True

    if en_menu:
        menu.dibujar()
    else:
        if not interfaz.esta_pausado():
            teclas = pygame.key.get_pressed()
            jugador.mover(teclas)

        pantalla.blit(fondo, (0, 0))
        jugador.dibujar(pantalla)
        interfaz.dibujar_panel(vidas, puntos, nivel)

    pygame.display.flip()
    reloj.tick(60)

pygame.quit()