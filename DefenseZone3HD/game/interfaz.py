import pygame

class interfaz:
    def __init__(self, pantalla):
        self.pantalla = pantalla
        self.ancho_panel = 0  
        self.font = pygame.font.SysFont("consolas", 24)
        self.font_small = pygame.font.SysFont("consolas", 18)
        self.botones = {}
        self.seleccion_actual = None
        self.pausado = False
        self.interfaz_visible = False
        self.crear_boton_toggle()
        self.crear_interfaz_modal()

    def crear_boton_toggle(self):
        
        self.boton_toggle = pygame.Rect(self.pantalla.get_width() - 120, 10, 100, 35)

    def crear_interfaz_modal(self):
        
        ancho_modal = 300
        alto_modal = 250  # Reducido porque hay menos botones
        x = (self.pantalla.get_width() - ancho_modal) // 2
        y = (self.pantalla.get_height() - alto_modal) // 2
        self.modal_rect = pygame.Rect(x, y, ancho_modal, alto_modal)
        
        
        nombres = ["Pausar", "Salir"]  # Quitamos Nivel 1, Nivel 2, Nivel 3
        self.botones = {}
        
        for i, nombre in enumerate(nombres):
            btn_x = self.modal_rect.x + 20
            btn_y = self.modal_rect.y + 120 + i * 60
            btn_rect = pygame.Rect(btn_x, btn_y, 260, 45)
            self.botones[nombre] = btn_rect

    def dibujar_boton_toggle(self):
        # Solo dibujar el botón cuando el juego NO está pausado
        if not self.pausado:
            color_toggle = (80, 180, 80)
            
            pygame.draw.rect(self.pantalla, color_toggle, self.boton_toggle)
            pygame.draw.rect(self.pantalla, (200, 200, 200), self.boton_toggle, 2)
            
            texto = "Pausa"
            
            superficie_texto = self.font_small.render(texto, True, (255, 255, 255))
            texto_rect = superficie_texto.get_rect(center=self.boton_toggle.center)
            self.pantalla.blit(superficie_texto, texto_rect)

    def dibujar_interfaz_modal(self, vidas, puntuacion, nivel):
        if not self.interfaz_visible:
            return
        
        
        overlay = pygame.Surface((self.pantalla.get_width(), self.pantalla.get_height()))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        self.pantalla.blit(overlay, (0, 0))
        
        
        pygame.draw.rect(self.pantalla, (40, 40, 60), self.modal_rect)
        pygame.draw.rect(self.pantalla, (200, 200, 200), self.modal_rect, 3)
        
        
        titulo = self.font.render("JUEGO PAUSADO", True, (255, 255, 255))
        titulo_rect = titulo.get_rect(centerx=self.modal_rect.centerx, y=self.modal_rect.y + 20)
        self.pantalla.blit(titulo, titulo_rect)
        
        
        for nombre, rect in self.botones.items():
            
            if nombre == "Pausar":
                color_base = (180, 80, 80) if self.pausado else (80, 180, 80)
                color = color_base if nombre == self.seleccion_actual else (color_base[0]//2, color_base[1]//2, color_base[2]//2)
                texto_boton = "Reanudar" if self.pausado else "Pausar"
            else:
                color = (80, 120, 180) if nombre == self.seleccion_actual else (60, 60, 90)
                texto_boton = nombre
            
            pygame.draw.rect(self.pantalla, color, rect)
            pygame.draw.rect(self.pantalla, (200, 200, 200), rect, 2)
            
            texto = self.font_small.render(texto_boton, True, (255, 255, 255))
            texto_rect = texto.get_rect(center=rect.center)
            self.pantalla.blit(texto, texto_rect)

    def dibujar(self, vidas, puntuacion, nivel):
        
        self.dibujar_boton_toggle()
        
        
        if self.interfaz_visible:
            self.dibujar_interfaz_modal(vidas, puntuacion, nivel)

    def manejar_evento(self, evento):
        if evento.type == pygame.MOUSEBUTTONDOWN:
            pos = evento.pos
            
            # Solo permitir clic en el botón toggle cuando NO está pausado
            if self.boton_toggle.collidepoint(pos) and not self.pausado:
                self.pausado = True
                self.interfaz_visible = True  # Abrir la interfaz cuando se pausa
                print(f"[Interfaz] Juego pausado")
                return "toggle_pausa"
            
            
            if self.interfaz_visible:
                for nombre, rect in self.botones.items():
                    if rect.collidepoint(pos):
                        self.seleccion_actual = nombre
                        
                        if nombre == "Pausar":
                            # Cambio: Al hacer clic en Reanudar, cierra la ventana Y reanuda el juego
                            if self.pausado:  # Si está pausado, reanudar
                                self.pausado = False
                                self.interfaz_visible = False  # Cerrar ventana
                                print(f"[Interfaz] Juego reanudado - Ventana cerrada")
                                return "toggle_pausa"
                            else:  # Si no está pausado, pausar
                                self.pausado = True
                                print(f"[Interfaz] Juego pausado")
                                return "toggle_pausa"
                        else:
                            print(f"[Interfaz] Botón seleccionado: {nombre}")
                            self.interfaz_visible = False
                            return nombre
                
                
                if not self.modal_rect.collidepoint(pos):
                    self.interfaz_visible = False
                    return "cerrar_interfaz"
            else:
                # Si la interfaz no está visible, hacer clic derecho para abrir menú
                if evento.button == 3:  # Botón derecho del ratón
                    self.interfaz_visible = True
                    print(f"[Interfaz] Interfaz abierta con botón derecho")
                    return "toggle_interfaz"
        
        # Tecla ESC para abrir/cerrar interfaz
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_TAB:
                self.interfaz_visible = not self.interfaz_visible
                print(f"[Interfaz] Interfaz {'abierta' if self.interfaz_visible else 'cerrada'} con TAB")
                return "toggle_interfaz"
        
        return None
    
    def esta_pausado(self):
        """Método para que otros módulos puedan consultar el estado de pausa"""
        return self.pausado
    
    def pausar(self):
        """Método para pausar desde código"""
        self.pausado = True
    
    def reanudar(self):
        """Método para reanudar desde código"""
        self.pausado = False
    
    def toggle_pausa(self):
        """Método para alternar el estado de pausa"""
        self.pausado = not self.pausado
    
    def abrir_interfaz(self):
        """Abrir la interfaz desde código"""
        self.interfaz_visible = True
    
    def cerrar_interfaz(self):
        """Cerrar la interfaz desde código"""
        self.interfaz_visible = False
    
    def esta_interfaz_visible(self):
        """Consultar si la interfaz está visible"""
        return self.interfaz_visible
    
    def dibujar_panel(self, vidas, puntuacion, nivel):
        """Método para compatibilidad con código existente"""
        self.dibujar(vidas, puntuacion, nivel)