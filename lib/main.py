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
from escenario import *
from bar import Bar

def game():
	# Inicializamos la pantalla
	pygame.init()
	screen = pygame.display.set_mode((800, 600))
	pygame.display.set_caption('BaronBeer v0.01')
	clock = pygame.time.Clock()

	# rellenamos el fondo
	background = pygame.Surface(screen.get_size())
	organic = Spriteador((0,0),'organic.jpg')
	background = background.convert()
	background.fill((163, 108, 54))

	# mostramos un texto
	#font = pygame.font.Font(None, 36)
	#text = font.render("TUBERIA 0.1", 1, (10, 10, 10))
	#textpos = text.get_rect()
	#textpos.centerx = background.get_rect().centerx
	#background.blit(text, textpos)

	spriter = Spriteador((0,0),'bola1.gif')
	ciudad_fondo, ciudad_fondo_rect = load_image('ciudad_fondo.jpg')
	#generamos los Mapas
	bolas = Bola(spriter.image, spriter.position, background,1000)
	m = bolas.graphMap(500,100, 0, 150)
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

	# El Sotano
	sotano = Escenario(100, 1000)
	sotano.draw(screen, 300, 400)

	
	# actualizamos(blit) todo en la pantalla
	screen.blit(background, (0, 0))
	pygame.display.flip()

	# Event loop
	release1 = 1
	release2 = 2
	while not sotano.terminar():
            tictoc = clock.tick(60)
            for event in pygame.event.get():
                if event.type == QUIT:
                    return
                if pygame.mouse.get_pressed()[0] == 1 and release1 == 1:# event.type == MOUSEBUTTONDOWN[1]:
                    print "BOTON 1 MOUSE"
                    mouse_pos =  pygame.mouse.get_pos()
                    estado = bolas.hit_or_not(mouse_pos,screen,background,ciudad_fondo,sotano)
                    #print estado
                    release1 = 0

#                    if estado:
                        # Actualizar bares
#                        bares[bolas.final_bar].alcohol = True
#                        sotano.cobrar(bares[bolas.final_bar].precio)
                
                if pygame.mouse.get_pressed()[0] == 0 :
                    release1 = 1
                if pygame.mouse.get_pressed()[2] == 1 and release2 == 1:
                    print "BOTON 2 MOUSE"
                    release2 = 0
                if pygame.mouse.get_pressed()[2] == 0:
                    release2 = 1
            screen.blit(background, (0, 0))
            screen.blit(ciudad_fondo,(0,0))
            sotano.draw(screen, 0, 360)
            j = 1


            for i in bolas.mapa.ids_bares: 
                bares[i].update()
                if bares[i].cambioHumor == 1 and bares[i].humor == 'angry':
                    sotano.golpizaMaton()
                bares[i].draw(screen, 70 * (2*j) - 70, 64)
                j = j + 1

            sotano.update()
            bolas.update(screen)

            pygame.display.update()
