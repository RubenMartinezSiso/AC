***ACUEDUCTO ÓPTIMO***
***Práctica 2 – Algoritmia y complejidad***

Grupo	GPraAula 3
Fecha	01/07/21
Nombre	Martínez Sisó, Rubén
DNI		48251151A
Escuela politécnica superior UdL
2º Curso – 2º Cuatrimestre Grado de Ingeniería Informática


**Introducción**
La actividad consiste en crear un algoritmo que calcule cuál es el acueducto más barato de hacer dado unos puntos de elevación en el terreno. El algoritmo recibirá una serie de datos: el número de pilares máximos, la altura deseada al nivel del mar, dos factores de coste y las coordenadas (x,y) de las diferentes elevaciones de terreno. Además, habrá que tener en cuenta que, en algunos casos, el acueducto podrá llegar a ser imposible de construir.
Para calcular el coste, se deberá utilizar la siguiente fórmula:
Todas las soluciones adjuntadas requieren de los archivos Ficheros.py y Punto.py (también adjuntos) para ser ejecutados.
Repositorio Github con todas las soluciones: https://github.com/RubenMartinezSiso/AC
En todos los casos, se ha utilizado un sistema en el que el acueducto viene determinado por una serie de unos y ceros. De esta forma, si un punto tiene columna, su valor es 1, y si no tiene, su valor es 0. Por ejemplo, un acueducto de 5 puntos podría ser este: 10101, de forma que habría una columna en el primer, tercer y último punto.
Cabe destacar que en todos los algoritmos se hace uso de la función impossible (o impossible_rec para las soluciones recursivas) que permite comprobar si los puntos del terreno que hay debajo del arco de un acueducto realmente no llegan a sobrepasar el propio arco.
El siguiente esquema sirve como guía para aclarar los pasos de la función. Concretamente, en este ejemplo se desea comprobar si el punto (3’5, 3) superan el arco formado por el acueducto entre el punto (1, 1) y (4, 0). El objetivo es siempre averiguar el valor de up_y y compararlo con el valor de test_y (en este caso, 3)


**Algoritmo greedy**
Se comienza desde el primer punto del terreno y se calcula el coste de todos los posibles acueductos cuyos dos pilares estén en el punto inicial y en uno de los otros puntos del terreno. Tras escoger el acueducto con menor coste, se repite el proceso, pero desde el último punto escogido.
Por ejemplo, desde el punto 0 se comprueba con que otros puntos del terreno se puede unir y cuál es más barato. Si se crea ese acueducto con el punto 3, ahora se comprobará desde el propio punto 3 con el resto de los puntos del terreno cuál es el acueducto más barato a crear.
La búsqueda finaliza cuándo se hayan conectado el primer y último punto del terreno y, finalmente, se obtiene el coste total del acueducto generado. En el caso de que no se pueda conectar ningún punto con el actual, el acueducto se califica como imposible.

*SOLUCIÓN RECURSIVA (greedy_rec.py)*
PSEUDOCÓDIGO (ALGORITMO PRINCIPAL)
MIENTRAS (index < número total de puntos del terreno) HACER
	calcular coste del acueducto entre el punto actual y el indicado por index
	comprobar si el nuevo acueducto es imposible
	SI (no es imposible) AND (nuevo coste obtenido menor que el ya guardado)
		guardar coste, coordenadas e índice del punto que crea el nuevo acueducto más barato
	
	SI (existe un posible acueducto)
		index += 1
	SINO
		#Si no se ha encontrado un acueducto más barato, salir del bucle
		index = número total de puntos

SI (se ha encontrado un nuevo acueducto)
	marcar en el acueducto el valor “1” para indicar que en ese punto del terreno hay un pilar
SINO
	marcar en el acueducto el valor “-1” para indicar que el acueducto es imposible porque no se puede continuar y es imposible conectar el primer y último punto del terreno

SI (el nuevo índice obtenido pertenece al último punto del terreno)
	devolver la matriz de unos y ceros que indica los pilares del acueducto
SINO
	repetir proceso a través de una llamada recursiva, donde el punto actual será el último que hemos conectado con el acueducto

COSTE: O(n)
El algoritmo no incluye bucles, las llamadas recursivas no acumulan coste en exceso.
GITHUB: https://github.com/RubenMartinezSiso/AC/blob/main/greedy_rec.py

*SOLUCIÓN ITERATIVA (greedy_it.py)*
PSEUDOCÓDIGO (ALGORITMO PRINCIPAL)
MIENTRAS (el nuevo índice del punto del terreno no sea el del último punto del terreno) AND (ese índice sea distinto de -1) HACER
	MIENTRAS (index < número total de puntos del terreno) HACER
		calcular coste del acueducto entre el punto actual y el indicado por index
		comprobar si el nuevo acueducto es imposible
		SI (no es imposible) AND (nuevo coste obtenido menor que el ya guardado)
			guardar coste, coordenadas e índice del punto que crea el nuevo acueducto más barato
	
		SI (existe un posible acueducto)
			index += 1
		SINO
			#Si no se ha encontrado un acueducto más barato, salir del bucle
			index = número total de puntos

	SI (se ha encontrado un nuevo acueducto)
		marcar en el acueducto el valor “1” para indicar que en ese punto del terreno hay un pilar
	SINO
		marcar en el acueducto el valor ” -1” para indicar que el acueducto es imposible porque no se puede continuar y es imposible conectar el primer y último punto del terreno

	ahora el índice y las coordenadas del punto actual pasan a ser las del último 	que hemos conectado con el acueducto
