#!/usr/bin/python
import csv
import heapq
import sys

#constantes
ARG = 2
BRA = 6
PER = 7
VEL = 4000 #km/dia
N = 14 #el N aca incluye a la ciudad origen

class Arista(object):
	def __init__(self,origen,destino,distancia):
		self.origen = origen
		self.destino = destino
		self.distancia = distancia

	def __cmp__(self,otro): #Definida con el proposito de utilizar el heapq (min heap)
		if self.distancia < otro.distancia:
			return -1
		if self.distancia >= otro.distancia:
			return 1
		return 0

class Tour(object):
	def __init__(self,velocidad,n,AmericaSur = True):
		self.aristas = []
		self.tiempoEstadia = 7
		self.tiempoViaje = 0
		self.vel = velocidad
		self.distDescanso = 0
		self.ciudadesVisitadas = {}
		for i in range(n):
			self.ciudadesVisitadas[i] = False
		self.ciudadesVisitadas[0] = True
		self.AmericaSur = AmericaSur

	def agregarArista(self,arista):
		self.aristas.append(arista)
		self.ciudadesVisitadas[arista.destino] = True
		self.tiempoViaje += (arista.distancia/self.vel)
		self.distDescanso += arista.distancia
		descanso = int(self.distDescanso/3000)
		if (descanso > 0):
			self.distDescanso = self.distDescanso % 3000
		self.tiempoEstadia += 7 + 5* descanso

	def aristaEsPosible(self,arista):
		if (self.ciudadesVisitadas[arista.destino]):
			return False;
		if (self.AmericaSur):
			tiempoLlegada = self.tiempoViaje + (arista.distancia/self.vel) + self.tiempoEstadia
			distDescanso = self.distDescanso + arista.distancia
			descanso = int(distDescanso/3000)
			tiempoSalida = tiempoLlegada + 7 + 5 * descanso
			if (arista.destino == ARG):
				if (tiempoSalida > 31):
					return False 
			elif (arista.destino == PER):
				if (tiempoLlegada > 31 and tiempoSalida <= 59):
					return False
			elif (arista.destino == BRA):
				if (not(tiempoLlegada > 31 and tiempoSalida <= 59)):
					return False
		return True;

	def estaCompleto(self):
		for ciudad in self.ciudadesVisitadas:
			if (not self.ciudadesVisitadas[ciudad]):
				return False
		return True

	def cerrarTour(self,distancias):
		ultimaArista =self.aristas[len(self.aristas)-1]
		arista = Arista(ultimaArista.destino,0,distancias[ultimaArista.destino][0])
		self.aristas.append(arista)
		self.tiempoViaje += (arista.distancia/self.vel)


	def mostrarTour(self):
		ciudades = [0]
		for arista in self.aristas:
			ciudades.append(arista.destino)
		print ciudades



def cargarDistancias(name):
	fileName = 'distancias'+name+'.csv'
	file = open(fileName,'r')
	reader = csv.reader(file,dialect = 'excel')

	distances = []
	for row in reader:
		dist = []
		for i in range(len(row)):
			dist.append(float(row[i]))
		distances.append(dist)
	file.close()

	return distances

def heapsAristas(distancias):
	heaps = []
	i = 0
	for fil in distancias:
		heap = []
		j = 0
		for d in fil:
			if (i != j):
				arista = Arista(i,j,d)
				heapq.heappush(heap,arista)
			j+=1
		heaps.append(heap)
		i += 1
	return heaps

def main():
	distancias = cargarDistancias('AmericaSur')
	heaps = heapsAristas(distancias)
	tour = Tour(VEL,N)
	i = 0
	while (not tour.estaCompleto()):
		tour.mostrarTour();
		if not(heaps[i]):
			print "NO SE ENCONTRO SOLUCION"
			sys.exit()
		arista = heapq.heappop(heaps[i])
		if (tour.aristaEsPosible(arista)): #verificar otras condiciones
			tour.agregarArista(arista)
			i = arista.destino
	tour.cerrarTour(distancias)
	tour.mostrarTour()



	

if __name__ == "__main__":
    main()