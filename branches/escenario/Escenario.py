import os, sys
import pygame
from bar import Bar
from tuberia import *
from pygame.locals import *

if not pygame.font: print 'Warning, fonts disabled'
if not pygame.mixer: print 'Warning, sound disabled' 

def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error, message:
        print 'Cannot load image:', name
        raise SystemExit, message
    image = image.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image, image.get_rect()

def load_sound(name):
    class NoneSound:
        def play(self): pass
    if not pygame.mixer:
        return NoneSound()
    fullname = os.path.join('data', name)
    try:
        sound = pygame.mixer.Sound(fullname)
    except pygame.error, message:
        print 'Cannot load sound:', wav
        raise SystemExit, message
    return sound

class Escenario:
    def __init__(self, cantBares, background, screen, precioSoborno, dineroAcumulado):
        """genera un escenario para el juego y llama al resto de las clases"""

	#suma de todo el dinero que se gano a lo largo del juego
	self.dineroAcumulado = dineroAcumulado
	self.dineroActual = 0
	self.precioSoborno = precioSoborno
	self.cantGolpizas = 0
	
	#cantidad de turnos para que se cobre el soborno
	self.velocidadSoborno = 20
	
	#turnos que faltan para que el soborno se actualice
	self.turnosSoborno = 20
	self.image, self.rect = load_image('Sotano.jpg')
	
	# Creacion de las clases
	self.bares = [0] * cantBares
	for i in range(cantBares):
		self.bares[i] = Bar(1000, 'maso', 500)
		self.bares[i].draw(screen)

	spriter = Spriteador((100,100))
	self.tuberia = Bola(spriter.image, spriter.position, background)

    def update(self):
        """genera y envia los tics del juego"""
	#self.tuberia.update()
	for bar in self.bares:
		bar.update()

	if self.turnosSoborno == 0:
		self.pagarSoborno()
		self.turnosSoborno = self.velocidadSoborno
	else:
		self.turnosSoborno = self.turnosSoborno - 1

    def pagarSoborno(self):
	""" """
	p = Policia()
	p.cobrarSoborno()
	self.dineroActual = self.dineroActual - self.precioSoborno
	if self.dineroActual < 0:
		self.golpizaPolicial()

    def cobrar(self, precioCerveza):
	""" resultado de la llegada de una bola a un bar """
	self.dineroActual = self.dineroActual + self.precioCerveza
    
    def golpizaMaton(self):
        """genera """
	m = Maton()
	m.golpiza()
	self.cantGolpizas = self.cantGolpizas + 1
	# es golpiza fatal
	if self.cantGolpizas == 3:
		self.terminar()
		    
#    def golpizaMatonFatal(self):
#        """genera """
#	m = Maton()
#	m.golpiza()
#	self.terminar()
			    
    def golpizaPolicial(self):
        """genera """
	p = Policia()
	p.golpiza()
	self.terminar()
        pass

    def terminar(self):
	""" termina """
	# Mensaje de fin
	# Actualizar record
	pass

    def draw(self, screen):
        screen.blit(self.image, (200, 300))


class Maton:
    def __init__(self):
	""" genera un maton """
	pass

    def golpiza(self):
	""" da la gopliza """
	pass

class Policia:
    def __init__(self):
	""" genera un maton """
	pass

    def golpiza(self):
	""" da la gopliza """
	pass

    def cobrarSoborno(self):
	""" """
	pass

def main():
	# Initialise screen
	pygame.init()
	screen = pygame.display.set_mode((800, 600))
	pygame.display.set_caption('Escenario 1')
	clock = pygame.time.Clock()

	# Fill background
	background = pygame.Surface(screen.get_size())
	background = background.convert()
	background.fill((250, 250, 250))

	# Display some text
	font = pygame.font.Font(None, 36)

	e = Escenario(3, background, screen, 3, 0)
	e.draw(screen)
	text = font.render("Bares "+str(len(e.bares))+" Tuberia ", 1, (0, 0, 0))

	textpos = text.get_rect()
	textpos.centerx = background.get_rect().centerx
	background.blit(text, textpos)

	# Blit everything to the screen
	screen.blit(background, (0, 0))
	pygame.display.flip()
	
	# Event loop
	while 1:
		clock.tick(60)
		for event in pygame.event.get():
			if event.type == QUIT:
				return
			elif event.type == KEYDOWN and event.key == K_ESCAPE:
 		 	        return
		        else:
                		continue
		e.update()
		#screen.blit(background, (0, 0))
		e.draw(screen)
		pygame.display.flip()


if __name__ == '__main__':
	main()
