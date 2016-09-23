#!/usr/bin/python
import csv
import math as m
import heapq

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
	def __init__(self,velocidad):
		self.aristas = []
		self.TiempoEstadia = 5
		self.TiempoViaje = 0
		self.vel = velocidad

	def agregarArista(arista):
		self.aristas.append(arista)
		self.TiempoViaje += (arista.distancia/self.vel)
		if (TiempoViaje*self.vel
		self.TiempoEstadia += 5


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

def inicializarCiudades(n):
	ciudadesVisitadas = {}
	for i in range(n):
		ciudadesVisitadas[i] = False
	ciudadesVisitadas[0] = True
	return ciudadesVisitadas	

def cumpleRequisitos(arista,tour,ciudadesVisitadas):
	if (ciudadesVisitadas[arista.destino]):
		return False;
	return True;

def agregarAristaTour(tour,arista):


def verificarTourCompleto(ciudadesVisitadas):
	for ciudad in ciudadesVisitadas:
		if (not ciudadesVisitadas[ciudad]):
			return False
	return True

def mostrarTour(tour):
	ciudades = [0]
	for arista in tour:
		ciudades.append(arista.destino)
	print ciudades

def main():
	ARG = 2
	BRA = 6
	PER = 7
	VEL = 4000
	N = 14 #el N aca incluye a la ciudad origen
	distancias = cargarDistancias('AmericaSur')
	heaps = heapsAristas(distancias)
	tour = Tour(VEL)
	ciudadesVisitadas = inicializarCiudades(N)
	tourCompleto = False
	tiempoEstadia=5
	tiempoViaje =0
	i = 0
	while (not tourCompleto):
		arista = heapq.heappop(heaps[i])
		if (cumpleRequisitos(arista,tour,ciudadesVisitadas)): #verificar otras condiciones
			agregarAristaTour(tour,arista)
			ciudadesVisitadas[arista.destino] = True
			i = arista.destino
			if (verificarTourCompleto(ciudadesVisitadas)):
				tour.append(Arista(arista.destino,0,distancias[arista.destino][0]))
				tourCompleto = True
	mostrarTour(tour)



	

if __name__ == "__main__":
    main()