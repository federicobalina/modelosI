#!/usr/bin/python

import csv
from heuristica import cargarDistancias,cargarNombres,Arista,Tour
import sys

#CONSTANTES
VEL = 4000.0 #km/dia
ARG = 2
BRA = 6
PER = 7
AMSUR = 'AmericaSur'

class Tour(object):
	def __init__(self,n):
		self.aristas = []
		self.ordenCiudades = []
		self.ciudadesVisitadas = {}
		self.distRecorrida = 0
		for i in range(n):
			self.ciudadesVisitadas[i] = False
		self.ciudadesVisitadas[0] = True
		self.n = n

	def agregarArista(self,arista):
		self.aristas.append(arista)
		self.ciudadesVisitadas[arista.destino] = True
		self.distRecorrida += arista.distancia
		self.ordenCiudades.append(arista.destino)

	def intercambiarCiudades(self,a,b,distancias):
		#print a,b #
		ordenA = self.ordenCiudades.index(a)
		ordenB = self.ordenCiudades.index(b)
		
		if (abs(ordenA-ordenB) != 1): #Si las ciudades no tienen una arista entre ellas
			aristaLlegadaA = self.aristas[ordenA]
			aristaSalidaA = self.aristas[ordenA+1]
			aristaLlegadaB = self.aristas[ordenB]
			aristaSalidaB = self.aristas[ordenB+1]

			distanciaVieja = aristaLlegadaA.distancia + aristaSalidaA.distancia + aristaLlegadaB.distancia + aristaSalidaB.distancia
			nuevaAristaLlegadaB = Arista(aristaLlegadaA.origen,b,distancias[aristaLlegadaA.origen][b])
			nuevaAristaSalidaB = Arista(b,aristaSalidaA.destino,distancias[b][aristaSalidaA.destino])
			nuevaAristaLlegadaA = Arista(aristaLlegadaB.origen,a,distancias[aristaLlegadaB.origen][a])
			nuevaAristaSalidaA = Arista(a,aristaSalidaB.destino,distancias[a][aristaSalidaB.destino])
			distanciaNueva = nuevaAristaLlegadaB.distancia + nuevaAristaSalidaB.distancia + nuevaAristaLlegadaA.distancia + nuevaAristaSalidaA.distancia
			self.aristas[ordenA] = nuevaAristaLlegadaB
			self.aristas[ordenA+1] = nuevaAristaSalidaB
			self.aristas[ordenB] = nuevaAristaLlegadaA
			self.aristas[ordenB+1] = nuevaAristaSalidaA
		else: #Si las ciudades tienen una arista entre ellas
			if( ordenA < ordenB ):
				minOrden = ordenA
				arista1 = self.aristas[ordenA]#LlegadaA
				arista2 = self.aristas[ordenA+1]#SalidaA=LlegadaB
				arista3 = self.aristas[ordenB+1]#SalidaB
				nuevaArista1 = Arista(arista1.origen,b,distancias[arista1.origen][b])
				nuevaArista2 = Arista(arista2.destino,arista2.origen,arista2.distancia)
				nuevaArista3 = Arista(a,arista3.destino,distancias[a][arista3.destino])
			else:
				minOrden = ordenB
				arista1 = self.aristas[ordenB]#LlegadaB
				arista2 = self.aristas[ordenB+1]#SalidaB=LlegadaA
				arista3 = self.aristas[ordenA+1]#SalidaA
				nuevaArista1 = Arista(arista1.origen,a,distancias[arista1.origen][a])
				nuevaArista2 = Arista(arista2.destino,arista2.origen,arista2.distancia)
				nuevaArista3 = Arista(b,arista3.destino,distancias[b][arista3.destino])
			self.aristas[minOrden] = nuevaArista1
			self.aristas[minOrden+1] = nuevaArista2
			self.aristas[minOrden+2] = nuevaArista3 #CHECKEAR casos limite
			distanciaVieja = arista1.distancia + arista2.distancia + arista3.distancia
			distanciaNueva = nuevaArista1.distancia + nuevaArista2.distancia + nuevaArista3.distancia

		self.ordenCiudades[ordenA] = b
		self.ordenCiudades[ordenB] = a
		self.distRecorrida += ( distanciaNueva - distanciaVieja )

	def invertirArista(self,arista):
		return Arista(arista.destino,arista.origen,arista.distancia)

	def intercambiarCaminos(self,e1,e2,distancias):
		arista1 = self.aristas[e1]
		arista2 = self.aristas[e2]
		distanciaVieja = arista1.distancia + arista2.distancia
		nuevaArista1 = Arista(arista1.origen,arista2.origen,distancias[arista1.origen][arista2.origen]) 
		nuevaArista2 = Arista(arista1.destino,arista2.destino,distancias[arista1.destino][arista2.destino])
		distanciaNueva = nuevaArista1.distancia + nuevaArista2.distancia
		#Caminos
		self.aristas[e1] = nuevaArista1
		self.aristas[e2] = nuevaArista2
		aristasAux = []
		for e in range(1,e2-e1):
			aristasAux.append(self.invertirArista(self.aristas[e2-e]))
		for e in range(1,e2-e1):
			self.aristas[e1+e] = aristasAux[e-1] 
		#Distancia
		self.distRecorrida += (distanciaNueva - distanciaVieja)
		#OrdenCiudades
		ciudadesAux = []
		for i in range(1,e2-e1+1):
			#print e2,e1,i
			ciudadesAux.append(self.ordenCiudades[e2-i])
		for i in range(0,e2-e1):
			self.ordenCiudades[e1+i] = ciudadesAux[i]

	def verificarVentanas(self):
		tiempoEstadia=7
		tiempoViaje=0
		distDescanso=0
		descanso=0
		for arista in self.aristas: #Se asume que el origen no puede tener una ventana requerida
			destino = arista.destino
			tiempoViaje += (arista.distancia/VEL)
			tiempoLlegada = tiempoViaje + tiempoEstadia
			distDescanso += arista.distancia
			descanso = int(distDescanso/3000)
			if (descanso > 0):
				distDescanso = distDescanso % 3000
			tiempoEstadia += 7 + 5 * descanso
			tiempoSalida = tiempoViaje + tiempoEstadia
			if ( destino == ARG ):
				if (tiempoSalida >= 31):
					return False
			if ( destino == BRA  ): #No restrinjo la entrada a Brasil si es la ultima ciudad, en caso de necesitarlo, espero lo que haga falta
				if ( (tiempoSalida >= 59) or ( (tiempoLlegada < 31) and (self.ordenCiudades[len(self.ordenCiudades)-1] != BRA) ) ):
					return False
			if ( destino == PER ):
				if ((tiempoLlegada >= 31 and tiempoLlegada < 59) or ((tiempoSalida >= 31 and tiempoSalida < 59))):
					return False
		return True

	def estaCompleto(self):
		for ciudad in self.ciudadesVisitadas:
			if (not self.ciudadesVisitadas[ciudad]):
				return False
		return True

	def cerrarTour(self,distancias):
		ultimaArista =self.aristas[len(self.aristas)-1]
		arista = Arista(ultimaArista.destino,0,distancias[ultimaArista.destino][0])
		self.aristas.append(arista)
		self.distRecorrida += arista.distancia

	def mostrarTour(self,names):
		distTotal = 0
		i = 0
		print("{}. {}({})".format(i,names[0][0],names[0][1]))
		for arista in self.aristas:
			i += 1
			print("{}. {}({})".format(i,names[arista.destino][0],names[arista.destino][1]))
			distTotal += arista.distancia
		print("Distancia total del tour: {} km".format(distTotal))


