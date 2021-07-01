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

    def sumhit(self, HEIGHT, aqueduct, value, YS):
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

    def impossible(self, HEIGHT, radius, old_x, old_y, old_pointer, index_x, index_y, index_pointer, XS, YS):
        """impossible: first check the height of the pillars
                       then check the intermediate points between the arch of the aqueduct"""
        newimpossible = False
        #Check that the pillars are lower than the maximum height
        if (HEIGHT - old_y) < radius or (HEIGHT - index_y) < radius:
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
                maxheight = up_y + (HEIGHT - radius)
                #5: Check that the point does not exceed maxheight
                test_y_float = float(test_y)
                if maxheight < test_y_float:
                    newimpossible = True
                loopindex += 1
        return newimpossible

    def generate(self, HEIGHT, aqueduct, value, height, alpha, beta, old_x, old_y, old_pointer, XS, YS):
        """generate: create the cheapest aqueduct"""
        new_pointer = 0
        exist = False
        while (new_pointer < value-1 or not exist) and (new_pointer != -1):
            provisional_cost = 99999999999999999999999
            new_x = -1
            new_y = -1
            new_pointer = -1
            exist = False
            index = old_pointer + 1
            while index < value:
                #Check all combinations from one point and save the cheapest option
                sumh = (height - old_y) + (height - YS[index])
                sumd = (XS[index] - old_x)**2
                cost = alpha*sumh + beta*sumd
                radius = (XS[index] - old_x)/2
                isimpossible = self.impossible(HEIGHT, radius, old_x, old_y, old_pointer, XS[index], YS[index], index, XS, YS)
                if (not isimpossible) and (cost <= provisional_cost):
                    #New cheapest combination found (and not impossible)
                    provisional_cost = cost
                    new_x = XS[index]
                    new_y = YS[index]
                    new_pointer = index
                    exist = True
                if exist:
                    index += 1
                else:
                    #If there is one that not exists, exit the loop directly
                    index = value
            if exist:
                #If it has been found a new points combination, mark it in the aqueduct
                aqueduct[new_pointer] = 1
            else:
                #If there is a -1, a sign that it is impossible
                aqueduct[old_pointer] = -1
            #Repeat the process but now from the new point found
            old_x = new_x
            old_y = new_y
            old_pointer = new_pointer
        #End
        return aqueduct

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
            #Create aqueduct
            AQUEDUCT = [0 for _ in range(NUMBER)]
            AQUEDUCT[0] = 1
            AQUEDUCT = self.generate(HEIGHT, AQUEDUCT, NUMBER, HEIGHT, ALPHA, BETA, XS[0], YS[0], 0, XS, YS)
            #Check that there is no -1 indicating that it is impossible
            IMPOSSIBLE = False
            LOOP = 0
            while LOOP < NUMBER and not IMPOSSIBLE:
                if AQUEDUCT[LOOP] == -1:
                    IMPOSSIBLE = True
                LOOP += 1
            if not IMPOSSIBLE:
                #Calculate total cost
                SUMHTOTAL = self.sumhit(HEIGHT, AQUEDUCT, NUMBER-1, YS)
                SUMDTOTAL = self.sumdit(AQUEDUCT, NUMBER-1, XS)
                COSTTOTAL = ALPHA*SUMHTOTAL + BETA*SUMDTOTAL
                print (COSTTOTAL)
            else:
                print ("impossible")
        else:
            print("ERROR: no file available")

def main():
    """main"""
    sys.setrecursionlimit(10000000)
    app = MyApplication()
    app.run(sys.argv)
if __name__ == '__main__':
    main()
    
