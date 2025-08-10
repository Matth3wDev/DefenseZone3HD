import pygame
import torre  

pygame.init()


ANCHO_VENTANA = 800
ALTO_VENTANA = 600

ventana = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
clock = pygame.time.Clock()


class torre:
    def __init__(self):
        self.vidas = 3
        self.puntos = 0
        self.nivel = 3
        self.derrota = False

estado = torre()


lista_torres = []
lista_enemigos = []  
colocando_tanque = False


boton_ametralladora = pygame.Rect(10, 10, 100, 50)

def verificar_derrota():
    for enemigo in lista_enemigos:
        for torre_obj in lista_torres:
            distancia = ((enemigo.x - torre_obj.x)**2 + (enemigo.y - torre_obj.y)**2)**0.5
            if distancia < 50:  
                estado.derrota = True
                print("¡Derrota! Un enemigo alcanzó la torre.")
                return

run = True
while run:
    ventana.fill((0, 0, 0))  

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if boton_ametralladora.collidepoint(event.pos):
                colocando_tanque = True
            elif colocando_tanque:
                nuevo_tanque = torre(event.pos[0], event.pos[1])
                lista_torres.append(nuevo_tanque)
                colocando_tanque = False

    if colocando_tanque:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        

    verificar_derrota()
    if estado.derrota:
        run = False  

    pygame.display.update()
    clock.tick(60)