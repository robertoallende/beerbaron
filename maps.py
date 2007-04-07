from grafoGen import grafo

"""metodo para la construccion de niveles:
definimos los nodos numerados y con el nombre generico de "nodo" ej: nodo1, nodo2 , ect.
el numero corresponde a la ubicacion nodo1 es el primer nodo nodo2 es el segundo, etc ordenados asi:
    6   5   4
     \   \ /
      \   3
       \ / 
        2
        |
        1

el segundo parametro cuando definimos un nodo es el nivel, este esta dado de la siguiente manera:
en el ej anterior 1 nivel -> 0, 2 nivel -> 1, 3 nivel -> 2, 4,5,6 nivel ->3

el tercer y cuarto parametro son la posicion en el mundo, y la variable esc es por si queremos agrandarlo
recomiendo que en la creacion, se utlize la medida 400 x 400 como referencia y que siempre se posicionen centrados
ej: (nodo de arriba) tiene 3 nodos en un nivel por lo tanto le sumamos 1 y dividimos en ancho este numero
400/ 4 = 100
ahora ubicamos el primer nodo (6) en la pos 100 el segundo (5) en la pos 200 y el tercero(4) en la 300, de
esta forma quedara centrado
ahora el nodo 3 esta entre el 5 y el 4 por lo tanto su posicion sera 250 y asi con todos los demas :P

para las "y" (recordar que se cuentan de arriba para abajo(el 0 esta arriba)) simplemente dividiremos la pantalla
en la cantidad de niveles que tengamos - 1

las aristas son la relacion de que nodo con cual, se peuden repetir relaciones ya que el algoritmo de grafoGen
saca las redundancias, lo hice por comodidad pero no funcionaria en el caso que querramos dar orden a los nodos
la unica direccion permitida es arriba :(
despue debemos declara un par de variables, y cosas asi..
y usar swicht:
swicht, guarda la informacion de que si un nodo es un swicht, un nodo de llegada o un nodo de entrada
swicht = 1, entrada = 2, salida = 3
simplemente debemos especificar como se comportara cada nodo"""
                

class Map1:
    def __init__(self, esc = 1):
        """inicializa un mapa, esc es una variable que escala el tamanioo que
        asignemos a los nodos"""
        g = grafo()
        #definimos los nodos
        g.nodo("nodo1",0, 200*esc,  399*esc)
        g.nodo("nodo2",1, 200*esc,  266*esc)
        g.nodo("nodo3",2, 250*esc,  133*esc)
        g.nodo("nodo4",3, 300*esc,   1*esc)
        g.nodo("nodo5",3, 200*esc,  1*esc)
        g.nodo("nodo6",3, 100*esc,  1*esc)
        #aristas
        g.arista("nodo1", "nodo2")
        g.arista("nodo2", "nodo3")
        g.arista("nodo2", "nodo6")
        g.arista("nodo3", "nodo4")
        g.arista("nodo3", "nodo5")
        g.packing()
        g.genPosMANUAL()
        self.nodos = g.nodos
        self.nodos_rdict = g.pack_dict #relacion de los nodos en diccionaro
        self.nodos_rlista = g.pack_array #idem anterior pero en lista
        self.nodos_nivel_dict = g.nodo_nivel_dict #nivel de cada nodo
        self.nodos_pos = g.pos_dict #pos de cada nodo
        #definimos quenodo y cual no es swictch
        g.swicht("nodo1",2)
        g.swicht("nodo2",1)
        g.swicht("nodo3",1)
        g.swicht("nodo4",3)
        g.swicht("nodo5",3)
        g.swicht("nodo6",3)
        self.swicht_dict = g.swicht_dict
        #definimos estados de los swiches random, y un diccionario de estados
        g.estados()
        self.estados_dict = g.estado_dict

