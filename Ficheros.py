#!/usr/bin/python3
# -*- coding: cp1252 -*-
from Punto import Punto

#clase que devuelve los datos del fichero.
class Ficheros():
	alfa=-1
	beta=-1
	h=-1
	n=-1
	puntos= []
	
	def leerFichero (self,nombreFichero):
		f = open(nombreFichero)
		datos = f.readline()
		tokens = datos.split()
		
		#guardar datos de la primera linea
		self.n = int(tokens[0])
		self.h = int(tokens[1])
		self.alfa = int(tokens[2])
		self.beta = int(tokens[3])

		#guardar coordenadas de los puntos
		for i in range(self.n):
			coordenadas = f.readline()
			tokensCoordenadas = coordenadas.split()
			punto=Punto(int(tokensCoordenadas[0]),int(tokensCoordenadas[1]))
			self.puntos.append(punto)
		
		f.close()
		return self.alfa,self.beta,self.h,self.n,self.puntos