def cargarTour(fileName,distancias):
	file = open(fileName,'r')
	reader = csv.reader(file,dialect = 'excel')
	n = int(reader.next()[0])
	tour = Tour(n)
	origen = int(reader.next()[0])
	for row in reader:
		destino = int(row[0])
		dist = distancias[origen][destino]
		arista = Arista(origen,destino,dist)
		tour.agregarArista(arista)
		origen = destino
	file.close()
	tour.cerrarTour(distancias)

	return tour

def generarIntercambiosPosiblesCiudades(n):
	intercambiosPosibles=[]
	for i in range(1,n):
		for j in range(i+1,n):
			intercambiosPosibles.append((i,j))
	return intercambiosPosibles

def kIntercambiosCiudades(tour,distancias,names,ventanas=False):
	intercambiosPosibles = generarIntercambiosPosiblesCiudades(tour.n)
	
	while len(intercambiosPosibles) > 0:
		(a,b) = intercambiosPosibles.pop()
		ordenA = tour.ordenCiudades.index(a)
		ordenB = tour.ordenCiudades.index(b)
		aristas=[]
		nuevasAristas=[]
		if (abs(ordenA-ordenB) != 1):
			aristas.append(tour.aristas[ordenA]) #aristaLlegadaA
			aristas.append(tour.aristas[ordenA+1]) #aristaSalidaA
			aristas.append(tour.aristas[ordenB]) #aristaLlegadaB
			aristas.append(tour.aristas[ordenB+1]) #aristaSalidaB 
			nuevasAristas.append(Arista(aristas[0].origen,b,distancias[aristas[0].origen][b])) #nuevaAristaLlegadaB
			nuevasAristas.append(Arista(b,aristas[1].destino,distancias[b][aristas[1].destino])) #nuevaAristaSalidaB
			nuevasAristas.append(Arista(aristas[2].origen,a,distancias[aristas[2].origen][a])) #nuevaAristaLlegadaA
 			nuevasAristas.append(Arista(a,aristas[3].destino,distancias[a][aristas[3].destino])) #nuevaAristaSalidaA
		else:
			if( ordenA < ordenB ):
				aristas.append(tour.aristas[ordenA])#LlegadaA
				aristas.append(tour.aristas[ordenB+1])#SalidaB
				nuevasAristas.append(Arista(aristas[0].origen,b,distancias[aristas[0].origen][b]))
				nuevasAristas.append(Arista(a,aristas[1].destino,distancias[a][aristas[1].destino]))
			else:
				aristas.append(tour.aristas[ordenB])#LlegadaB
				aristas.append(tour.aristas[ordenA+1])#SalidaA
				nuevasAristas.append(Arista(aristas[0].origen,a,distancias[aristas[0].origen][a]))
				nuevasAristas.append(Arista(b,aristas[1].destino,distancias[b][aristas[1].destino]))
		distanciaVieja = sum(item.distancia for item in aristas)
		distanciaNueva = sum(item.distancia for item in nuevasAristas)
		if ( distanciaNueva < distanciaVieja ):
			tour.intercambiarCiudades(a,b,distancias)
			if( (ventanas) and (not tour.verificarVentanas() )):
				tour.intercambiarCiudades(a,b,distancias) #deshago el cambio
				continue
			tour.mostrarTour(names)#
			intercambiosPosibles = generarIntercambiosPosiblesCiudades(tour.n)

