import os, sys
import pygame
from pygame.locals import *
from random import uniform
from data import load_image


# Constantes

# El precio minimo:
MIN_PRECIO = 100
# Lo que se resta al precio cuando llega un bola al bar:
RESTA_PRECIO = 10000
# Lo que aumenta el precio con cada tick:
PRECIO_TICK = 10
# Parametros opr defecto para el bar:
PRECIO_DEFAULT = 1000
HUMOR_DEFAULT = 'moody'
VELOCIDAD_HUMOR_DEFAULT = 500


class Bar:
    def __init__(self, precio=None, humor=None, velocidadHumor=None):
	self.image, self.rect = load_image('bar'+str(int(round(uniform(1,2))))+'_'+str(int(round(uniform(1,3))))+'.gif')
	
        if precio is None:
            self.precio = PRECIO_DEFAULT
        else:
            self.precio = precio

        if humor is None or humor not in ['happy', 'moody', 'angry']:
            self.humor = HUMOR_DEFAULT
        else:  
            self.humor = humor

        if velocidadHumor is None:
            self.velocidadHumor = VELOCIDAD_HUMOR_DEFAULT
        else:
            self.velocidadHumor = velocidadHumor

        self.cambioHumor = self.generar_velocidad_humor()
        self.alcohol = False

    def generar_velocidad_humor(self):
        return int(round(self.velocidadHumor*uniform(0.5, 2)))

    def update(self):
        if self.alcohol:
            self.humor = 'happy'
            self.cambioHumor = self.generar_velocidad_humor()
            self.precio = max(MIN_PRECIO, self.precio-RESTA_PRECIO)
        else:
            self.precio = self.precio + PRECIO_TICK
            self.cambioHumor = self.cambioHumor - 1
            if self.cambioHumor == 0:
                if self.humor == 'angry':
                    self.mandarMatones()
                elif self.humor == 'moody':
                    self.humor = 'angry'
                elif self.humor == 'happy':
                    self.humor = 'moody'

                self.cambioHumor = self.generar_velocidad_humor()
        self.alcohol = False

    def draw(self, screen, x, y):

        # Dibujar el precio 
        bg = 5, 5, 5
        fg = 255, 255, 255
        fuente = pygame.font.Font(None, 30)
        precio = '$'+str(self.precio)
        size = fuente.size(precio)
        pesos = fuente.render(precio, 0, fg)
        screen.blit(pesos, (x, y-45))

        # Dibujar el humor
        bg = 255, 255, 255
        if self.humor == 'angry':
            fg = 255, 0, 0
        elif self.humor == 'moody':
            fg = 250, 200, 60
        else:
            fg = 0, 255, 0
        
        fuente = pygame.font.Font(None, 30)
        humor = str(self.humor)
        size = fuente.size(humor)
        fel = fuente.render(humor, 0, fg)
        screen.blit(fel, (x, y-25))

        # Dibujar el bar 
        screen.blit(self.image, (x, y))

    def ver(self):
        print "BAR"
        print "Precio: " + str(self.precio)
        print "Humor: " + self.humor
        print "Cambio de humor en: " + str(self.cambioHumor)
        print "Velocidad de humor: " + str(self.velocidadHumor)

    def mandarMatones(self):
        pass



def test():
    # Inicializamos la pantalla
#    import pdb; pdb.set_trace()
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption('BAR 0.1')
    clock = pygame.time.Clock()

    # rellenamos el fondo
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((250, 250, 250))

    # mostramos un texto
    font = pygame.font.Font(None, 36)
    text = font.render("BAR 0.1", 1, (10, 10, 10))
    textpos = text.get_rect()
    textpos.centerx = background.get_rect().centerx
    background.blit(text, textpos)

    # creando un par de bares 
    bar1 = Bar()
    bar1.draw(screen, 100, 100)
        
    # actualizamos(blit) todo en la pantalla
    screen.blit(background, (0, 0))
    pygame.display.flip()

    while 1:
        for event in pygame.event.get():
            if event.type == QUIT:
                return
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                return
            elif pygame.mouse.get_pressed()[0] == 1:
                bar1.ver()
            elif pygame.mouse.get_pressed()[2] == 1:
                # simular la llegada de una bola al bar
                bar1.alcohol = True
                bar1.ver()
            else:
                continue
                
        clock.tick(50)
        screen.blit(background, (0, 0))
        bar1.update()
        bar1.draw(screen, 100, 100)
        pygame.display.flip()


if __name__ == '__main__':
    test()