devolver la matriz de unos y ceros que indica los pilares del acueducto

COSTE: O(n2)
Algunas funciones empleadas, como la utilizada para el algoritmo principal, requieren de dos bucles anidados, lo que provoca un aumento significativo del coste.
GITHUB: https://github.com/RubenMartinezSiso/AC/blob/main/greedy_it.py


**Algoritmo backtracking**
A diferencia del anterior algoritmo, en este no se crea un solo acueducto poco a poco. En su lugar, se crean todas las posibles combinaciones de pilares, como si de un árbol binario se tratase, y se escoge el acueducto de menor coste.
A esto se le añaden las restricciones de que el acueducto no puede ser imposible de crear y ambos extremos del acueducto deben tener pilares. Si durante la creación de un acueducto completo se detecta que no se cumplen las restricciones, se deja continuar por esa “rama del árbol”.
Los siguientes algoritmos utilizan una pila para acumular las diferentes combinaciones de pilares. El procedimiento consiste en que por cada “1” acumulado en la pila, posteriormente se ha de intercambiar por un “0” gracias a una llamada recursiva. Esto se cumple para todos los puntos excepto para el primero y el último ya que, como hemos comentado, ambos extremos del acueducto deben tener pilares.
El siguiente esquema muestra un ejemplo de como se generarían las posibles soluciones con 4 puntos en el terreno (2(número de puntos – 2) combinaciones totales)

*SOLUCIÓN RECURSIVA (backtracking_rec.py)*
PSEUDOCÓDIGO (ALGORITMO PRINCIPAL)
#Al inicio, la pila está vacía
SI (tamaño de la pila distinto del número total de puntos del terreno, es decir, la pila
     está incompleta)
	apilar el valor “1” en la pila
	SI (el acueducto indicado en la pila no es imposible de hacer)
		llamada recursiva a la propia función enviando esta misma pila
	SI (la pila está incompleta)
		#No se cambia el último “1” por el “0” en el caso de que la pila se encuentre llena en este momento porque el acueducto siempre debe acabar en 1
		desapilar el último valor de la pila
		apilar el valor “0” en la pila
		llamada recursiva a la propia función enviando esta misma pila
SINO
	#Pila llena
	calcular el coste del acueducto indicado en la pila
	SI (el acueducto indicado en la pila no es imposible de hacer) AND (el nuevo coste calculado el menor que el guardado anteriormente)
		el nuevo coste pasa a ser el provisional
devolver el coste final

COSTE: O(n)
El algoritmo no incluye bucles principales, las llamadas recursivas no acumulan coste en exceso.
GITHUB: https://github.com/RubenMartinezSiso/AC/blob/main/backtracking_rec.py

*SOLUCIÓN ITERATIVA (backtracking_it.py)*
PSEUDOCÓDIGO (ALGORITMO PRINCIPAL)
#Al inicio, la pila está vacía
SI (tamaño de la pila distinto del número total de puntos del terreno, es decir, la pila
     está incompleta)
	apilar el valor “1” en la pila
	SI (el acueducto indicado en la pila no es imposible de hacer)
		llamada recursiva a la propia función enviando esta misma pila
	SI (la pila está incompleta)
		#No se cambia el último “1” por el “0” en el caso de que la pila se encuentre llena en este momento porque el acueducto siempre debe acabar en 1
		desapilar el último valor de la pila
		apilar el valor “0” en la pila
		llamada recursiva a la propia función enviando esta misma pila
SINO
	#Pila llena
	calcular el coste del acueducto indicado en la pila
	SI (el acueducto indicado en la pila no es imposible de hacer) AND (el nuevo coste calculado el menor que el guardado anteriormente)
		el nuevo coste pasa a ser el provisional
devolver el coste final

COSTE: O(n2)
Una función empleada requiere de dos bucles anidados, lo que provoca un aumento significativo del coste.
GITHUB: https://github.com/RubenMartinezSiso/AC/blob/main/backtracking_it.py


*SOLUCIÓN ITERATIVA ALTERNATIVA (backtracking_it_alt.py)*
Se ha añadido una versión iterativa alternativa en la que, a pesar de que no se cumple el planteamiento correctamente, se hace uso de listas en el algoritmo principal para evitar totalmente la recursividad. En este caso, no se hace uso de una pila.
PSEUDOCÓDIGO (ALGORITMO PRINCIPAL)
crear una lista con todas las combinaciones posibles de unos y ceros del tamaño del número total de puntos del terreno
MIENTRAS (index perteneciente al rango de 2^(número total de puntos del terreno) )
	#2^NUMBER es el número total de combinaciones obtenidas
	SI (el primer o último valor de la combinación de números es “1”)
		calcular el coste del acueducto indicado en la lista
		SI (el acueducto indicado en la lsita no es imposible de hacer) AND (el nuevo coste calculado el menor que el guardado anteriormente)
			el nuevo coste pasa a ser el provisional
