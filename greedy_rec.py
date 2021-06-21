#!/usr/bin/python3
# -*- coding: cp1252 -*-
"""System module"""
import sys
import math
sys.setrecursionlimit(10000000)

def sumhrec(acueducto, value, height):
    """sumhrec: calcular el sumatorio de hi recursivo"""
    if value < 0:
        return 0
    elif acueducto[value] == 1:
        return height - YS[value] + sumhrec(acueducto, value-1, height)
    return 0 + sumhrec(acueducto, value-1, height)

def sumdrec(acueducto, value):
    """sumdrec: calcular el sumatorio de di recursivo"""
    if value <= 0:
        return 0
    salir = False
    index = value-1
    while index > 0 and not salir:
        if acueducto[index] == 0:
            index -= 1
        else:
            salir = True
    return (XS[value] - XS[index])**2 + sumdrec(acueducto, index)

def impossible(radius, height, old_x, old_y, old_pointer, index_x, index_y, index_pointer):
    """imposible: primero comprobar altura de los pilares
       luego comprobar los puntos intermedios entre el arco del acueducto"""
    if (height - old_y) < radius or (height - index_y) < radius:
        return True
    elif old_pointer + 1 != index_pointer:
        return impossible_rec(old_pointer + 1, radius, height, index_pointer, index_x, old_x)
    return False

def impossible_rec(loopindex, radius, height, index_pointer, index_x, old_x):
    """imposible_rec: comprobar los puntos intermedios entre el arco del acueducto"""
    if loopindex >= index_pointer:
        return False
    #Necesito un test_x y test_y (del punto que he de comprobar)
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

def generate(acueducto, value, height, alpha, beta, old_x, old_y, old_pointer):
    """generate: generar el acueducto mas barato"""
    provisional_cost = 99999999999999999999999
    new_x = -1
    new_y = -1
    new_pointer = -1
    exist = False
    index = old_pointer + 1
    while index < value:
        #Comprobar todas las combinaciones desde un punto y guardar la opcion mas barata
        sumh = (height - old_y) + (height - YS[index])
        sumd = (XS[index] - old_x)**2
        cost = alpha*sumh + beta*sumd
        radius = (XS[index] - old_x)/2
        newimpossible = impossible(radius, height, old_x, old_y, old_pointer, XS[index], YS[index], index)
        if (not newimpossible) and (cost <= provisional_cost):
            #Nueva combinacion mas barata encontrada (y no imposible)
            provisional_cost = cost
            new_x = XS[index]
            new_y = YS[index]
            new_pointer = index
            exist = True
        if exist:
            index += 1
        else:
            #Si hay uno que no existe, salir del bucle directamente
            index = value
    if exist:
        #Si se ha encontrado una nueva combinacion de puntos, marcarlo en el acueducto
        acueducto[new_pointer] = 1
    else:
        #Si hay un -1, señal de que es imposible
        acueducto[old_pointer] = -1
    if new_pointer == value-1 or not exist:
        #Final
        return acueducto
    #Repetir proceso pero ahora desde el nuevo punto hayado
    return generate(acueducto, value, height, alpha, beta, new_x, new_y, new_pointer)
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
    #Crear acueducto
    ACUEDUCTO = [0 for _ in range(NUMBER)]
    ACUEDUCTO[0] = 1
    ACUEDUCTO = generate(ACUEDUCTO, NUMBER, HEIGHT, ALPHA, BETA, XS[0], YS[0], 0)
    #Comprobar que no hay un -1 que indique que es imposible
    IMPOSSIBLE = False
    LOOP = 0
    while LOOP < NUMBER and not IMPOSSIBLE:
        if ACUEDUCTO[LOOP] == -1:
            IMPOSSIBLE = True
        LOOP += 1
    if not IMPOSSIBLE:
        #Calcular coste total
        SUMHTOTAL = sumhrec(ACUEDUCTO, NUMBER-1, HEIGHT)
        SUMDTOTAL = sumdrec(ACUEDUCTO, NUMBER-1)
        COSTTOTAL = ALPHA*SUMHTOTAL + BETA*SUMDTOTAL
        print(COSTTOTAL)
    else:
        print("impossible")
else:
    print("ERROR: Ningun archivo por parametro")
    
