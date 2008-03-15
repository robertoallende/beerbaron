import os, sys
from math import sqrt, cos, acos, degrees

import pygame
from pygame.locals import *
import maps
import bar

from data import load_image


#NOTAS:
#de la clase BOLA:
#self.final_bar (el id del bar final)...
#self.mapa.nodos_pos[self.final_bar] (la posicion de ese id_nodo, en este caso la pos del bar final)

#en el main()...
#el evento de mouse hit_or_not (en realidad metodo de bola), cuando se presiona en el primer nodo (nodo de salida)
#reliza la accion de "self.balls.append(1)", y cuando la bola llega a un bar este
#contador decrementa en uno (no implementado)
#tener en cuenta que la variable self.final_bar es el bar a donde "llego", como el movimiento no esta implementado
#y automaticamente realiza el camino y llega al bar se puede usar el evento de hit_or_not que incrementa self.balls.append(1)
#para usarlo como contador de que bola llega donde
#en definitiva seria mas que suficiente escuchar en "self.ball" cuando se modifica mirar sel.final_bar y sumarle una bola
#entregada a ese bar...

#ahora la variable "self.cantbolas" de la calse BOLA, mantiene una constancia de la cantidad de bolas
# que tiene el usuario para largar, no laragara una si no posee ninguna,en cualquier momento se peude modificar
# la cantidad con los cambiar el valor de self.cantbolas

class Ball:
    def __init__(self, sprite, xy_path, image):
        self.sprite = sprite
        xy_path.reverse()
        self.xy_path = xy_path
        self.image = image
        self.rect = self.image.get_rect()

    def update(self, screen):
        if len(self.xy_path) > 0:
            pos = self.xy_path.pop()
            self.sprite.update( pos  )
            screen.blit(self.image, self.sprite.position)
#        for i in self.xy_path:
#            self.bola_group.clear(screen,background)
#            self.bola_group.update(i)
#            self.bola_group.draw(self.surface)
            
        #  self.surface.blit(m.image,m.position)
#        self.bola_group.empty()
#        m.kill()


