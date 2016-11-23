#!/usr/bin/python
import csv
import math as m
from decimal import Decimal

class prettyfloat(float):
    def __repr__(self):
        return "%0.2f" % self

def main():
	continente = 'AmericaSurBis'
	fileName = 'capitales'+continente+'.csv'
	file = open(fileName,'r')
	reader = csv.reader(file,dialect = 'excel')
	reader.next() #Salteo etiquetas

	cities = []
	for row in reader:
		lat = float(row[2].replace(',','.'))*(m.pi/180)
		lon = float(row[3].replace(',','.'))*(m.pi/180)
		cities.append((lat,lon))
	file.close()

	diametroTierra = 6378.137
	distancias = []
	for city1 in cities:
		dist = []
		for city2 in cities:
			if (city1 == city2):
				d=0.0
			else:
				lat1 = city1[0]
				lat2 = city2[0]
				lon1 = city1[1]
				lon2 = city2[1]
				d = diametroTierra * m.acos( m.cos(lat1) * m.cos(lat2) * m.cos(lon2-lon1) + m.sin(lat1) * m.sin(lat2) )
			#dist.append(d)
			dist.append(Decimal("%.2f" % d))
		distancias.append(dist)

	fileName = 'distancias'+continente+'.csv'
	file = open(fileName,'w')
	writer = csv.writer(file,dialect = 'excel')

	writer.writerows(distancias)
	#print [map(prettyfloat,x) for x in distancias]
	file.close()

if __name__ == "__main__":
    main()
