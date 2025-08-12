import math
import random
import pygame
from enemigos import enemigos  

class ComputadoraIA:
    def __init__(self, enemigos, torres):
        self.enemigos = enemigos  
        self.torres = torres
        self.dificultad = "medio"  
        self.tiempo_ultimo_spawn = 0
        self.spawn_cooldown = 3000  
        self.oleadas_enviadas = 0
        self.estrategia_actual = "tanques"  
        
    def calcular_distancia(self, pos1, pos2):
        """Calcula distancia euclidiana entre dos posiciones"""
        return math.sqrt((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2)
    
    def evaluar_amenaza_torre(self, torre):
        """Evalúa qué tan amenazante es una torre"""
        amenaza = 0
        if hasattr(torre, 'daño'):
            amenaza += torre.daño * 2
        if hasattr(torre, 'rango'):
            amenaza += torre.rango
        if hasattr(torre, 'velocidad_ataque'):
            amenaza += torre.velocidad_ataque
        return amenaza
    
    def encontrar_torre_mas_debil(self):
        """Encuentra la torre con menos salud"""
        if not self.torres:
            return None
        return min(self.torres, key=lambda t: getattr(t, 'salud', 100))
    
    def encontrar_torre_mas_amenazante(self):
        """Encuentra la torre más peligrosa"""
        if not self.torres:
            return None
        return max(self.torres, key=self.evaluar_amenaza_torre)
    
    def asignar_objetivos(self):
        """Asigna objetivos estratégicos a cada enemigo"""
        torres_disponibles = self.torres.copy()
        
        for enemigo in self.enemigos:
            if not torres_disponibles:
                enemigo.objetivo = None
                continue
                
           
            if enemigo.nombre == "Tanque":
                enemigo.objetivo = self.encontrar_torre_mas_amenazante()
            else:
                enemigo.objetivo = self.encontrar_torre_mas_debil()
    
    def cambiar_estrategia(self):
        """Mantiene siempre la estrategia de tanques"""
        self.estrategia_actual = "tanques"
    
    def generar_oleada(self, sprite_paths=None):
        """Genera nuevos enemigos - solo tanques"""
        tiempo_actual = pygame.time.get_ticks()
        if tiempo_actual - self.tiempo_ultimo_spawn < self.spawn_cooldown:
            return []
        
        self.tiempo_ultimo_spawn = tiempo_actual
        nuevos_enemigos = []
        
       
        if not sprite_paths:
            sprite_paths = {
                'tanque': 'sprites/tanque.png'
            }
        
       
        multiplicador = 1
        if self.dificultad == "dificil":
            multiplicador = 1.5
        elif self.dificultad == "facil":
            multiplicador = 0.7
        
        
        for i in range(int(2 * multiplicador)):
            nuevos_enemigos.append(Tanque(sprite_paths.get('tanque', 'sprites/tanque.png'), 800, 150 + i*80))
        
        self.oleadas_enviadas += 1
        return nuevos_enemigos
    
    def ejecutar_turno(self):
        """Ejecuta el turno de la IA con estrategia de tanques"""
        
        if self.oleadas_enviadas % 3 == 0:
            self.cambiar_estrategia()
        
        
        self.asignar_objetivos()
        
        acciones = []
        enemigos_a_eliminar = []
        
        for enemigo in self.enemigos[:]: 
            if enemigo.salud <= 0:
                enemigos_a_eliminar.append(enemigo)
                continue
                
            
            torre_cercana = None
            distancia_minima = float('inf')
            
            for torre in self.torres:
                distancia = self.calcular_distancia(enemigo.rect.center, torre.rect.center)
                if distancia < distancia_minima:
                    distancia_minima = distancia
                    torre_cercana = torre
            
            
            if torre_cercana and enemigo.rect.colliderect(torre_cercana.rect):
                resultado = enemigo.atacar(torre_cercana)
                if resultado:
                    acciones.append(resultado)
                    enemigo.estado = "atacando"
            else:
                
                if enemigo.objetivo:
                    
                    dx = enemigo.objetivo.rect.centerx - enemigo.rect.centerx
                    dy = enemigo.objetivo.rect.centery - enemigo.rect.centery
                    distancia = math.sqrt(dx**2 + dy**2)
                    
                    if distancia > 0:
                        # Normaliza y aplica velocidad
                        enemigo.rect.x += int((dx / distancia) * enemigo.velocidad * 0.7)
                        enemigo.rect.y += int((dy / distancia) * enemigo.velocidad * 0.3)
                else:
                    
                    enemigo.update()
                
                enemigo.estado = "avanzando"
                acciones.append(f"{enemigo.nombre} avanza estratégicamente hacia objetivo")
        
        
        for enemigo in enemigos_a_eliminar:
            if enemigo in self.enemigos:
                self.enemigos.remove(enemigo)
        
       
        if len(self.enemigos) < 2:  
            nuevos_enemigos = self.generar_oleada()
            self.enemigos.extend(nuevos_enemigos)
            if nuevos_enemigos:
                acciones.append(f"¡Nueva oleada de {len(nuevos_enemigos)} tanques!")
        
        return acciones
    
    def ajustar_dificultad(self, nueva_dificultad):
        """Cambia la dificultad de la IA"""
        self.dificultad = nueva_dificultad
        
        if nueva_dificultad == "facil":
            self.spawn_cooldown = 5000  
        elif nueva_dificultad == "dificil":
            self.spawn_cooldown = 1500  
        else:
            self.spawn_cooldown = 3000  



class Tanque(enemigos):
    def __init__(self, sprite_path, x, y):
        super().__init__("Tanque", 300, 1, 30, sprite_path, x, y)
        self.cooldown_ataque = 2000



def main():
    pygame.init()
    pantalla = pygame.display.set_mode((1000, 600))
    reloj = pygame.time.Clock()
    
    
    enemigos_lista = []
    torres_lista = []  
    
    
    ia_computadora = ComputadoraIA(enemigos_lista, torres_lista)
    
    
    sprite_paths = {
        'tanque': 'sprites/tanque.png'    
    }
    
    
    primeros_enemigos = [
        Tanque(sprite_paths['tanque'], 800, 200),
        Tanque(sprite_paths['tanque'], 850, 280)
    ]
    enemigos_lista.extend(primeros_enemigos)
    
    corriendo = True
    while corriendo:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                corriendo = False
        
       
        acciones_ia = ia_computadora.ejecutar_turno()
        
        
        for enemigo in enemigos_lista:
            enemigo.update()
        
        
        pantalla.fill((50, 50, 50))
        
       
        for enemigo in enemigos_lista:
            enemigo.dibujar(pantalla)
        
        pygame.display.flip()
        reloj.tick(60)
    
    pygame.quit()


if __name__ == "__main__":
    main()