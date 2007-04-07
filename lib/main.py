'''Game main module.

Contains the entry point used by the run_game.py script.

Feel free to put all your game code here, or in other modules in this "lib"
directory.
'''
import os, sys
from math import sqrt, cos, acos, degrees

import pygame
from pygame.locals import *


from data import load_image
from tuberia import *
from bar import Bar

def main():
	# Inicializamos la pantalla
	pygame.init()
	screen = pygame.display.set_mode((800, 600))
	pygame.display.set_caption('TUBERIA 0.1')
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

	spriter = Spriteador((100,100),'bola11.png')
	
	#generamos los Mapas
	bolas = Bola(spriter.image, spriter.position, background,1000)
	m = bolas.graphMap(400,300)
	for t in m:
            background.blit(t.image, t.position)
        bolas.state_change_view()
        #fin generar Mapas

        # Los bares
        bares = {}
        i = 1
        for key in bolas.mapa.ids_bares:
            bares[key] = Bar()
            bares[key].draw(screen, 500, 100*i)
            i = i + 1
	
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
