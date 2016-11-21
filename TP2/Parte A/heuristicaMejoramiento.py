#!/usr/bin/python

import csv
from heuristica import cargarDistancias,cargarNombres,Arista,Tour
import sys

#CONSTANTES
VEL = 4000 #km/dia
AMSUR = 'AmericaSur'

def cargarTour(fileName,distancias,AmSur):
	file = open(fileName,'r')
	reader = csv.reader(file,dialect = 'excel')
	n = reader.next()
	tour = Tour(VEL,int(n[0]),AmSur)
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

def main(argv):
	if (not argv):
		continente = AMSUR
	else:
		continente = argv[0]	
	americaSur = (continente == AMSUR)
	distancias = cargarDistancias(continente)
	nombres = cargarNombres(continente)
	tour = cargarTour("tour.csv",distancias,americaSur)
	tour.mostrarTour(nombres)


if __name__ == "__main__":
    main(sys.argv[1:])


