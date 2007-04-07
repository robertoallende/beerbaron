import os, sys
import pygame
from pygame.locals import *

def load_image(name):
    """funcion general para cargar imagenes de forma facil"""
    fullname = os.path.join('data', name)
    image = pygame.image.load(fullname)
    image = image.convert_alpha()
    return image, image.get_rect()

class Bar:
    def __init__(self, precio, humor, velocidadHumor):
        self.image, self.rect = load_image('bar.png')
#        import pdb; pdb.set_trace()
        self.precio = precio
        self.humor = humor
        self.velocidadHumor = velocidadHumor
        self.cambioHumor = self.velocidadHumor
        self.alcohol = False

    def update(self):
        if self.alcohol:
            self.humor = 'contento'
            self.cambioHumor = self.velocidadHumor
        else:
            self.cambioHumor = self.cambioHumor - 1
            if self.cambioHumor == 0:
                if self.humor == 'enojado':
                    self.mandarMatones()
                elif self.humor == 'maso':
                    self.humor = 'enojado'
                elif self.humor == 'contento':
                    self.humor = 'maso'

                self.cambioHumor = self.velocidadHumor

    def draw(self, screen):
        screen.blit(self.image, (100, 100))

    def mandarMatones(self):
        pass


def main():
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
    bar1 = Bar(1000, 'maso', 500)
    bar1.draw(screen)
        
    # actualizamos(blit) todo en la pantalla
    screen.blit(background, (0, 0))
    pygame.display.flip()

    while 1:
        for event in pygame.event.get():
            if event.type == QUIT:
                return
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                return
            else:
                continue
                
        clock.tick(50)
        screen.blit(background, (0, 0))
        bar1.update()
        bar1.draw(screen)
        pygame.display.flip()


if __name__ == '__main__':
    main()
