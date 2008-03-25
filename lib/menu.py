background_image_filename = 'data/images/background-800x600.png'
icon_image_filename       = 'data/images/choop.png'
icon_hover_image_filename = 'data/images/choop-hover.png'
font_filename             = 'data/fonts/Simpsonfont.ttf'

import pygame
from pygame.locals import *
from sys import exit


#SCREEN_SIZE = ( 640, 480 )
SCREEN_SIZE  = ( 800, 600 )
#SCREEN_SIZE  = ( 1024, 768 )

pygame.init()

screen           = pygame.display.set_mode( SCREEN_SIZE, 0, 32)
background       = pygame.image.load( background_image_filename ).convert()
icon             = pygame.image.load( icon_image_filename ).convert_alpha()
icon_hover       = pygame.image.load( icon_hover_image_filename ).convert_alpha()
font             = pygame.font.Font( font_filename, 32 )
#font             = pygame.font.SysFont( "Verdana", 34 )
fontColor        = ( 255, 0, 0 )
backgroundColor  = ( 160, 200, 255 )
#menuPosition    = ( 140, 160 ) # 640x480
menuPosition    = ( 200, 180 ) # 800x600
#menuPosition     = ( 200, 280 ) # 1024x768

Fullscreen       = False
menuItemSelected = 0
showMenu         = True


key  = { "fullscreen":K_f, "quit":K_q, "left":K_LEFT, "right":K_RIGHT, "up":K_UP, "down":K_DOWN, "fire":K_SPACE, "select":K_RETURN }
#menu = ["New Game!", "Help", "Score", "Configurations", "Quit"]
menu = [ { "title": "New Game!", "action":"pay_game", "area":0 }, \
#        { "title": "Help", "action":"show_help", "area":0 }, \
#        { "title": "Score", "action":"show_score", "area":0 }, \
#        { "title": "Configurations", "action":"configuration", "area":0 }, \
        { "title": "Quit", "action":"quit and bye bye!", "area":0 } \
       ]



while True:

    event = pygame.event.wait()

    if event.type == QUIT or ( event.type == KEYDOWN and ( event.key == K_ESCAPE or event.key == key['quit'] ) ) :
        exit()

    if event.type == KEYDOWN:

        if event.key == key['fullscreen'] :
            Fullscreen = not Fullscreen
            if Fullscreen:
                screen = pygame.display.set_mode(SCREEN_SIZE, FULLSCREEN, 32)
            else:
                screen = pygame.display.set_mode(SCREEN_SIZE, 0, 32)

        elif event.key == key['up']:
            if menuItemSelected > 0 :
                menuItemSelected -= 1

        elif event.key == key['down']:
            if menuItemSelected < len(menu) - 1 :
                menuItemSelected += 1

        elif event.key in [ key['fire'], key['select'] ] :
            # ejecuta la accion

            print "Action: %i" % menuItemSelected
            print menu[menuItemSelected]['action']

            if   menuItemSelected == 0 :
                pass
            elif menuItemSelected == 1 :
                exit()

        #elif event.mouse

    if showMenu :

        screen.blit(background, (0, 0))
        x, y     = menuPosition
        menuItem = 0

        for item in menu:

            # calcular el area donde esta ubicado el texto en la pantalla
            # y asignarlo al item del menu, para luego poder calcular la 
            # posicion del mouse y saber si esta presionando sobre un item.
            # menu[menuItem]['area'] = 0

            y += icon.get_height()
            if menuItem != menuItemSelected :
                text = font.render( item['title'], True, fontColor, backgroundColor )
                screen.blit( icon, ( x, y ))
                screen.blit( text, ( x + icon.get_width() + 10, y + ( icon.get_height() - text.get_height() ) / 2 ))
            else :
                font.set_bold(True)
                text = font.render( item['title'], True, fontColor, backgroundColor )
                font.set_bold(False)
                screen.blit( icon_hover, ( x, y ))
                screen.blit( text, ( x + icon_hover.get_width() + 10, y + ( icon.get_height() - text.get_height() ) / 2 ))

            y += 10
            menuItem += 1


        pygame.display.update()
