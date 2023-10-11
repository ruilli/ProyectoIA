import cv2
import numpy as np
import random
import matplotlib.pyplot as plt
import im as Inc
n=int(input("Ingrese Monmento de dia [Mañana:1] [Tarde:2] [Noche:3]"))-1
m=int(input("Ingrese Si llueve [Si:1] [No:2]"))-1
if m==1:#si no esta lloviendo pedir el pronostico del clima
   b=float(input("Ingrese pronostico de lluvia[valores de 0 a 1]"))
else:
   b=1
lista=Inc.Incertidumbre(n,m,b)#tomamos los valores de semaforo, accidente y trefico
semaforo=int(lista[0])
trafico=int(lista[2])
accidente=int(lista[1])
print(lista)

def generador_lista_colores(imagen):
  colores = [] # Creo una lista para almacenar los colores de los píxeles
  alto, ancho, canales = imagen.shape #tomo las dimenciones de la matris correspondiente a la imagen
  for y in range(alto):   # recorro la imagen y obtengo el color de cada pixel
      for x in range(ancho):
          color_bgr = imagen[y, x] # Obtener el color del píxel en formato BGR
          color_rgb = (color_bgr[2], color_bgr[1], color_bgr[0]) # Convertir el color a formato RGB
          colores.append(color_rgb) #rojo,verde,azul
  return colores

class Nodo():
    def __init__(self, estado, padre,heuristica):
        self.estado = estado #estado actual de nodo
        self.padre = padre #padre del nodo anterior
        self.heuristica = heuristica   # Agregamos una heurística al nodo    

class Frontera():
    def __init__(self):
        self.frontera =[]
        # inicializamos el constructor y creamos lista vacia
    def empty(self):
        return (len(self.frontera) == 0)
        # verifica la frontera esta vacia o no
    def add(self, nodo):
        self.frontera.append(nodo)
        # añadiendo nodos a la frontera
    def eliminar(self):
        nodo = self.frontera[-1]
        self.frontera = self.frontera[:-1]
        return nodo
        # identificamos el nodo a eliminar
class Laberinto():
    def __init__(self, filename):
        self.imagen = cv2.imread(filename)
        colores = generador_lista_colores(self.imagen) #creamos una listaanidada que contiene los colores de los pixeles
        # Verificamos punto inicial y objetivo
        if colores.count((255,0,0)) != 1:#el punto rojo
            raise Exception("El laberinto debe tener solo un punto de inicio")
        if colores.count((0,0,255)) != 1:#el punto azul
            raise Exception("El laberinto debe ter tener exactamente un objetivo")
        self.contenido = colores  #Globaliso la lista de colores
        self.altura = len(self.imagen)  # altura del laberinto
        self.ancho = max(len(line) for line in self.imagen)  # el ancho del laberinto
        self.solucion = None  # rastrea la solución
        self.muros = []  # lista que nos dice si hay muro o no
        for i in range(self.altura):
            filas = []
            for j in range(self.ancho):
                try:
                    color_bgr = self.imagen[i, j]
                    color_rgb = (color_bgr[2], color_bgr[1], color_bgr[0])
                    if color_rgb==(255,0,0):
                        self.inicio = (i, j)  # Estado inicial, donde comienza
                        filas.append(False)   # false dice que no es un muro
                    elif color_rgb==(0,0,255):
                        self.objetivo = (i, j)  # Estado objetivo, donde comienza
                        filas.append(False)   # false dice que no es un muro
                    elif color_rgb !=(0,0,0): # si no es negro
                        filas.append(False)   # false dice que no es un muro
                    else:
                        filas.append(True)  # tonc muro
                except IndexError:
                    filas.append(False)
            self.muros.append(filas) #Agregamos la fila a la lista


              
    def vecinos(self, estado):
        fila, columna = estado  # desempaqueta estado en x,y
        candidatos = [
            ("up", (fila - 1, columna)),
            ("down", (fila + 1, columna)),
            ("left", (fila, columna - 1)),
            ("right", (fila, columna + 1))  # lista de tuplas con el posible movimiento
            ]
        resultados = []  # aquí van a quedar los vecinos válidos
        for accion, (f, c) in candidatos:
            if 0 <= f < self.altura and 0 <= c < self.ancho and not self.muros[f][c]:  # verifica altura, ancho, muro
                resultados.append((accion, (f, c)))  # se guarda en la lista
                random.shuffle(resultados)# desordenamos los vecinos para aleatorisar el primer vecino a explorar
        return resultados


    def distancia_manhattan(self, estado):
        distancia = abs(estado[0] - self.objetivo[0]) + abs(estado[1] - self.objetivo[1])  # distancia horizontal y vertical entre los puntos
        return distancia


    def solve_all(self, num_rutas=3):
        # Encuentra un número específico de rutas hacia el objetivo en el laberinto
        soluciones = []  # Almacenará las rutas encontradas
        while len(soluciones) < num_rutas:
            # Reiniciamos la exploración
            self.num_explorados = 0
            self.explorado = set()
            # Inicializamos la frontera y realizamos la búsqueda
            start = Nodo(estado=self.inicio, padre=None,heuristica=self.distancia_manhattan(self.inicio))
            frontera = Frontera()
            frontera.add(start)
            while not frontera.empty() and len(soluciones) < num_rutas:
                #frontera.frontera.sort(key=lambda nodo: nodo.heuristica, reverse=True) #ordenamos la listafrontera por heuristica
                nodo = frontera.eliminar()
                self.num_explorados += 1 # contador
                # Si el nodo es el objetivo, entonces tenemos una solución
                if nodo.estado == self.objetivo:# al encontar el objetivo
                    costo = [] # lista costo del tiempo perdido en cada nodo
                    cel = [] # lista cel donde guardaremos las cordenadas del nodo
                    while nodo.padre is not None: # rastreamos el nodo padre
                        costo.append(nodo.heuristica)
                        cel.append(nodo.estado)
                        nodo = nodo.padre
                    costo.reverse()
                    cel.reverse()
                    soluciones.append((costo, cel))# agregamos la solucion hallada a la lista
                self.explorado.add(nodo.estado)  #evitar repetir el mismo estado

                for accion, estado in self.vecinos(nodo.estado): #identificamos los vecinos
                    if estado not in self.explorado: #vemos si no se encuentra en el congunto explorado
                        i,j=estado # descomponemos en i,j la cordenada que nos da estado
                        if (self.imagen[i, j]==[255,255,0]).all(): #identificamos el color del pixel corespondiente a semaforo
                          DM=semaforo
                        elif (self.imagen[i, j]==[255,0,255]).all(): #identificamos el color del pixel corespondiente a trafico
                          DM=trafico
                        elif (self.imagen[i, j]==[0,255,255]).all(): #identificamos el color del pixel corespondiente a accidente
                          DM=accidente
                        else:
                          DM=1 #sino solo usamos la distancia manhatan como metrica
                        hijo = Nodo(estado=estado, padre=nodo, heuristica=DM)
                        frontera.add(hijo)#añadimos el nodo a la frontera


        # ordenamos la lista por medio de la suma de todas las metricas de cada nodo en cada una de las soluciones
        def suma_de_sublista(elemento):
          return sum(elemento[0])
        # Ordenar la lista de listas por la suma de los números en cada sublista
        soluciones = sorted(soluciones, key=suma_de_sublista)
        nuevalista=[]# esta lista se crea para eliminar soluciones iguales
        for x in soluciones:# recorremos todas las soluciones
          er=0 #identificador o bandera
          if nuevalista==[]: #si la lista esta vacia agregamos la primera solucion
            nuevalista.append(x)
          for i in nuevalista: #recorremos la nueva lista
            if x==i: #si la nueva lista se encuentra en soluciones activamos la bandera (er=1) y salimos del for
              er=1
              break
          if er==0: # si la vandera no esta activa al salir del for quiere decir que la nueva lista no se encuentra en solucione
            nuevalista.append(x) #la agregamos
        self.soluciones = nuevalista #globalisamos la nueva lista
        self.solucion = soluciones




