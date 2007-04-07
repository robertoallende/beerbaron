import os, sys

import pygame
from pygame.locals import *
import maps

        

class Bola:
    def __init__(self, image, position, surface):
        self.image = image
        self.position = position
        self.surface = surface
        #self.pos = image.get_rect().move(0, height)
    def graphMap(self, alto, ancho, xoff=30, yoff=50):
        """grafica un mapa establece el estado de swiches y los controla"""
        x_center = -15#para centrar el sprite
        y_center = -15#para centrar el sprite
        # cargamos el mapa
        self.mapa = maps.Map3() #conviene poner todos los mapar como metodos dentro de una clase asi se peuden buclear
        pos = self.mapa.nodos_pos

        self.objetos = []
        self.rect_list = []
        
        for x in self.mapa.nodos:
            m = Spriteador((pos[x][0]+xoff+x_center,pos[x][1]+yoff+y_center))
            (x1, y1) = m.position
            m.rect.center = (x1 - x_center, y1 - y_center)
            self.objetos.append(m)##object de cada sprite con sus atributos
            self.rect_list.append(pygame.Rect(m))#lista de rectangulos para que maneje pygame
        #dibujamos lineas de nodo a nodo

        for x in self.mapa.nodos:
            if self.mapa.swicht_dict[x] == 2: #nodo de comienzo
                col = self.mapa.nodos_rdict[x][0]
                pygame.draw.line(self.surface, (0,0,0), (pos[x][0]+xoff, pos[x][1]+yoff),
                                 (pos[col][0]+xoff,pos[col][1]+yoff),1)
            elif self.mapa.swicht_dict[x] == 1:
                col = self.mapa.nodos_rdict[x]
                for i in range(len(col)): #lista de colindantes (el primero es el nodo anterior)
                    if i != 0:
                        pygame.draw.line(self.surface, (0,0,0), (pos[x][0]+xoff,pos[x][1]+yoff),
                                         ( pos[col[i]][0]+xoff,pos[col[i]][1] +yoff),1)

        return self.objetos #los usaremos para acutalizarlos constantemente
    def hit_or_not(self,mouse):
        """calcula si el mouse toca a alguno de los swiches"""
        #por ahora tira un error cuando uno clickea en el ultimo nodo (bar)... se soluciona con self.rect_list.pop(-1)
        #para que no escuche a ese nodo
        (x,y) = mouse
        cursor_box= pygame.Rect(x,y,2,2)#hacemos una caja alrededor del cursor para calcular colisiones
        i= cursor_box.collidelist(self.rect_list)
        id_nodo =self.mapa.nodos[i]
        if self.mapa.swicht_dict[id_nodo] ==1:
            print "CAMBIA EL ESTADO DE", i
            self.state_change(id_nodo)
        print "NODO", self.mapa.nodos[i]
        
    def state_change(self, id):
        """maneja los cambies de estado de los swiches,
        modificca la state_list, con la nueva configuracion, funciona para una cantidad ilimitada de aristas"""
        a = (len(self.mapa.nodos_rdict[id])-1) #cantidad de elementos colindantes (menos los anteriores)
        #puede caminar sobre los colindantes menos el 0 y el ultimo+1
        ea = self.mapa.estados_dict[id][0] #estado actual
        if ea == a: #si el est acutal seniala al ultimo nodo
            self.mapa.estados_dict[id] = [1]
        else:
            self.mapa.estados_dict[id] = [self.mapa.estados_dict[id][0]+1]
        print self.mapa.estados_dict[id]

class Spriteador(pygame.sprite.Sprite):
    def __init__(self, position):
        """inicializa una imagen como sprite"""
        pygame.sprite.Sprite.__init__(self) #call Sprite initializer
        self.image, self.rect = load_image('swicht.png')
        self.position = position
        self.rect = self.image.get_rect()
        #self.rect.center = self.position


def main():
	# Inicializamos la pantalla
	pygame.init()
	screen = pygame.display.set_mode((800, 600))
	pygame.display.set_caption('TUBERIA 0.1')

	# rellenamos el fondo
	background = pygame.Surface(screen.get_size())
	background = background.convert()
	background.fill((250, 250, 250))

	# mostramos un texto
	font = pygame.font.Font(None, 36)
	text = font.render("TUBERIA 0.1", 1, (10, 10, 10))
	textpos = text.get_rect()
	textpos.centerx = background.get_rect().centerx
	background.blit(text, textpos)

	spriter = Spriteador((100,100))
	
	#generamos los Mapas
	bolas = Bola(spriter.image, spriter.position, background)
	m = bolas.graphMap(400,300)
	for t in m:
            background.blit(t.image, t.position)
        #fin generar Mapas

	
	# actualizamos(blit) todo en la pantalla
	screen.blit(background, (0, 0))
	pygame.display.flip()

	# Event loop
	release1 = 1
	release2 = 2
	while 1:
		for event in pygame.event.get():
			if event.type == QUIT:
				return
                if pygame.mouse.get_pressed()[0] == 1 and release1 == 1:# event.type == MOUSEBUTTONDOWN[1]:
                    print "BOTON 1 MOUSE"
                    mouse_pos =  pygame.mouse.get_pos()
                    estado = bolas.hit_or_not(mouse_pos)
                    #print estado
                    release1 = 0
                if pygame.mouse.get_pressed()[0] == 0 :
                    release1 = 1
                if pygame.mouse.get_pressed()[2] == 1 and release2 == 1:
                    print "BOTON 2 MOUSE"
                    release2 = 0
                if pygame.mouse.get_pressed()[2] == 0:
                    release2 = 1
		screen.blit(background, (0, 0))
		pygame.display.flip()


def load_image(name):
    """funcion general para cargar imagenes de forma facil"""
    fullname = os.path.join('imagenes', name)
    image = pygame.image.load(fullname)
    image = image.convert_alpha()
    return image, image.get_rect()
	

if __name__ == '__main__': main()
