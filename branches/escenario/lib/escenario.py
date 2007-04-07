import os, sys
import pygame
from bar import Bar
from tuberia import *
from pygame.locals import *
from data import load_image

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
	# Inicializamos la pantalla
	pygame.init()
	screen = pygame.display.set_mode((800, 600))
	pygame.display.set_caption('BaronBeer v0.01')
	clock = pygame.time.Clock()

	# rellenamos el fondo
	background = pygame.Surface(screen.get_size())
	background = background.convert()
	background.fill((163, 108, 54))

	# mostramos un texto
	font = pygame.font.Font(None, 36)
	text = font.render("TUBERIA 0.1", 1, (10, 10, 10))
	textpos = text.get_rect()
	textpos.centerx = background.get_rect().centerx
	background.blit(text, textpos)

	spriter = Spriteador((0,0),'bola1.gif')
	
	#generamos los Mapas
	bolas = Bola(spriter.image, spriter.position, background,1000)
	m = bolas.graphMap(400,300)
	for t in m:
            background.blit(t.image, t.position)
        bolas.state_change_view()
        #fin generar Mapas

        # Los bares
        bares = {}
        for i in range(5):
            key = 'nodo'+str(6+i)
            bares[key] = bar.Bar()
            bares[key].draw(screen, 500, 100*i)
	
	# actualizamos(blit) todo en la pantalla
	screen.blit(background, (0, 0))
	pygame.display.flip()

	# Event loop
	release1 = 1
	release2 = 2
	while 1:
            tictoc = clock.tick(60)
            for event in pygame.event.get():
                if event.type == QUIT:
                    return
                if pygame.mouse.get_pressed()[0] == 1 and release1 == 1:# event.type == MOUSEBUTTONDOWN[1]:
                    print "BOTON 1 MOUSE"
                    mouse_pos =  pygame.mouse.get_pos()
                    estado = bolas.hit_or_not(mouse_pos)
                    #print estado
                    release1 = 0

                    if estado:
                        # Actualizar bares
                        for i in bares.keys():
                            bares[bolas.final_bar].alcohol = True
                
                if pygame.mouse.get_pressed()[0] == 0 :
                    release1 = 1
                if pygame.mouse.get_pressed()[2] == 1 and release2 == 1:
                    print "BOTON 2 MOUSE"
                    release2 = 0
                if pygame.mouse.get_pressed()[2] == 0:
                    release2 = 1
                screen.blit(background, (0, 0))

            j = 1
            for i in bares.keys(): 
                bares[i].update()
                bares[i].draw(screen, 500, 100*j)
                j = j + 1

            pygame.display.flip()



if __name__ == '__main__': main()