l=Laberinto('./NY61x62.png')
print("Calculando")
l.solve_all(50000)
print("Número de rutas halladas:",len(l.soluciones))
print("Número total de rutas exploradas:",len(l.solucion))

def printar_solve3(): # pintamos las soluciones
    for idx, solucion in enumerate(l.soluciones, start=1):
        imagen_en_blanco = np.zeros((l.altura, l.ancho, 3), dtype=np.uint8) # creamos una imagen en blanco
        acciones, estados = solucion
        print(f"Ruta {idx}:", end=' ')
        for i, fila in enumerate(l.muros):# recorremos la lista muros y la dibujaremos sobre la magen en blanco
            for j, col in enumerate(fila):
                if (i, j) == l.inicio:# si la posicion i,j corresponde a la posicion de inicio la coloreamos de azul
                    imagen_en_blanco[i,j]=(255,0,0)
                elif (i, j) == l.objetivo:# si la posicion i,j corresponde a la posicion objetivo la coloreamos de rojo
                    imagen_en_blanco[i,j]=(0,0,255)
                elif (i, j) in estados: # si corresponde a la posiciones de la solucion la coloreamos de verde
                    imagen_en_blanco[i,j]=(0,255,0)
                elif col: # si corresponde a un muro la coloreamos de negro
                    imagen_en_blanco[i,j]=(0,0,0)
                else: #si no es ninguna de las anteriores la coloreamos de blanco
                    imagen_en_blanco[i,j]=(255,255,255)
        imagen_redimensionada = cv2.resize(imagen_en_blanco, (l.ancho*1,l.altura*1)) #redimencionamos la imagen
        x=plt.subplot(1,3,idx)
        x.title.set_text(f"Ruta {idx}")
        x.set_axis_off()
        plt.imshow(imagen_redimensionada) #la montramos
        def suma_de_distascias():# esto es para mostrar el costo total de la ruta
          f=0
          for i in acciones:
            f +=i
          return f
        print(f"Acciones: {suma_de_distascias()}")
        if idx >= 3:# esto es para mostrar las 3 primeras soluciones
          break
printar_solve3()
plt.show()
