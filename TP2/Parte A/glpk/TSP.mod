# PROBLEMA DEL VIAJANTE
#

#Conjuntos
set CIUDADES;
set CIUDADES_SO;

#Parámetros
param N; # cantidad de ciudades a visitar

param C{i in CIUDADES, j in CIUDADES};

var Y{ i in CIUDADES, j in CIUDADES}, binary; # Si se realiza el trayecto de i a j es igual a 1, sino es igual a 0.

var U{ i in CIUDADES}; # Representa el orden en el que es visitada la ciudad i


minimize total: sum{i in CIUDADES, j in CIUDADES} C[i,j] * Y[i,j];

s.t. bound: sum{i in CIUDADES, j in CIUDADES} C[i,j] * Y[i,j] <= 24670;

s.t. salida{i in CIUDADES}: sum{j in CIUDADES: j!=i } Y[i,j] = 1;

s.t. llegada{j in CIUDADES}: sum{i in CIUDADES: i!=j } Y[i,j] = 1;

s.t. evitarSubTours{i in CIUDADES_SO, j in CIUDADES_SO: i!=j }: U[i] - U[j] + N * Y[i,j] <= N-1;

s.t. rangoOrden{i in CIUDADES_SO}: 1 <= U[i] <= N;

solve;

end;
