#!/usr/bin/python3
# -*- coding: cp1252 -*-
"""System module"""
import sys
import math
from Ficheros import Ficheros

class Stack:
    """Representation of a stack"""
    def __init__(self):
        """Create empty stack"""
        self.items = []
    def pile(self, element):
        """Add element"""
        self.items.append(element)
    def unstack(self):
        """Remove last item from the stack and return it"""
        try:
            return self.items.pop()
        except IndexError:
            raise ValueError("empty")
    def size(self):
        """Returns the length of the stack"""
        return len(self.items)
    def lastitem(self):
        """Returns the last item of the stack"""
        return self.items[len(self.items)-1]
    def content(self):
        """Returns the entire contents of the stack"""
        stack = [0 for _ in range(len(self.items))]
        index = 0
        while index < len(self.items):
            stack[index] = self.items[index]
            index += 1
        return stack

class MyApplication():
    """clase principal"""
    def __init__(self):
        """constructor"""

    def sumhrec(self, aqueduct, value, height, XS, YS):
        """sumhrec: calculate summation of hi recursive"""
        if value < 0:
            return 0
        elif aqueduct[value] == 1:
            return height - YS[value] + self.sumhrec(aqueduct, value-1, height, XS, YS)
        return 0 + self.sumhrec(aqueduct, value-1, height, XS, YS)

    def sumdrec(self, aqueduct, value, XS, YS):
        """sumdrec: calculate summation of di recursive"""
        if value <= 0:
            return 0
        exit = False
        index = value-1
        while index > 0 and not exit:
            if aqueduct[index] == 0:
                index -= 1
            else:
                exit = True
        return (XS[value] - XS[index])**2 + self.sumdrec(aqueduct, index, XS, YS)

    def impossible(self, radius, height, old_x, old_y, old_pointer, index_x, index_y, index_pointer, XS, YS):
        """impossible: first check the height of the pillars
                       then check the intermediate points between the arch of the aqueduct"""
        if (height - old_y) < radius or (height - index_y) < radius:
            return True
        elif old_pointer + 1 != index_pointer:
            return self.impossible_rec(old_pointer + 1, radius, height, index_pointer, index_x, old_x, XS, YS)
        return False

    def impossible_rec(self, loopindex, radius, height, index_pointer, index_x, old_x, XS, YS):
        """imposible_rec: check the intermediate points between the arch of the aqueduct"""
        if loopindex >= index_pointer:
            return False
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
            return True
        return self.impossible_rec(loopindex+1, radius, height, index_pointer, index_x, old_x, XS, YS)

    def impossiblestack(self, stack, height, back_x, back_y, XS, YS, back_pointer=0, index=1):
        """impossiblestack: select the parts of the stack to be checked
                            to know if they are impossible aqueducts or not"""
        if index >= len(stack):
            return False
        boolean = False
        if stack[index] == 1:
            front_x = XS[index]
            front_y = YS[index]
            front_pointer = index
            radius = (front_x - back_x)/2
            boolean = self.impossible(radius, height, back_x, back_y, back_pointer, front_x, front_y, front_pointer, XS, YS)
            return boolean or self.impossiblestack(stack, height, front_x, front_y, XS, YS, front_pointer, index+1)
        return boolean or self.impossiblestack(stack, height, back_x, back_y, XS, YS, back_pointer, index+1)

    def calculatecost(self, aqueduct, XS, YS, NUMBER, HEIGHT, ALPHA, BETA):
        """calculatecost: calculate the cost of the entire aqueduct received"""
        sumh = self.sumhrec(aqueduct, NUMBER-1, HEIGHT, XS, YS)
        sumd = self.sumdrec(aqueduct, NUMBER-1, XS, YS)
        return ALPHA*sumh + BETA*sumd

    def copystack(self, stack):
        """copystack: duplicate stack"""
        stack2 = Stack()
        between = Stack()
        for index in range(stack.size()):
            between.pile(stack.lastitem())
            stack.unstack()
        for index in range(between.size()):
            stack.pile(between.lastitem())
            stack2.pile(between.lastitem())
            between.unstack()
        return stack2

    def generate(self, stack, HEIGHT, NUMBER, XS, YS, ALPHA, BETA):
        """generate: create the cheapest aqueduct"""
        global PROVISIONALCOST
        stack2 = self.copystack(stack)
        if stack2.size() != NUMBER:
            stack2.pile(1)
            if not self.impossiblestack(stack2.content(), HEIGHT, XS[0], YS[0], XS, YS):
                self.generate(stack2, HEIGHT, NUMBER, XS, YS, ALPHA, BETA)
            if stack2.size() != NUMBER:
                stack2.unstack()
                stack2.pile(0)
                self.generate(stack2, HEIGHT, NUMBER, XS, YS, ALPHA, BETA)
        else:
            newcost = self.calculatecost(stack2.content(), XS, YS, NUMBER, HEIGHT, ALPHA, BETA)
            if not self.impossiblestack(stack2.content(), HEIGHT, XS[0], YS[0], XS, YS) and newcost < PROVISIONALCOST:
                PROVISIONALCOST = newcost
        return PROVISIONALCOST

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
            STACK = Stack()
            STACK.pile(1)
            COSTAQUEDUCT = self.generate(STACK, HEIGHT, NUMBER, XS, YS, ALPHA, BETA)
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
    PROVISIONALCOST = 999999999999999999999999999999
    main()
    
