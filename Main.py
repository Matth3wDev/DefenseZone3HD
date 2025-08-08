import pygame
import Variables
from Torre import torre
pygame.init()
ventana = pygame.display.set_mode((Variables.ancho_ventana,Variables.alto_ventana))

run = True
while run :
    for event in pygame.event.get():
        #cerrar juego
        if event.type == pygame.QUIT:
            run = False
pygame.display.updade()

boton_ametralladora = pygame.Rect(10, 10, 100, 50)  # El botón torre

if event.type == pygame.MOUSEBUTTONDOWN:
    if boton_ametralladora.collidepoint(event.pos):
        colocando_tanque = True
    #mouse_x, mouse_y es la ubicacion del mouse(torre)
if colocando_tanque:
    mouse_x, mouse_y = pygame.mouse.get_pos()
    # Dibuja la imagen del tanque centrada en el cursor
    screen.blit(imagen_torre, (mouse_x - imagen_torre.get_width() // 2, mouse_y - imagen_torre.get_height() // 2))

if colocando_tanque and event.type == pygame.MOUSEBUTTONDOWN:
    # Asegurarse de que no es un clic en la interfaz de usuario
    if not algun_rectangulo_ui_collidepoint(event.pos): 
        # Aquí crearías una instancia de tu clase Tanque
        nuevo_tanque = torre(event.pos[0], event.pos[1])
        lista_torres.append(nuevo_tanque)
        colocando_tanque = False
        
        

 