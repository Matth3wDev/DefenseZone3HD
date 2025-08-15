import os
import pygame
from interfaz import interfaz   
from gestor_recursos import gestor_recursos 
from motorgrafico import motorgrafico 
from enemigos import enemigos 
from jugador import jugador  
from nivel import nivel 
from torre import torre 
from TorreAmetralladora import TorreAmetralladora
from torreMisil import torreMisil
from torresLlamas import torresLlamas
from menu_principal import menu_principal
from ControladorMovimiento import ControladorMovimiento
from ComputadoraIA import ComputadoraIA
from Dinero import Dinero, VisualizadorDinero, TipoTransaccion

class DefenseZone3HD:
    def __init__(self):
        pygame.init()
        self.pantalla = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.ANCHO, self.ALTO = self.pantalla.get_size()
        pygame.display.set_caption("Defense Zone 3HD")
        
        
        self.recursos = gestor_recursos()
        self.motor_grafico = motorgrafico(self.pantalla)
        self.interfaz = interfaz(self.pantalla)
        self.jugador = jugador(100, 100, self.interfaz.ancho_panel, self.ANCHO, self.ALTO)
        self.menu = menu_principal(self.pantalla)
        
        
        self.torres = []
        self.enemigos_activos = []
        
        
        self.controlador = ControladorMovimiento(self.torres)
        self.ia = ComputadoraIA(self.enemigos_activos, self.torres)
        
        
        self.sistema_dinero = Dinero(1000) 
        self.visualizador_dinero = VisualizadorDinero(36)  
        
        
        self.estado = "MENU"
        self.nivel_actual = None
        self.vidas = 20
        self.puntos = 0
        self.oleada = 0
        self.enemigos_eliminados = 0  
        
        self.cargar_recursos()
        self.ia.ajustar_dificultad("medio")
    
    def cargar_recursos(self):
        """Carga todos los assets verificando su existencia"""
        try:
            self.fondo = self.recursos.cargar_imagen("Mapa.png")
            self.sonido_disparo = self.recursos.cargar_sonido("disparo.wav")
        except Exception as e:
            print(f"Error cargando recursos: {e}")
            self.fondo = pygame.Surface((self.ANCHO, self.ALTO))
            self.fondo.fill((30, 30, 30))
    
    def iniciar_nivel(self, num_nivel):
        """Configura un nivel nuevo con parámetros progresivos"""
        
        if num_nivel == 1:
            dificultad = 'fácil'
        elif num_nivel == 2:
            dificultad = 'medio'
        else:
            dificultad = 'difícil'
        
       
        self.nivel_actual = nivel(num_nivel, dificultad)
        
        
        self.nivel_actual.rutas = self.generar_rutas(num_nivel)
        self.nivel_actual.dinero = self.sistema_dinero.cantidad 
        self.nivel_actual.vidas = self.vidas
        self.nivel_actual.oleada_activa = False
        
       
        def iniciar_oleada(oleada_num):
            self.nivel_actual.oleada_activa = True
            print(f"Iniciando oleada {oleada_num}")
            
            self.enemigos_eliminados = 0
        
        def actualizar():

            self.nivel_actual.dinero = self.sistema_dinero.cantidad
            
            
            enemigos_vivos = [e for e in self.enemigos_activos if hasattr(e, 'salud') and e.salud > 0]
            enemigos_muertos = len(self.enemigos_activos) - len(enemigos_vivos)
            
            
            if enemigos_muertos > self.enemigos_eliminados:
                nuevos_eliminados = enemigos_muertos - self.enemigos_eliminados
                for _ in range(nuevos_eliminados):
                    
                    self.sistema_dinero.recompensar_eliminacion('tanque')
                self.enemigos_eliminados = enemigos_muertos
            
        def dibujar(pantalla):
            
            pass
        
        # Asignar los métodos al objeto nivel
        self.nivel_actual.iniciar_oleada = iniciar_oleada
        self.nivel_actual.actualizar = actualizar
        self.nivel_actual.dibujar = dibujar
        
        self.oleada = 0
        self.estado = "JUGANDO"
        self.torres = []
        self.enemigos_activos = []
        self.enemigos_eliminados = 0
        
        self.controlador.lista_torres = self.torres
        self.ia.torres = self.torres
        self.ia.enemigos = self.enemigos_activos
        
        self.generar_oleada_inicial()
    
    def generar_rutas(self, nivel):
        """Genera rutas con patrones complejos según el nivel"""
        if nivel == 1:
            return [(0, 300), (400, 300), (400, 500), (self.ANCHO, 500)]
        elif nivel == 2:
            return [(0, 200), (300, 200), (300, 400), (600, 400), (600, 100), (self.ANCHO, 100)]
        else:
            return [(0, y) for y in range(100, self.ALTO, 100)]
    
    def generar_oleada_inicial(self):
        """Genera la primera oleada de enemigos"""
        sprite_path = os.path.join('assets', 'sprites', 'tanque.png')
        if not os.path.exists(sprite_path):
            print(f"Advertencia: No se encontró el sprite en {sprite_path}")
            sprite_path = None
            
        primeros_enemigos = self.ia.generar_oleada({'tanque': sprite_path})
        if primeros_enemigos:
            self.enemigos_activos.extend(primeros_enemigos)
            if hasattr(self.nivel_actual, 'enemigos'):
                self.nivel_actual.enemigos.extend(primeros_enemigos)
    
    def manejar_eventos(self):
        eventos_disparo = []  
        
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return False
            
            
            if evento.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
                eventos_disparo.append(evento)
            
            if self.estado == "MENU":
                accion = self.menu.manejar_evento(evento)
                
                if accion and isinstance(accion, str):
                    if accion.startswith("iniciar_nivel_"):
                        try:
                            num_nivel = int(accion.split("_")[-1])
                            self.iniciar_nivel(num_nivel)
                        except (IndexError, ValueError):
                            print(f"Error: Formato de nivel inválido en {accion}")
                    elif accion == "Salir":
                        return False
            
            elif self.estado == "JUGANDO":
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_p:
                        self.estado = "PAUSA"
                
                accion = self.interfaz.manejar_evento(evento)
                if accion:
                    pos = pygame.mouse.get_pos()
                    
                    if accion == "TorreBasica":
                        if self.sistema_dinero.puede_comprar('torre_basica'):
                            self.agregar_torre(torre, pos, 'torre_basica')
                        else:
                            print("No tienes suficiente dinero para Torre Básica")
                    elif accion == "TorreMisiles":
                        if self.sistema_dinero.puede_comprar('torre_misiles'):
                            self.agregar_torre(torreMisil, pos, 'torre_misiles')
                        else:
                            print("No tienes suficiente dinero para Torre de Misiles")
                    elif accion == "TorreLaser":
                        if self.sistema_dinero.puede_comprar('torre_laser'):
                            self.agregar_torre(TorreAmetralladora, pos, 'torre_laser')
                        else:
                            print("No tienes suficiente dinero para Torre Láser")
                    elif accion == "TorreLlamas":
                        if self.sistema_dinero.puede_comprar('torre_llamas'):
                            self.agregar_torre(torresLlamas, pos, 'torre_llamas')
                        else:
                            print("No tienes suficiente dinero para Torre de Llamas")
            
            elif self.estado == "PAUSA":
                if evento.type == pygame.KEYDOWN and evento.key == pygame.K_p:
                    self.estado = "JUGANDO"
        
        
        if self.estado == "JUGANDO":
            teclas = pygame.key.get_pressed()
            if hasattr(self.controlador, 'mover_torres'):
                self.controlador.mover_torres(teclas)
            
            
            if eventos_disparo and hasattr(self.controlador, 'manejar_disparo'):
                self.controlador.manejar_disparo(eventos_disparo)
        
        return True
    
    def agregar_torre(self, tipo_torre, posicion, tipo_item):
        """Método seguro para agregar torres usando el sistema monetario"""
        if not hasattr(self.nivel_actual, 'agregar_torre'):
            return
        
        
        if self.sistema_dinero.comprar_item(tipo_item):
            nueva_torre = tipo_torre(*posicion)
            self.nivel_actual.agregar_torre(nueva_torre)
            self.torres.append(nueva_torre)
            print(f"Torre {tipo_item} comprada por ${self.sistema_dinero.obtener_costo(tipo_item)}")
        else:
            print(f"No se pudo comprar {tipo_item}")
    
    def actualizar(self):
        if self.estado != "JUGANDO":
            return
        
        
        if hasattr(self.ia, 'ejecutar_turno'):
            acciones_ia = self.ia.ejecutar_turno()
            for accion in acciones_ia:
                print(f"IA: {accion}")
        
        
        self.enemigos_activos = [e for e in self.enemigos_activos if hasattr(e, 'salud') and e.salud > 0]
        
       
        if hasattr(self.nivel_actual, 'oleada_activa'):
            if not self.nivel_actual.oleada_activa and self.oleada < 10:
                if hasattr(self.nivel_actual, 'iniciar_oleada'):
                    self.nivel_actual.iniciar_oleada(self.oleada)
                self.oleada += 1
            
            
            elif self.nivel_actual.oleada_activa and not self.enemigos_activos:
                
                self.sistema_dinero.recompensar_oleada(
                    self.oleada, 
                    self.enemigos_eliminados,
                    tiempo_bonus=False  
                )
                self.nivel_actual.oleada_activa = False
                print(f"¡Oleada {self.oleada} completada! Bonus: $150+")
        
        
        if hasattr(self.nivel_actual, 'actualizar'):
            self.nivel_actual.actualizar()
        if hasattr(self.jugador, 'actualizar'):
            self.jugador.actualizar()
        
        #
        if hasattr(self.nivel_actual, 'vidas'):
            if self.nivel_actual.vidas <= 0:
                self.estado = "GAME_OVER"
            elif self.oleada >= 10 and not self.enemigos_activos:
                
                self.sistema_dinero.recompensar_nivel(
                    getattr(self.nivel_actual, 'numero_nivel', 1),
                    self.nivel_actual.vidas
                )
                self.estado = "VICTORIA"
                print(f"¡Nivel completado! Bonus: $500+ por vidas restantes: {self.nivel_actual.vidas}")
    
    def renderizar(self):
        self.pantalla.blit(self.fondo, (0, 0))
        
        if self.estado == "MENU":
            if hasattr(self.menu, 'dibujar'):
                self.menu.dibujar()
        
        elif self.estado in ("JUGANDO", "PAUSA"):
            if hasattr(self.nivel_actual, 'dibujar'):
                self.nivel_actual.dibujar(self.pantalla)
            
            if hasattr(self.jugador, 'dibujar'):
                self.jugador.dibujar(self.pantalla)
            
            if hasattr(self.interfaz, 'dibujar_panel'):
                self.interfaz.dibujar_panel(
                    vidas=getattr(self.nivel_actual, 'vidas', 0),
                    puntos=self.puntos,
                    nivel=getattr(self.nivel_actual, 'numero_nivel', 1),
                    dinero=self.sistema_dinero.cantidad  
                )
            
            
            self.visualizador_dinero.dibujar(
                self.pantalla, 
                self.sistema_dinero, 
                20, 20
            )
            
            
            if self.estado == "PAUSA":
                if hasattr(self.motor_grafico, 'dibujar_texto'):
                    self.motor_grafico.dibujar_texto("PAUSA", self.ANCHO//2, self.ALTO//2, tamaño=72)
                
                
                self.visualizador_dinero.dibujar_estadisticas(
                    self.pantalla,
                    self.sistema_dinero,
                    50, 
                    self.ALTO//2 + 100
                )
        
        elif self.estado == "GAME_OVER":
            
            if hasattr(self.motor_grafico, 'dibujar_texto'):
                self.motor_grafico.dibujar_texto("GAME OVER", self.ANCHO//2, self.ALTO//2-100, tamaño=72)
                stats = self.sistema_dinero.obtener_estadisticas()
                self.motor_grafico.dibujar_texto(f"Dinero final: ${stats['cantidad_actual']:,}", 
                                               self.ANCHO//2, self.ALTO//2, tamaño=36)
                self.motor_grafico.dibujar_texto(f"Total ganado: ${stats['total_ganado']:,}", 
                                               self.ANCHO//2, self.ALTO//2+50, tamaño=36)
        
        elif self.estado == "VICTORIA":
            
            if hasattr(self.motor_grafico, 'dibujar_texto'):
                self.motor_grafico.dibujar_texto("¡VICTORIA!", self.ANCHO//2, self.ALTO//2-100, tamaño=72)
                stats = self.sistema_dinero.obtener_estadisticas()
                self.motor_grafico.dibujar_texto(f"Dinero final: ${stats['cantidad_actual']:,}", 
                                               self.ANCHO//2, self.ALTO//2, tamaño=36)
                self.motor_grafico.dibujar_texto(f"Ganancia neta: ${stats['ganancia_neta']:,}", 
                                               self.ANCHO//2, self.ALTO//2+50, tamaño=36)
        
        pygame.display.flip()
    
    def ejecutar(self):
        reloj = pygame.time.Clock()
        corriendo = True
        
        while corriendo:
            try:
                corriendo = self.manejar_eventos()
                self.actualizar()
                self.renderizar()
                reloj.tick(60)
            except Exception as e:
                print(f"Error en el bucle principal: {e}")
                
                self.sistema_dinero.exportar_historial("error_log_dinero.json")
                corriendo = False

if __name__ == "__main__":
    try:
        juego = DefenseZone3HD()
        juego.ejecutar()
    except Exception as e:
        print(f"Error al iniciar el juego: {e}")
    finally:
        pygame.quit()