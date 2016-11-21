#!/usr/bin/python
import csv
import heapq
import sys
import copy

#constantes
ARG = 2
BRA = 6
PER = 7
VEL = 4000 #km/dia
#N = 14 #el N aca incluye a la ciudad origen
AMSUR = 'AmericaSur'

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
		self.descansos = []
		self.descanso = 0
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
		self.descanso = int(self.distDescanso/3000)
		self.descansos.append(self.descanso)
		if (self.descanso > 0):
			self.distDescanso = self.distDescanso % 3000
		self.tiempoEstadia += 7 + 5* self.descanso

	def eliminarUltimaArista(self):
	#Solo se puede usar una vez, no dos seguidas porque no tengo la informacion de descanso
		arista = self.aristas.pop()
		self.ciudadesVisitadas[arista.destino] = False
		self.tiempoViaje -= (arista.distancia/self.vel)
		if (self.descanso > 0):
			self.distDescanso = self.distDescanso + 3000*self.descanso
		self.distDescanso -= arista.distancia
		self.tiempoEstadia -= 7 + 5* self.descanso
		self.descansos.pop()
		self.descanso = self.descansos[len(self.descansos)-1]
		return arista
	
	def aristaEsPosible(self,arista):
		if (self.ciudadesVisitadas[arista.destino]):
			return False;
		if (self.AmericaSur):
			tiempoLlegada = self.tiempoViaje + (arista.distancia/self.vel) + self.tiempoEstadia
			distDescanso = self.distDescanso + arista.distancia
			descanso = int(distDescanso/3000)
			tiempoSalida = tiempoLlegada + 7 + 5 * descanso
			if (arista.destino == ARG):
				if (tiempoSalida >= 31):
					return False 
			elif (arista.destino == PER):
				if ((tiempoLlegada >= 31 and tiempoLlegada < 59) or ((tiempoSalida >= 31 and tiempoSalida < 59))):
					return False
			elif (arista.destino == BRA):
				if (not(tiempoLlegada >= 31 and tiempoSalida < 59)):
					return False
			elif ((not self.ciudadesVisitadas[ARG]) and tiempoSalida >= 31):
				return False
			elif ((not self.ciudadesVisitadas[BRA]) and tiempoSalida >= 59):
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


	def mostrarTour(self,names):
		distTotal = 0
		i = 0
		print("{}. {}({})".format(i,names[0][0],names[0][1]))
		for arista in self.aristas:
			i += 1
			print("{}. {}({})".format(i,names[arista.destino][0],names[arista.destino][1]))
			distTotal += arista.distancia
		print("Distancia total del tour: {} km".format(distTotal))

	def exportarTour(self,fileName):
		file = open(fileName,'w')
		writer = csv.writer(file,dialect = 'excel')
		writer.writerow([len(self.ciudadesVisitadas)])
		for arista in self.aristas:
			writer.writerow([arista.origen])
		file.close()


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

def cargarNombres(name):
	fileName = 'capitales'+name+'.csv'
	file = open(fileName,'r')
	reader = csv.reader(file,dialect = 'excel')
	reader.next()

	names = {}
	i = 0
	for row in reader:
		names[i] = (row[0],row[1])
		i += 1
	file.close()

	return names

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


#Se recibe como parametro el string correspondiente al continente
def main(argv):
	if (not argv):
		continente = AMSUR
	else:
		continente = argv[0]	
	americaSur = (continente == AMSUR)
	distancias = cargarDistancias(continente)
	nombres = cargarNombres(continente)
	heaps = heapsAristas(distancias)
	heapsAux=copy.deepcopy(heaps)
	tour = Tour(VEL,len(nombres),americaSur)
	
	i = 0
	while (not tour.estaCompleto()):
		if not(heapsAux[i]):
			if(i==0):
				print "NO SE ENCONTRO SOLUCION"
				sys.exit()
			heapsAux[i] = copy.deepcopy(heaps[i])
			aristaElim = tour.eliminarUltimaArista()
			i = aristaElim.origen
			continue
		arista = heapq.heappop(heapsAux[i])
		if (tour.aristaEsPosible(arista)):
			tour.agregarArista(arista)
			i = arista.destino
	tour.cerrarTour(distancias)
	tour.exportarTour("tour.csv")

if __name__ == "__main__":
    main(sys.argv[1:])