class Bola:
    def __init__(self, image, position, surface, cantbolas):
        self.image = image
        self.position = position
        self.surface = surface
        self.tick = 90
        self.balls = []
        self.cantbolas = cantbolas
        #self.pos = image.get_rect().move(0, height)

    def update(self, screen):
        """da toda la informacion, cant de bolas, pos de bolas, etc"""
        for b in self.balls:
            r = b.update(screen)

            if r == False:
                self.balls.remove(b)
 
    def graphMap(self, alto, ancho, xoff=30, yoff=50):
        """grafica un mapa establece el estado de swiches y los controla"""
        self.xoff = xoff
        self.yoff = yoff
        x_center = -20#para centrar el sprite
        y_center = -20#para centrar el sprite
        # cargamos el mapa
        self.mapa = maps.Map3() #conviene poner todos los mapar como metodos dentro de una clase asi se peuden buclear
        pos = self.mapa.nodos_pos

        self.objetos = []
        self.rect_list = []

        self.tubos = []
        self.tubos_rect = []
        
        for x in self.mapa.nodos:
            m = Spriteador((pos[x][0]+xoff+x_center,pos[x][1]+yoff+y_center), 'union1.png')#la giladas verdes :P
            (x1, y1) = m.position
            m.rect.center = (x1 - x_center, y1 - y_center)
            self.objetos.append(m)##object de cada sprite con sus atributos
            self.rect_list.append(pygame.Rect(m))#lista de rectangulos para que maneje pygame

        #idem que anterior para dibujar lineas solo que este completa con graficos de tuberias
        #por una question de que no queda bien usaremos la pos del siguiente nodo :(
        for x in self.mapa.nodos:
            if self.mapa.swicht_dict[x] == 2: #nodo de comienzo
                col = self.mapa.nodos_rdict[x][0]#colindante
                s = Spriteador((pos[x][0]+xoff-10,pos[col][1]+yoff), 'tubo1.png')#+xoff-10 +yoff-15
                (x1, y1) = m.position
                s.image = pygame.transform.scale(s.image, [20,abs(pos[x][1] - pos[col][1])])
                s.rect.center = (x1 - x_center, y1 - y_center)
                self.surface.blit(s.image, s.position)
                self.tubos.append(s)
                self.tubos_rect.append(pygame.Rect(s))
                
            elif self.mapa.swicht_dict[x] == 1:
                col = self.mapa.nodos_rdict[x]
                for i in range(len(col)): #lista de colindantes (el primero es el nodo anterior)
                    if i != 0:
                        #testeamos las posicion para ver donde posicionamos el nodo
                        if pos[x][0] < pos[col[i]][0]:
                            s = Spriteador((pos[x][0]+xoff-10,pos[col[i]][1]+yoff), 'tubo1.png')#+xoff-10 +yoff-15
                        else:
                            s = Spriteador((pos[col[i]][0]+xoff-10,pos[col[i]][1]+yoff), 'tubo1.png')#+xoff-10 +yoff-15
                        (x1, y1) = m.position
                        self.hip(pos[x][0],pos[x][1], pos[col[i]][0], pos[col[i]][1])
                        s.image = pygame.transform.scale(s.image, [20,int(round(self.hipo,0))])
                        s.image = pygame.transform.rotate(s.image, self.angulo)
                        s.rect.center = (x1 - x_center, y1 - y_center)

                        self.surface.blit(s.image, s.position)
                        self.tubos.append(s)
                        self.tubos_rect.append(pygame.Rect(s))

        self.searchPath()
        
        return self.objetos #los usaremos para acutalizarlos constantemente
    def hip(self, x1, y1, x2, y2):
            """calcula la hipotenusa y el angulo en grados(para sistema de pygame)"""
            self.hipo = sqrt(pow((x1-x2),2) + pow((y1 - y2),2))
            if x1 == x2: #angulo 0
                self.angulo = 0
            else:
                self.angulo = 90-degrees(acos((x1-x2)/self.hipo))
            
    def hit_or_not(self,mouse,screen,background,ciudad_fondo,sotano):
        """calcula si el mouse toca a alguno de los swiches"""
        #por ahora tira un error cuando uno clickea en el ultimo nodo (bar)... se soluciona con self.rect_list.pop(-1)
        #para que no escuche a ese nodo
        (x,y) = mouse
        cursor_box= pygame.Rect(x,y,2,2)#hacemos una caja alrededor del cursor para calcular colisiones
        i= cursor_box.collidelist(self.rect_list)
        id_nodo =self.mapa.nodos[i]
        
        if self.mapa.swicht_dict[id_nodo] ==1:
            #print "CAMBIA EL ESTADO DE", i
            self.state_change(id_nodo)
            self.state_change_view(id_nodo,i)
        if self.mapa.swicht_dict[id_nodo] ==2:
            if self.cantbolas != 0:
                print "se crea una bola"
                mibola = self.createBall(id_nodo,screen,background,ciudad_fondo,sotano)
                self.balls.append(mibola)
                self.cantbolas = self.cantbolas -1
                #self.noballs = 0
            else:
                print "NO HAY BOLAS"
                #self.noballs = 1

        if id_nodo == self.mapa.sotano:
            return True
        else:
            return False
            
        #print "NODO", self.mapa.nodos[i]
        
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
            
        self.searchPath()
        print self.mapa.estados_dict[id]
    def state_change_view(self,id=None,i=None):
        """cambia el estado visualmente"""
        def aux(id_node,indice):
            pos1 = self.mapa.nodos_pos[id_node]
            pos2 = self.mapa.nodos_pos[self.mapa.nodos_rdict[id_node][self.mapa.estados_dict[id_node][0]]]
            if pos2[0] > pos1[0]:#derecha
                s = Spriteador((pos[id_node][0]+self.xoff-15,pos[id_node][1]+self.yoff-15), 'flecha.png')
                s.image = pygame.transform.rotate(s.image, -90)
                s.rect = (pos[id_node][0]+self.xoff -20,pos[id_node][1]+self.yoff-20)
                self.surface.blit(self.objetos[indice].image, s.rect)
                self.surface.blit(s.image,s.position) 
            elif pos2[0] < pos1[0]:#izquerda
                s = Spriteador((pos[id_node][0]+self.xoff-15,pos[id_node][1]+self.yoff-15), 'flecha.png')
                s.image = pygame.transform.rotate(s.image, 90)
                s.rect = (pos[id_node][0]+self.xoff -20,pos[id_node][1]+self.yoff-20)
                self.surface.blit(self.objetos[indice].image, s.rect)
                self.surface.blit(s.image,s.position)
            
        pos = self.mapa.nodos_pos
        if id == None and i == None:#incializa los estado... o actualiza todos los estados
            for i, x in enumerate(self.mapa.nodos):
                if self.mapa.swicht_dict[x] == 1:
                    aux(x,i)
        else:
            aux(id,i)
            

    def createBall(self,nodo,screen,background,ciudad_fondo,sotano):
#        self.balls = []
        self.balls_rect = []
        
        pos = self.mapa.nodos_pos
        m = Spriteador((pos[nodo][0]+self.xoff+15,pos[nodo][1]+self.yoff+15), 'bola1.gif')
