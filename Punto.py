#!/usr/bin/python3
# -*- coding: cp1252 -*-

class Punto():
	x = -1
	y = -1

	def __init__(self, x, y):
		self.x = x
		self.y = y

	def getX(self):
		return self.x

	def getY(self):
		return self.y
	
	#to String
	def __repr__(self):
		return str(self.__dict__)
