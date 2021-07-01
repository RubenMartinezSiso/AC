#!/usr/bin/python3
# -*- coding: cp1252 -*-
"""System module"""
import sys
import math
from itertools import product
from Ficheros import Ficheros

class MyApplication():
    """clase principal"""
    def __init__(self):
        """constructor"""

    def sumhit(self, aqueduct, value, HEIGHT, YS):
        """sumhit: calculate summation of hi iterative"""
        sumh = 0
        index = value
        while index >= 0:
            if aqueduct[index] == 1:
                sumh = sumh + (HEIGHT - YS[index])
            index -= 1
        return sumh

    def sumdit(self, aqueduct, value, XS):
        """sumdit: calculate summation of di iterative"""
        sumd = 0
        index1 = 0
        index2 = value
        while index2 > 0:
            exit = False
            index1 = index2 - 1
            while index1 > 0 and not exit:
                if aqueduct[index1] == 0:
                    index1 -= 1
                else:
                    exit = True
            sumd = sumd + (XS[index2] - XS[index1])**2
            index2 = index1
        return sumd

    def impossible(self, radius, height, old_x, old_y, old_pointer, index_x, index_y, index_pointer, XS, YS):
        """impossible: first check the height of the pillars
                       then check the intermediate points between the arch of the aqueduct"""
        newimpossible = False
        #Check that the pillars are lower than the maximum height
        if (height - old_y) < radius or (height - index_y) < radius:
            newimpossible = True
        #Check the intermediate points between the arch of the aqueduct
        loopindex = old_pointer + 1
        if loopindex != index_pointer and not newimpossible:
            while loopindex < index_pointer:
                #test_x and test_y points are needed (coordinates of the point to be checked)
                test_x = XS[loopindex]
                test_y = YS[loopindex]
                #1: Search coordinate x of mid-point
                medio = (index_x - old_x)/2 + old_x
                #2: Calculate up_x
                up_x = test_x - medio
                #3: Calculate up_y
                up_y = math.sqrt(radius**2 - up_x**2)
                #4: Caculate maxheight
                maxheight = up_y + (height - radius)
                #5: Check that the point does not exceed maxheight
                test_y_float = float(test_y)
                if maxheight < test_y_float:
                    newimpossible = True
                loopindex += 1
        return newimpossible

    def impossiblestack(self, stack, height, XS, YS):
        """impossiblestack: select the parts of the stack to be checked
                            to know if they are impossible aqueducts or not"""
        boolean = False
        back_x = XS[0]
        back_y = YS[0]
        back_pointer = 0
        index = 1
        while index < len(stack) and not boolean:
            if stack[index] == 1:
                front_x = XS[index]
                front_y = YS[index]
                front_pointer = index
                radius = (front_x - back_x)/2
                boolean = self.impossible(radius, height, back_x, back_y, back_pointer, front_x, front_y, front_pointer, XS, YS)
                back_x = front_x
                back_y = front_y
                back_pointer = front_pointer
            index += 1
        return boolean

    def calculatecost(self, aqueduct, XS, YS, NUMBER, HEIGHT, ALPHA, BETA):
        """calculatecost: calculate the cost of the entire aqueduct received"""
        sumh = self.sumhit(aqueduct, NUMBER-1, HEIGHT, YS)
        sumd = self.sumdit(aqueduct, NUMBER-1, XS)
        return ALPHA*sumh + BETA*sumd

    def generate(self, HEIGHT, NUMBER, XS, YS, ALPHA, BETA):
        """generate: create the cheapest aqueduct"""
        provisionalcost = 999999999999999999999999999999
        aqlist = list(product([0, 1], repeat=NUMBER))
        for index in range(2**NUMBER):
            if (aqlist[index][0] == 1 and aqlist[index][NUMBER-1] == 1):
                newcost = self.calculatecost(aqlist[index], XS, YS, NUMBER, HEIGHT, ALPHA, BETA)
                if(not self.impossiblestack(aqlist[index], HEIGHT, XS, YS) and newcost < provisionalcost):
                    provisionalcost = newcost
        return provisionalcost

    def run(self, params):
        """run: ejecute algorithm"""
        if len(sys.argv) == 2:
            #Open the file and read the first line (split to separate the data)
            ALPHA, BETA, HEIGHT, NUMBER, POINTS = Ficheros().leerFichero(params[1])
            XS = [0 for _ in range(NUMBER)]
            YS = [0 for _ in range(NUMBER)]
            for i in range(NUMBER):
                XS[i] = POINTS[i].getX()
                YS[i] = POINTS[i].getY()
            #Calculate total cost
            COSTAQUEDUCT = self.generate(HEIGHT, NUMBER, XS, YS, ALPHA, BETA)
            if COSTAQUEDUCT != 999999999999999999999999999999:
                print(COSTAQUEDUCT)
            else:
                print("impossible")
        else:
            print("ERROR: no file available")

def main():
    """main"""
    sys.setrecursionlimit(10000000)
    app = MyApplication()
    app.run(sys.argv)
if __name__ == '__main__':
    main()
    
