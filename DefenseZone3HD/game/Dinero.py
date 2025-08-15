import pygame
import json
from enum import Enum

class TipoTransaccion(Enum):
    COMPRA_TORRE = "compra_torre"
    MEJORA_TORRE = "mejora_torre"
    ELIMINAR_ENEMIGO = "eliminar_enemigo"
    COMPLETAR_OLEADA = "completar_oleada"
    COMPLETAR_NIVEL = "completar_nivel"
    BONUS_VELOCIDAD = "bonus_velocidad"
    BONUS_PRECISION = "bonus_precision"
    

class Dinero:
    def __init__(self, cantidad_inicial=1000):
        """
        Sistema monetario del juego
        
        Args:
            cantidad_inicial (int): Dinero inicial del jugador
        """
        self._cantidad = max(0, cantidad_inicial)
        self._cantidad_inicial = cantidad_inicial
        self._total_ganado = 0
        self._total_gastado = 0
        self._historial_transacciones = []
        
        
        self._recompensas = {
            TipoTransaccion.ELIMINAR_ENEMIGO: {
                'tanque': 20,
                'avion': 30,
                'robot': 25,
                'boss': 100
            },
            TipoTransaccion.COMPLETAR_OLEADA: 150,
            TipoTransaccion.COMPLETAR_NIVEL: 500,
            TipoTransaccion.BONUS_VELOCIDAD: 50,    
            TipoTransaccion.BONUS_PRECISION: 25     
        }
        
        
        self._costos = {
            'torre_basica': 100,
            'torre_misiles': 200,
            'torre_laser': 300,
            'torre_llamas': 250,
            'mejora_daño': 50,
            'mejora_velocidad': 75,
            'mejora_rango': 60
        }
    
    @property
    def cantidad(self):
        """Obtiene la cantidad actual de dinero"""
        return self._cantidad
    
    @property
    def total_ganado(self):
        """Obtiene el total de dinero ganado"""
        return self._total_ganado
    
    @property
    def total_gastado(self):
        """Obtiene el total de dinero gastado"""
        return self._total_gastado
    
    @property
    def historial(self):
        """Obtiene el historial de transacciones"""
        return self._historial_transacciones.copy()
    
    def tiene_suficiente(self, cantidad):
        """
        Verifica si el jugador tiene suficiente dinero
        
        Args:
            cantidad (int): Cantidad a verificar
            
        Returns:
            bool: True si tiene suficiente dinero
        """
        return self._cantidad >= cantidad
    
    def gastar(self, cantidad, concepto="Gasto genérico", tipo_item=None):
        """
        Gasta dinero si hay suficiente
        
        Args:
            cantidad (int): Cantidad a gastar
            concepto (str): Descripción del gasto
            tipo_item (str): Tipo de item comprado (opcional)
            
        Returns:
            bool: True si se pudo realizar el gasto
        """
        if not self.tiene_suficiente(cantidad):
            return False
        
        self._cantidad -= cantidad
        self._total_gastado += cantidad
        
       
        transaccion = {
            'tipo': 'gasto',
            'cantidad': cantidad,
            'concepto': concepto,
            'item': tipo_item,
            'saldo_anterior': self._cantidad + cantidad,
            'saldo_actual': self._cantidad
        }
        self._historial_transacciones.append(transaccion)
        
        return True
    
    def ganar(self, cantidad, concepto="Ingreso genérico", tipo_transaccion=None):
        """
        Añade dinero al jugador
        
        Args:
            cantidad (int): Cantidad a añadir
            concepto (str): Descripción del ingreso
            tipo_transaccion (TipoTransaccion): Tipo de transacción
        """
        if cantidad <= 0:
            return
        
        self._cantidad += cantidad
        self._total_ganado += cantidad
        
        
        transaccion = {
            'tipo': 'ingreso',
            'cantidad': cantidad,
            'concepto': concepto,
            'tipo_transaccion': tipo_transaccion.value if tipo_transaccion else None,
            'saldo_anterior': self._cantidad - cantidad,
            'saldo_actual': self._cantidad
        }
        self._historial_transacciones.append(transaccion)
    
    def obtener_costo(self, item):
        """
        Obtiene el costo de un item específico
        
        Args:
            item (str): Nombre del item
            
        Returns:
            int: Costo del item, 0 si no existe
        """
        return self._costos.get(item, 0)
    
    def puede_comprar(self, item):
        """
        Verifica si se puede comprar un item específico
        
        Args:
            item (str): Nombre del item
            
        Returns:
            bool: True si se puede comprar
        """
        costo = self.obtener_costo(item)
        return self.tiene_suficiente(costo)
    
    def comprar_item(self, item):
        """
        Compra un item específico
        
        Args:
            item (str): Nombre del item
            
        Returns:
            bool: True si se pudo comprar
        """
        costo = self.obtener_costo(item)
        if costo > 0:
            return self.gastar(costo, f"Compra de {item}", item)
        return False
    
    def recompensar_eliminacion(self, tipo_enemigo):
        """
        Otorga recompensa por eliminar un enemigo
        
        Args:
            tipo_enemigo (str): Tipo de enemigo eliminado
        """
        recompensas_enemigos = self._recompensas[TipoTransaccion.ELIMINAR_ENEMIGO]
        cantidad = recompensas_enemigos.get(tipo_enemigo, 15)  # 15 por defecto
        
        self.ganar(
            cantidad, 
            f"Eliminación de {tipo_enemigo}", 
            TipoTransaccion.ELIMINAR_ENEMIGO
        )
    
    def recompensar_oleada(self, numero_oleada, enemigos_eliminados=0, tiempo_bonus=False):
        """
        Otorga recompensa por completar una oleada
        
        Args:
            numero_oleada (int): Número de oleada completada
            enemigos_eliminados (int): Cantidad de enemigos eliminados
            tiempo_bonus (bool): Si se completó en tiempo récord
        """
        
        recompensa_base = self._recompensas[TipoTransaccion.COMPLETAR_OLEADA]
        
        
        bonus_oleada = (numero_oleada - 1) * 25
        
        
        bonus_enemigos = enemigos_eliminados * 5
        
        
        bonus_tiempo = 100 if tiempo_bonus else 0
        
        total = recompensa_base + bonus_oleada + bonus_enemigos + bonus_tiempo
        
        concepto = f"Oleada {numero_oleada} completada"
        if tiempo_bonus:
            concepto += " (Bonus de velocidad)"
        
        self.ganar(total, concepto, TipoTransaccion.COMPLETAR_OLEADA)
    
    def recompensar_nivel(self, numero_nivel, vidas_restantes=0):
        """
        Otorga recompensa por completar un nivel
        
        Args:
            numero_nivel (int): Número de nivel completado
            vidas_restantes (int): Vidas que quedaron
        """
        recompensa_base = self._recompensas[TipoTransaccion.COMPLETAR_NIVEL]
        bonus_nivel = numero_nivel * 100
        bonus_vidas = vidas_restantes * 50
        
        total = recompensa_base + bonus_nivel + bonus_vidas
        
        self.ganar(
            total, 
            f"Nivel {numero_nivel} completado", 
            TipoTransaccion.COMPLETAR_NIVEL
        )
    
    def aplicar_bonus(self, tipo_bonus, multiplicador=1.0):
        """
        Aplica bonus especiales
        
        Args:
            tipo_bonus (TipoTransaccion): Tipo de bonus
            multiplicador (float): Multiplicador del bonus
        """
        if tipo_bonus in self._recompensas:
            cantidad = int(self._recompensas[tipo_bonus] * multiplicador)
            self.ganar(cantidad, f"Bonus: {tipo_bonus.value}", tipo_bonus)
    
    def reiniciar(self):
        """Reinicia el sistema monetario a valores iniciales"""
        self._cantidad = self._cantidad_inicial
        self._total_ganado = 0
        self._total_gastado = 0
        self._historial_transacciones.clear()
    
    def obtener_estadisticas(self):
        """
        Obtiene estadísticas del sistema monetario
        
        Returns:
            dict: Diccionario con estadísticas
        """
        return {
            'cantidad_actual': self._cantidad,
            'cantidad_inicial': self._cantidad_inicial,
            'total_ganado': self._total_ganado,
            'total_gastado': self._total_gastado,
            'transacciones_totales': len(self._historial_transacciones),
            'ganancia_neta': self._total_ganado - self._total_gastado
        }
    
    def exportar_historial(self, archivo):
        """
        Exporta el historial a un archivo JSON
        
        Args:
            archivo (str): Ruta del archivo
        """
        try:
            with open(archivo, 'w', encoding='utf-8') as f:
                json.dump({
                    'estadisticas': self.obtener_estadisticas(),
                    'historial': self._historial_transacciones
                }, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error al exportar historial: {e}")
            return False
    
    def __str__(self):
        """Representación en string del objeto"""
        return f"Dinero: ${self._cantidad}"
    
    def __repr__(self):
        """Representación detallada del objeto"""
        return f"Dinero(cantidad={self._cantidad}, ganado={self._total_ganado}, gastado={self._total_gastado})"



class VisualizadorDinero:
    def __init__(self, fuente_size=32):
        """
        Visualizador del dinero en pantalla
        
        Args:
            fuente_size (int): Tamaño de la fuente
        """
        pygame.font.init()
        self.fuente = pygame.font.Font(None, fuente_size)
        self.color_texto = (255, 215, 0)  
        self.color_fondo = (0, 0, 0, 128)  
    
    def dibujar(self, pantalla, dinero, x, y):
        """
        Dibuja el dinero en pantalla
        
        Args:
            pantalla: Surface de pygame
            dinero (Dinero): Objeto dinero
            x (int): Posición X
            y (int): Posición Y
        """
        
        texto = f"${dinero.cantidad:,}"
        superficie_texto = self.fuente.render(texto, True, self.color_texto)
        
        
        ancho_texto = superficie_texto.get_width()
        alto_texto = superficie_texto.get_height()
        
        fondo = pygame.Surface((ancho_texto + 20, alto_texto + 10))
        fondo.fill((0, 0, 0))
        fondo.set_alpha(128)
        
        
        pantalla.blit(fondo, (x - 10, y - 5))
        pantalla.blit(superficie_texto, (x, y))
    
    def dibujar_estadisticas(self, pantalla, dinero, x, y):
        """
        Dibuja estadísticas detalladas del dinero
        
        Args:
            pantalla: Surface de pygame
            dinero (Dinero): Objeto dinero
            x (int): Posición X inicial
            y (int): Posición Y inicial
        """
        stats = dinero.obtener_estadisticas()
        textos = [
            f"Dinero actual: ${stats['cantidad_actual']:,}",
            f"Total ganado: ${stats['total_ganado']:,}",
            f"Total gastado: ${stats['total_gastado']:,}",
            f"Ganancia neta: ${stats['ganancia_neta']:,}"
        ]
        
        for i, texto in enumerate(textos):
            superficie = self.fuente.render(texto, True, self.color_texto)
            pantalla.blit(superficie, (x, y + i * 35))