class Map2:
    def __init__(self, esc = 1):
        """inicializa un mapa, esc es una variable que escala el tamanioo que
        asignemos a los nodos"""
        g = grafo()
        #definimos los nodos
        g.nodo("nodo1",0, 200*esc,  400*esc)
        g.nodo("nodo2",1, 200*esc,  301*esc)
        g.nodo("nodo3",2, 240*esc,  201*esc)
        g.nodo("nodo4",3, 200*esc,   101*esc)
        g.nodo("nodo5",4, 320*esc,  1*esc)
        g.nodo("nodo6",4, 240*esc,  1*esc)
        g.nodo("nodo7",4, 160*esc,  1*esc)
        g.nodo("nodo8",4, 80*esc,  1*esc)
        #aristas
        g.arista("nodo1", "nodo2")
        g.arista("nodo2", "nodo3")
        g.arista("nodo2", "nodo8")
        g.arista("nodo3", "nodo4")
        g.arista("nodo3", "nodo5")
        g.arista("nodo4", "nodo6")
        g.arista("nodo4", "nodo7")
        g.packing()
        g.genPosMANUAL()
        self.nodos = g.nodos
        self.nodos_rdict = g.pack_dict #relacion de los nodos en diccionaro
        self.nodos_rlista = g.pack_array #idem anterior pero en lista
        self.nodos_nivel_dict = g.nodo_nivel_dict #nivel de cada nodo
        self.nodos_pos = g.pos_dict #pos de cada nodo
        #definimos quenodo y cual no es swictch
        g.swicht("nodo1",2)
        g.swicht("nodo2",1)
        g.swicht("nodo3",1)
        g.swicht("nodo4",1)
        g.swicht("nodo5",3)
        g.swicht("nodo6",3)
        g.swicht("nodo7",3)
        g.swicht("nodo8",3)
        self.swicht_dict = g.swicht_dict
        #definimos estados de los swiches random, y un diccionario de estados
        g.estados()
        self.estados_dict = g.estado_dict


class Map3:
    def __init__(self, esc = 1):
        """inicializa un mapa, esc es una variable que escala el tamanioo que
        asignemos a los nodos"""
        g = grafo()
        #definimos los nodos
        g.nodo("nodo1",0, 198*esc,  400*esc)
        g.nodo("nodo2",1, 198*esc,  301*esc)
        g.nodo("nodo3",2, 165*esc,  201*esc)
        g.nodo("nodo4",3, 231*esc,   101*esc)
        g.nodo("nodo5",4, 99*esc,  101*esc)
        g.nodo("nodo6",4, 330*esc,  1*esc)
        g.nodo("nodo7",4, 264*esc,  1*esc)
        g.nodo("nodo8",4, 198*esc,  1*esc)
        g.nodo("nodo9",4, 132*esc,  1*esc)
        g.nodo("nodo10",4, 66*esc,  1*esc)
        #aristas
        g.arista("nodo1", "nodo2")
        g.arista("nodo2", "nodo3")
        g.arista("nodo2", "nodo6")
        g.arista("nodo3", "nodo4")
        g.arista("nodo3", "nodo5")
        g.arista("nodo4", "nodo7")
        g.arista("nodo4", "nodo8")
        g.arista("nodo5", "nodo9")
        g.arista("nodo5", "nodo10")
        g.packing()
        g.genPosMANUAL()
        self.nodos = g.nodos
        self.nodos_rdict = g.pack_dict #relacion de los nodos en diccionaro
        self.nodos_rlista = g.pack_array #idem anterior pero en lista
        self.nodos_nivel_dict = g.nodo_nivel_dict #nivel de cada nodo
        self.nodos_pos = g.pos_dict #pos de cada nodo
        #definimos quenodo y cual no es swictch
        g.swicht("nodo1",2)
        g.swicht("nodo2",1)
        g.swicht("nodo3",1)
        g.swicht("nodo4",1)
        g.swicht("nodo5",1)
        g.swicht("nodo6",3)
        g.swicht("nodo7",3)
        g.swicht("nodo8",3)
        g.swicht("nodo9",3)
        g.swicht("nodo10",3)
        self.swicht_dict = g.swicht_dict
        #definimos estados de los swiches random, y un diccionario de estados
        g.estados()
        self.estados_dict = g.estado_dict