#        (x1, y1) = m.position
#        m.rect.center = (x1 - 15, y1 - 15)
#        self.balls = []
#        self.balls.append(m)##object de cada sprite con sus atributos
#        self.balls_rect.append(pygame.Rect(m))

        #self.surface.blit(self.balls[-1].image, m.position)
#        self.bola_group = pygame.sprite.RenderClear(m)
#        self.bola_group.draw(self.surface)

        #simulamos el recorrido poniendo la bola en el lugar donde terminaria
        #primero borramos los nodos de los baares
#        self.update_bar_view(3)
        #ahora si :P
        pos = self.mapa.nodos_pos[self.final_bar]
        
#        for i in self.path_nodes:
#            print self.mapa.nodos_pos[i]
       
#        position = (pos[0]+self.xoff, pos[1]+self.yoff)
#        print 'position: ' + str( position )
        mibola =  Ball(m, self.createPath(), self.image)

        return mibola
 
    def searchPath(self):
        """crea un array o un diccionario con los datos de el camino"""
        next_node= ""
        aux = []
        nodos = []
        actual_node = self.mapa.nodos[0]
        while next_node != "final":
            a = self.mapa.estados_dict[actual_node][0]
            #a = self.mapa.swicht_dict[x] #estados de los swiches
            if a != "final":
                next_node = self.mapa.nodos_rdict[actual_node][a] #nodos con el que colida
                nodos.append(actual_node)
                aux.append(next_node)
                actual_node = next_node
            else:
                bar = actual_node
                aux.append("final")
                next_node = "final"
                
        self.final_bar = bar #el bar donde caera la bola con la configuracion esta de path
        self.path_nodes = nodos # los id_nodes que conforman el path
        self.path_nodes_r= aux # la relacion de los id_nodes anteriores
        self.path_dict = dict(zip(nodos, aux))#un diccionario de las cosas anteriores :P

    def createPath(self):
        # coordenadas del camino
        #for i in self.path_nodes:       
        xy_path = []

        x = self.mapa.nodos_pos[self.path_nodes[0]][0]+self.xoff - 10
        y = self.mapa.nodos_pos[self.path_nodes[0]][1]+self.yoff 
        xy_path.append( (x,y) )
        xbefore = x
        ybefore = y
      
        recorrido = self.path_nodes
        recorrido.append(self.final_bar)

        for i in  range(len(recorrido)):       
            if i > 0:
                x = self.mapa.nodos_pos[self.path_nodes[i]][0]+self.xoff - 10 
                y = self.mapa.nodos_pos[self.path_nodes[i]][1]+self.yoff 

                N = 20
                mod_x = x - xbefore 
                mod_y = y - ybefore  
      
                c = range(N) 
                c.reverse()
                for j in c:
                    if j/float(N) < 1:
                        w = x - ( mod_x *  j/float(N) ) + self.xoff # xoff = 0 
                        z = y - ( mod_y *  j/float(N) ) # yoff = 150
                        xy_path.append( (w,z) )

                xy_path.append( (x,y) )
                xbefore = x
                ybefore = y

        pos = self.mapa.nodos_pos[self.final_bar]
        xy_path.append( (pos[0]+self.xoff, pos[1]+self.yoff))

        return xy_path


#        self.xy_path.append((pos[0]+self.xoff, pos[1]+self.yoff))

    def update_bar_view(self, tipo=None, node=None ):
        """borra cualquier cosa dibujada sobre el nodo del bar"""

        if tipo != None:
            for i, x in enumerate(self.mapa.nodos):
                if self.mapa.swicht_dict[x] == tipo: #ultimo nodos (bares)
                    self.surface.blit(self.objetos[i].image, self.objetos[i].rect)
        elif node != None:
            for i,x in enumerate(self.mapa.nodos):
                if x == node:
                    self.surface.blit(self.objetos[i].image, self.objetos[i].rect)
        else:
            print "NO SE ESPECIFICO ARGUMENTO"
                  

class Spriteador(pygame.sprite.Sprite):
    def __init__(self, position, name):
        """inicializa una imagen como sprite"""
        pygame.sprite.Sprite.__init__(self) #call Sprite initializer
        self.image, self.rect = load_image(name)
        self.position = position
        self.rect = self.image.get_rect()
        self.rect.center = self.position
        
    def update(self, pos):
        x,y =self.position
        #aca en este espacio deben ir las modificaciones de x e y
        (x,y) = pos
        #-------------
        self.position = (x,y)
        self.image = self.image
        self.rect = self.image.get_rect()
        self.rect.center = self.position

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
