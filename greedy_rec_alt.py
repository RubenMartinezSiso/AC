#!/usr/bin/python3
# -*- coding: cp1252 -*-
"""System module"""
import sys
import math
from Ficheros import Ficheros

class MyApplication():
    """clase principal"""
    def __init__(self):
        """constructor"""
    def sumhrec(self, acueducto, value, height, xs, ys):
        """sumhrec: calcular el sumatorio de hi recursivo"""
        if value < 0:
            return 0
        elif acueducto[value] == 1:
            return height - ys[value] + self.sumhrec(acueducto, value-1, height, xs, ys)
        return 0 + self.sumhrec(acueducto, value-1, height, xs, ys)

    def sumdrec(self, acueducto, value, xs, ys):
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
        return (xs[value] - xs[index])**2 + self.sumdrec(acueducto, index, xs, ys)

    def impossible(self, radius, height, old_x, old_y, old_pointer, index_x, index_y, index_pointer, xs, ys):
        """imposible: primero comprobar altura de los pilares
           luego comprobar los puntos intermedios entre el arco del acueducto"""
        if (height - old_y) < radius or (height - index_y) < radius:
            return True
        elif old_pointer + 1 != index_pointer:
            return self.impossible_rec(old_pointer + 1, radius, height, index_pointer, index_x, old_x, xs, ys)
        return False

    def impossible_rec(self, loopindex, radius, height, index_pointer, index_x, old_x, xs, ys):
        """imposible_rec: comprobar los puntos intermedios entre el arco del acueducto"""
        if loopindex >= index_pointer:
            return False
        #Necesito un test_x y test_y (del punto que he de comprobar)
        test_x = xs[loopindex]
        test_y = ys[loopindex]
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
        return self.impossible_rec(loopindex+1, radius, height, index_pointer, index_x, old_x, xs, ys)

    def generate(self, acueducto, value, height, alpha, beta, old_x, old_y, old_pointer, xs, ys):
        """generate: generar el acueducto mas barato"""
        provisional_cost = 99999999999999999999999
        new_x = -1
        new_y = -1
        new_pointer = -1
        exist = False
        index = old_pointer + 1
        while index < value:
            #Comprobar todas las combinaciones desde un punto y guardar la opcion mas barata
            sumh = (height - old_y) + (height - ys[index])
            sumd = (xs[index] - old_x)**2
            cost = alpha*sumh + beta*sumd
            radius = (xs[index] - old_x)/2
            newimpossible = self.impossible(radius, height, old_x, old_y, old_pointer, xs[index], ys[index], index, xs, ys)
            if (not newimpossible) and (cost <= provisional_cost):
                #Nueva combinacion mas barata encontrada (y no imposible)
                provisional_cost = cost
                new_x = xs[index]
                new_y = ys[index]
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
        return self.generate(acueducto, value, height, alpha, beta, new_x, new_y, new_pointer, xs, ys)

    def run(self, params):
        if len(sys.argv) == 2:
            alpha, beta, height, number, puntos = Ficheros().leerFichero(params[1])
            #conversion a variables
            xs = [0 for _ in range(number)]
            ys = [0 for _ in range(number)]
            for i in range(number):
                xs[i] = puntos[i].getX()
                ys[i] = puntos[i].getY()
            #Crear acueducto
            acueducto = [0 for _ in range(number)]
            acueducto[0] = 1
            acueducto = self.generate(acueducto, number, height, alpha, beta, xs[0], ys[0], 0, xs, ys)
            #Comprobar que no hay un -1 que indique que es imposible
            impossible = False
            loop = 0
            while loop < number and not impossible:
                if acueducto[loop] == -1:
                    impossible = True
                loop += 1
            if not impossible:
                #Calcular coste total
                sumhtotal = self.sumhrec(acueducto, number-1, height, xs, ys)
                sumdtotal = self.sumdrec(acueducto, number-1, xs, ys)
                costtotal = alpha*sumhtotal + beta*sumdtotal
                print(costtotal)
            else:
                print("impossible")
        else:
            print("ERROR: Ningun archivo por parametro")

def main():
    """main"""
    sys.setrecursionlimit(10000000)
    app = MyApplication()
    app.run(sys.argv)
if __name__ == '__main__':
    main()