def generarIntercambiosPosiblesCaminos(n):
	intercambiosPosibles = []
	for i in range (n):
		for j in range (i+1,n):
			intercambiosPosibles.append((i,j))
	return intercambiosPosibles

def kIntercambiosCaminos(tour,distancias,names,ventanas=False):
	intercambiosPosibles = generarIntercambiosPosiblesCaminos(len(tour.aristas))
	#e1 es anterior a e2
	while (len(intercambiosPosibles) > 0):
		(e1,e2) = intercambiosPosibles.pop()
		arista1 = tour.aristas[e1]
		arista2 = tour.aristas[e2]
		distanciaVieja = arista1.distancia + arista2.distancia
		nuevaArista1 = Arista(arista1.origen,arista2.origen,distancias[arista1.origen][arista2.origen]) 
		nuevaArista2 = Arista(arista1.destino,arista2.destino,distancias[arista1.destino][arista2.destino])
		distanciaNueva = nuevaArista1.distancia + nuevaArista2.distancia
		if ( distanciaNueva < distanciaVieja ):
			tour.intercambiarCaminos(e1,e2,distancias)
			if( (ventanas) and (not tour.verificarVentanas() )):
				tour.intercambiarCaminos(e1,e2,distancias) #deshago el cambio
				continue
			tour.mostrarTour(names)#
			intercambiosPosibles = generarIntercambiosPosiblesCaminos(len(tour.aristas))


def main(argv):
	if (not argv):
		continente = AMSUR
	else:
		continente = argv[0]
	ventanas=True
	distancias = cargarDistancias(continente)
	nombres = cargarNombres(continente)
	tour = cargarTour("tour.csv",distancias)
	
	tour.mostrarTour(nombres)
	kIntercambiosCaminos(tour,distancias,nombres,ventanas)

if __name__ == "__main__":
    main(sys.argv[1:])


