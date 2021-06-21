#!/usr/bin/python3
# -*- coding: cp1252 -*-
"""System module"""
import sys
import math
sys.setrecursionlimit(10000000)

class Pila:
    """Representacion de una pila"""
    def __init__(self):
        """Crear pila vacia"""
        self.items = []
    def apilar(self, element):
        """Agrega el elemento"""
        self.items.append(element)
    def desapilar(self):
        """Eliminar ultimo elemento de la pila y lo devuelve"""
        try:
            return self.items.pop()
        except IndexError:
            raise ValueError("empty")
    def longitud(self):
        """Devuelve la longitud de la pila"""
        return len(self.items)
    def inspeccionar(self):
        """Devuelve el ultimo elemento de la pila"""
        return self.items[len(self.items)-1]
    def contenido(self):
        """Devuelve todo el contenido de la pila"""
        pila = [0 for _ in range(len(self.items))]
        index = 0
        while index < len(self.items):
            pila[index] = self.items[index]
            index += 1
        return pila

def sumhrec(aqueducto, long1):
    """sumhrec: calcular el sumatorio de hi recursivo"""
    if long1 < 0:
        return 0
    elif aqueducto[long1] == 1:
        return HEIGHT - YS[long1] + sumhrec(aqueducto, long1-1)
    return 0 + sumhrec(aqueducto, long1-1)

def sumdrec(aqueducto, long2):
    """sumdrec: calcular el sumatorio de di recursivo"""
    if long2 <= 0:
        return 0
    salir = False
    index = long2-1
    while index > 0 and not salir:
        if aqueducto[index] == 0:
            index -= 1
        else:
            salir = True
    return (XS[long2] - XS[index])**2 + sumdrec(aqueducto, index)

def impossible(radius, height, old_x, old_y, old_pointer, index_x, index_y, index_pointer):
    """imposible: primero comprobar altura de los pilares
       luego comprobar los puntos intermedios entre el arco del acueducto"""
    if (height - old_y) < radius or (height - index_y) < radius:
        return True
    elif old_pointer + 1 != index_pointer:
        return impossible_rec(old_pointer + 1, radius, height, index_pointer, index_x, old_x)

def impossible_rec(loopindex, radius, height, index_pointer, index_x, old_x):
    """imposible_rec: comprobar los puntos intermedios entre el arco del acueducto"""
    if loopindex >= index_pointer:
        return False
    #Necesito una test_x y test_y (del punto que he de comprobar)
    test_x = XS[loopindex]
    test_y = YS[loopindex]
    #1: Buscar x del punto medio
    medio = (index_x - old_x)/2 + old_x
    #2: Calcular up_x
    up_x = test_x - medio
    #3: Calcular up_y
    up_y = math.sqrt(radius**2 - up_x**2)
    #4: Cacular altura
    alt = up_y + (height - radius)
    #5: Comprobar que no pase la altura
    test_y_float = float(test_y)
    if alt < test_y_float:
        return True
    return impossible_rec(loopindex+1, radius, height, index_pointer, index_x, old_x)

def impossiblestack(pila, height, back_x, back_y, back_pointer=0, index=1):
    """impossiblestack: seleccionar las partes de la pila que hay comprobar
       para saber si son acueductos imposible o no"""
    if index >= len(pila):
        return False
    boolean = False
    if pila[index] == 1:
        front_x = XS[index]
        front_y = YS[index]
        front_pointer = index
        radius = (front_x - back_x)/2
        boolean = impossible(radius, height, back_x, back_y, back_pointer, front_x, front_y, front_pointer)
        return boolean or impossiblestack(pila, height, front_x, front_y, front_pointer, index+1)
    return boolean or impossiblestack(pila, height, back_x, back_y, back_pointer, index+1)

def calculatecost(acueducto):
    """calculateCost: calcular el coste del acueducto entero recibido"""
    lenght = len(acueducto)
    sumh = sumhrec(acueducto, lenght-1)
    sumd = sumdrec(acueducto, lenght-1)
    return ALPHA*sumh + BETA*sumd

def copiarpila(pila):
    """copiarpila: duplicar la pila racibida"""
    copia = Pila()
    intermedio = Pila()
    for index in range(pila.longitud()):
        intermedio.apilar(pila.inspeccionar())
        pila.desapilar()
    for index in range(intermedio.longitud()):
        pila.apilar(intermedio.inspeccionar())
        copia.apilar(intermedio.inspeccionar())
        intermedio.desapilar()
    return copia

def generate(pila, height):
    """generate: generar todos los acueductos posibles y quedarse con el mas barato"""
    global PROVISIONALCOST
    global ANTERIOR
    global MATRIX
    global COUNTER
    copia = copiarpila(pila)
    if copia.longitud() != NUMBER:
        copia.apilar(1)
        if not impossiblestack(copia.contenido(), height, XS[0], YS[0]):
            if copia.longitud() <= 2:
                minicost = calculatecost(copia.contenido())
                ANTERIOR = minicost
                MATRIX.append(minicost)
            else:
                temporal = copia.contenido()
                resto = ANTERIOR
                minicost = calculatecost(temporal)
                ANTERIOR = minicost
                minicost = minicost - resto
                COUNTER += 1
                MATRIX.append(minicost)
            generate(copia, height)
        if copia.longitud() != NUMBER:
            copia.desapilar()
            copia.apilar(0)
            generate(copia, height)
    else:
        index = 0
        othercost = 0
        while index <= COUNTER:
            othercost += MATRIX[index]
            index += 1
        if not impossiblestack(copia.contenido(), height, XS[0], YS[0]) and othercost < PROVISIONALCOST:
            PROVISIONALCOST = othercost
    return PROVISIONALCOST

#main()
if len(sys.argv) == 2:
    #Abrir el fichero y leer la primera linea (split para separar los datos)
    FILE = open(sys.argv[1])
    DATOS = FILE.readline()
    DATOS2 = DATOS.split()
    #Guardar datos de la primera linea
    NUMBER = int(DATOS2[0])
    HEIGHT = int(DATOS2[1])
    ALPHA = int(DATOS2[2])
    BETA = int(DATOS2[3])
    #Guardar coordenadas de los puntos
    XS = [0 for _ in range(NUMBER)]
    YS = [0 for _ in range(NUMBER)]
    for i in range(NUMBER):
        DATOS = FILE.readline()
        DATOS2 = DATOS.split()
        XS[i] = int(DATOS2[0])
        YS[i] = int(DATOS2[1])
    FILE.close()
    #Calcular coste total
    STACK = Pila()
    STACK.apilar(1)
    PROVISIONALCOST = 999999999999999999999999999999
    ANTERIOR = 0
    MATRIX = []
    COUNTER = 0
    COSTACUEDUCTO = generate(STACK, HEIGHT)
    if COSTACUEDUCTO != 999999999999999999999999999999:
        print(COSTACUEDUCTO)
    else:
        print("impossible")
else:
    print("ERROR: Ningun archivo por parametro")
    