devolver el coste final

COSTE: O(n2)
Una función empleada requiere de dos bucles anidados, lo que provoca un aumento significativo del coste.
GITHUB: https://github.com/RubenMartinezSiso/AC/blob/main/backtracking_it_alt.py


**Algoritmo dynamic programming**
En este algoritmo se utiliza un planteamiento similar al anterior. La diferencia erradica en que se calculan los costes de los diferentes acueductos a medida que creamos el árbol binario. De esta manera, no se calculan los costes desde cero para cada combinación, sino que se van guardando en un vector y acumulando.
Por ejemplo, para un acueducto de 5 puntos en el terreno, se puede llegar a un nodo del árbol con la combinación 101_ _ cuyo coste es 6200€. Si al continuar por el árbol se llega a la combinación 1011_, no se volvería a calcular el coste desde cero, sino que se acumularía a 6200€ (es decir, 6200 + el coste del acueducto _ _ 11 _).
Este algoritmos también utiliza una pila para generar las posibles soluciones.

*SOLUCIÓN RECURSIVA (dynamic_rec.py)*
PSEUDOCÓDIGO (ALGORITMO PRINCIPAL)
#Al inicio, la pila está vacía
SI (tamaño de la pila distinto del número total de puntos del terreno, es decir, la pila
     está incompleta)
	apilar el valor “1” en la pila
	SI (el acueducto indicado en la pila no es imposible de hacer)
		SI (el tamaño de la pila es menor o igual que 2)
			calcular y guardar el coste del acueducto indicado en la pila
			almacenar el coste en la matriz
		SINO
			calcular el nuevo coste a partir del anterior
			almacenar el coste en la matriz
		llamada recursiva a la propia función enviando esta misma pila
	SI (la pila está incompleta)
		#No se cambia el último “1” por el “0” en el caso de que la pila se encuentre llena en este momento porque el acueducto siempre debe acabar en 1
		desapilar el último valor de la pila
		apilar el valor “0” en la pila
		llamada recursiva a la propia función enviando esta misma pila
SINO
	#Pila llena
	calcular el coste del acueducto sumando los valores acumulados en la matriz
	SI (el acueducto indicado en la pila no es imposible de hacer) AND (el nuevo coste calculado el menor que el guardado anteriormente)
		el nuevo coste pasa a ser el provisional
devolver el coste final

COSTE: O(n)
El algoritmo no incluye bucles principales, las llamadas recursivas no acumulan coste en exceso.
GITHUB: https://github.com/RubenMartinezSiso/AC/blob/main/dynamic_rec.py

*SOLUCIÓN ITERATIVA (dynamic_it.py)*
PSEUDOCÓDIGO (ALGORITMO PRINCIPAL)
#Al inicio, la pila está vacía
SI (tamaño de la pila distinto del número total de puntos del terreno, es decir, la pila
     está incompleta)
	apilar el valor “1” en la pila
	SI (el acueducto indicado en la pila no es imposible de hacer)
		SI (el tamaño de la pila es menor o igual que 2)
			calcular y guardar el coste del acueducto indicado en la pila
			almacenar el coste en la matriz
		SINO
			calcular el nuevo coste a partir del anterior
			almacenar el coste en la matriz
		llamada recursiva a la propia función enviando esta misma pila
	SI (la pila está incompleta)
		#No se cambia el último “1” por el “0” en el caso de que la pila se encuentre llena en este momento porque el acueducto siempre debe acabar en 1
		desapilar el último valor de la pila
		apilar el valor “0” en la pila
		llamada recursiva a la propia función enviando esta misma pila
SINO
	#Pila llena
	calcular el coste del acueducto sumando los valores acumulados en la matriz
	SI (el acueducto indicado en la pila no es imposible de hacer) AND (el nuevo coste calculado el menor que el guardado anteriormente)
		el nuevo coste pasa a ser el provisional
devolver el coste final

COSTE: O(n2)
Una función empleada requiere de dos bucles anidados, lo que provoca un aumento significativo del coste.
GITHUB: https://github.com/RubenMartinezSiso/AC/blob/main/dynamic_it.py


**Comentarios**
Esta actividad ha mejorado la capacidad de programación junto con la implementación de algoritmos. También se ha requerido un buen análisis del código y comprensión del funcionamiento de diversos recursos. Cabe destacar que la buena colaboración por parte de los profesores ha resultado de gran ayuda a la hora de plantear las diferentes soluciones. Lamentablemente, algunos de los algoritmos presentados no presentan un planteamiento totalmente eficaz. 
Personalmente, a pesar del gran esfuerzo que me ha requerido la implementación de esta actividad, los programas son mejorables y no acaban de satisfacer mis expectativas. La falta de experiencia y práctica ha sido perjudicial, además de adiciones como algoritmos novedosos o un lenguaje de programación al que no estamos acostumbrados. Como compensación, considero que los buenos planteamientos y el tedioso trabajo empleado se pueden llegar a tener en cuenta.
