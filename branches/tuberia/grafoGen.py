from random import randint

class grafo:
    def __init__(self):
        self.nodos = []
        self.aristas = []
        self.niveles = []
        self.nodos_pos = []
        self.entro = 0

    def nodo(self, nod, nivel=None, xpos=None,ypos=None):
        """nod = id nodo, crea un nodo sin link a ninguna arista
        debe ser un string
        nivel = nivel al cual pertenece el nodo, no se deben armar estructuras irreales (cuenta desde 0)
        xpos, ypos = pos x,y del nodo y tiene el 0 arriba y x a la izquierda nuestra
        se debe epecificar ambos valores"""
        if nivel != None:
            self.niveles.append(nivel)
        else:
            print "ERROR: no se especifico el nivel del nodo"

        if xpos != None:
            self.entro = 1
            if ypos != None:
                self.nodos_pos.append([xpos, ypos])
            else:
                print "ERROR: no se especifico un valor para y"
        else:
            if self.entro == 1:
                print "ERROR: se espesifico una posicion para alguno de los nodos ahora se debe hacer para todos"
        self.nodos.append(nod)

    def arista(self, nodo1, nodo2):
        """une por una arista dos nodos, nodo1 y nodo2 deben ser id's validos de nodos
        y se deben definir antes que con el metodo 'nodo(id)'"""
        self.aristas.append([nodo1,nodo2])

    def packing(self):
        """una vez terminada el setup de nodos y aristas, este metodo empaca todo en un diccionario"""
        #extraemos los nodos redundantes
        for x in self.aristas:
            x.sort()
            cont = self.aristas.count(x)
            if cont >= 2:
                self.aristas.remove(x)
                
        #creamos una lista de colindantes para cada nodo
        self.aristas2 = []
        for j,x in enumerate(self.nodos):
            self.aristas2.append([])
            for i in self.aristas:
                c = i.count(x)#cantidad de veces que se encuentra el nodo entre las aristas
                if c == 1:#si se encuentra buscamos el nodo que lo acompania
                    if i.index(x) == 0:
                        self.aristas2[j].append(i[1])
                    else:
                        self.aristas2[j].append(i[0])
                    
        
        self.pack_dict = dict(zip(self.nodos, self.aristas2))
        self.pack_array = self.aristas2

        #vemos cada nodo y su nivel (si se especifico... sino no se hace nada)
        self.nodo_nivel = []
        if self.niveles != []:
            for i,x in enumerate(self.niveles):
                self.nodo_nivel.append([self.nodos[i],x])
            self.nodo_nivel_dict = dict(zip(self.nodos, self.niveles))#diccionario de los niveles del nodo
            
    def genPos(self, alto, ancho):
        #NO USAR ESTE METODO ESTA INCOMPLETO
        lvl = max(self.niveles)
        y_plus = round((alto / lvl),0)
        #generamos la ubicacion segun la cantidad de nodos de cada nivel
        aux = []#cada cuanto se tienen que acomodar
        lvls = []#cuantos nodos hay en cada nivel
        for x in range(lvl+1):
            lvls.append(self.niveles.count(lvl-x))
            aux.append(round((ancho/self.niveles.count(lvl-x)),0))
            
        nodos_nivel = []#guardaremos los nodos de cada nivel
        num = 7
        for j,x in enumerate(lvls):
            #tomamos los nodos segun la cantidad en cada nivel
            nodos_nivel.append([])
            for i in range(x):
                nodos_nivel[j].append("nodo"+str(num-i))
            num = num - x

        #le asignamos a los primero nodos una pos para heredar las demas de hay
        nodos_nivel_pos = [[]]
        for i,x in enumerate(nodos_nivel[0]):
            nodos_nivel_pos[0].append(aux[0]*i)

        #nos fijamos los nodos de niveles inferiores con cuantos arriba estan conectados
        #si se conecta con un numero par se ubicara en la mitad de estos
        #si se comunica con un numero impar se ubicara en la pos del nodo contral de estos

        #nota: las posiciones no estan centradas ejemplo los cuatro primeros nodos estan en la pos
        # 0,100,200,300 y el espacio que tiene para usar son 400px

    def genPosMANUAL(self, nodo = None, xpos= None, ypos = None):
        """permite modificar alguno de los valores de pos a un nodo"""
        if nodo == None: #se quiere empaquetar las posiciones
            self.pos_dict = dict(zip(self.nodos, self.nodos_pos))
        else:#se especifico un nodo para cambiarle algunos de los argumentos
            if xpos != None:
                if ypos != None:
                    self.pos_dict[nodo] = [xpos,ypos]
                else:
                    self.pos_dict[nodo] = [xpos, self.pos_dict[nodo][1]]
            elif ypos != None:
                self.pos_dict[nodo] = [self.pos_dict[nodo][0], ypos]
        self.swicht_dict = dict(zip(self.nodos, self.nodos)) #definimos estados aleatorios a swicht
    def swicht(self,nodo, estado ):
        """definimos si un nodo es un swicht 1 o si es un nodo de salida 2 o si es un nodo de llegada 3"""
        self.swicht_dict[nodo] = estado

    def estados(self):
        """define estados random para un lista de swiches, ademas returna un dict de estados para cada nodo
        si el nodo es un nodo principal  tmb asigna su unico estado los nodos finales son los unicos que completa
        con None"""
        aux = []#almacenaremos los estados
        for x in self.nodos:
            if self.swicht_dict[x]== 2:
                aux.append([0])
            elif self.swicht_dict[x] == 1:
                c = randint(1,(len(self.pack_dict[x])-1))#random entre las cantidad de opciones que posee el nodo
                for i,x in enumerate(self.pack_dict[x]):
                    if i == c:
                        aux.append([c])
            else:
                aux.append(["final"])
                    
        self.estado_dict = dict(zip(self.nodos, aux))
        
        
                


def test2():
    x = grafo()
    x.nodo("nodo1",0)
    x.nodo("nodo2",1)
    x.nodo("nodo3",2)
    x.nodo("nodo4",3)
    x.nodo("nodo5",3)
    x.nodo("nodo6",3)
    x.nodo("nodo7",3)
    x.arista("nodo1", "nodo2")
    x.arista("nodo2", "nodo3")
    x.arista("nodo2", "nodo7")
    x.arista("nodo3", "nodo4")
    x.arista("nodo3", "nodo5")
    x.arista("nodo3", "nodo6")
    x.arista("nodo7", "nodo2")
    x.packing()
    print x.pack_dict
    print x.pack_array
    print x.nodo_nivel
    print x.nodo_nivel_dict
    x.genPos(400,400)

def test():
    a = ["h", "g", "j"]
    b = [["h","g"], ["h","j"],["g","h"],["j","h"],["g","j"]]

    for x in b:
        x.sort()
        cant =b.count(x)
        if cant >=2:
            b.remove(x)

    aux = []
    for j,x in enumerate(a):
        aux.append([])
        for i in b:
            c = i.count(x)
            if c ==1:
                m = i.index(x)
                if m ==0:
                    aux[j].append(i[1])
                else:
                    aux[j].append(i[0])
    print aux
        

    c = dict(zip(a,aux))
    print c
