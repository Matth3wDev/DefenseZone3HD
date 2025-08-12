import pygame
from gestor_recursos import gestor_recursos

class menu_principal:
    def __init__(self, pantalla):
        self.pantalla = pantalla
        self.font = pygame.font.SysFont("consolas", 36)
        self.font_small = pygame.font.SysFont("consolas", 24)
        self.botones = {}
        self.botones_niveles = {}
        self.seleccion = None
        self.recursos = gestor_recursos()
        self.selector_nivel_visible = False
        self.nivel_seleccionado = None
        
        
        try:
            self.fondo = self.recursos.cargar_interfaz("Window.png") 
        except:
            self.fondo = None
            
        self.crear_botones()
        self.crear_selector_niveles()

    def crear_botones(self):
        nombres = ["Jugar", "Salir"]
        ancho = 300
        alto = 60
        x = (self.pantalla.get_width() - ancho) // 2
        for i, nombre in enumerate(nombres):
            y = 250 + i * 100
            rect = pygame.Rect(x, y, ancho, alto)
            self.botones[nombre] = rect

    def crear_selector_niveles(self):
        
        ancho_modal = 400
        alto_modal = 350
        x = (self.pantalla.get_width() - ancho_modal) // 2
        y = (self.pantalla.get_height() - alto_modal) // 2
        self.modal_rect = pygame.Rect(x, y, ancho_modal, alto_modal)
        
        
        niveles = ["Nivel 1", "Nivel 2", "Nivel 3", "Volver"]
        self.botones_niveles = {}
        
        for i, nivel in enumerate(niveles):
            btn_x = self.modal_rect.x + 50
            btn_y = self.modal_rect.y + 100 + i * 60
            btn_rect = pygame.Rect(btn_x, btn_y, 300, 50)
            self.botones_niveles[nivel] = btn_rect

    def dibujar(self):
        
        if self.fondo:
            self.pantalla.blit(self.fondo, (0, 0))
        else:
            self.pantalla.fill((20, 20, 40))
        
        
        titulo = self.font.render("Defense Zone 3HD", True, (255, 255, 255))
        titulo_rect = titulo.get_rect(center=(self.pantalla.get_width() // 2, 150))
        self.pantalla.blit(titulo, titulo_rect)

        
        for nombre, rect in self.botones.items():
            pygame.draw.rect(self.pantalla, (70, 100, 160), rect)
            pygame.draw.rect(self.pantalla, (255, 255, 255), rect, 2)
            texto = self.font.render(nombre, True, (255, 255, 255))
            texto_rect = texto.get_rect(center=rect.center)
            self.pantalla.blit(texto, texto_rect)

        
        if self.selector_nivel_visible:
            self.dibujar_selector_niveles()

    def dibujar_selector_niveles(self):
        
        overlay = pygame.Surface((self.pantalla.get_width(), self.pantalla.get_height()))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        self.pantalla.blit(overlay, (0, 0))
        
        
        pygame.draw.rect(self.pantalla, (40, 40, 60), self.modal_rect)
        pygame.draw.rect(self.pantalla, (200, 200, 200), self.modal_rect, 3)
        
        
        titulo = self.font_small.render("SELECCIONAR NIVEL", True, (255, 255, 255))
        titulo_rect = titulo.get_rect(centerx=self.modal_rect.centerx, y=self.modal_rect.y + 30)
        self.pantalla.blit(titulo, titulo_rect)
        
        
        for nombre, rect in self.botones_niveles.items():
            
            if nombre == "Volver":
                color = (160, 80, 80)
            else:
                color = (80, 120, 180)
            
            pygame.draw.rect(self.pantalla, color, rect)
            pygame.draw.rect(self.pantalla, (200, 200, 200), rect, 2)
            
            texto = self.font_small.render(nombre, True, (255, 255, 255))
            texto_rect = texto.get_rect(center=rect.center)
            self.pantalla.blit(texto, texto_rect)

    def manejar_evento(self, evento):
        if evento.type == pygame.MOUSEBUTTONDOWN:
            pos = evento.pos
            
            
            if self.selector_nivel_visible:
                # Verificar clics en botones de niveles
                for nombre, rect in self.botones_niveles.items():
                    if rect.collidepoint(pos):
                        if nombre == "Volver":
                            self.selector_nivel_visible = False
                            print("[MenuPrincipal] Volviendo al menú principal")
                            return "volver"
                        else:
                            # Seleccionar nivel
                            self.nivel_seleccionado = nombre
                            self.selector_nivel_visible = False
                            print(f"[MenuPrincipal] Nivel seleccionado: {nombre}")
                            return f"iniciar_{nombre.lower().replace(' ', '_')}"  
                
                
                if not self.modal_rect.collidepoint(pos):
                    self.selector_nivel_visible = False
                    return "volver"
            
            else:
                
                for nombre, rect in self.botones.items():
                    if rect.collidepoint(pos):
                        if nombre == "Jugar":
                            
                            self.selector_nivel_visible = True
                            print("[MenuPrincipal] Abriendo selector de niveles")
                            return "selector_niveles"
                        else:
                            
                            self.seleccion = nombre
                            print(f"[MenuPrincipal] Selección: {nombre}")
                            return nombre
        
        
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_ESCAPE and self.selector_nivel_visible:
                self.selector_nivel_visible = False
                return "volver"
        
        return None
    
    def get_nivel_seleccionado(self):
        """Método para obtener el nivel seleccionado"""
        return self.nivel_seleccionado
    
    def cerrar_selector(self):
        """Método para cerrar el selector desde código"""
        self.selector_nivel_visible = False