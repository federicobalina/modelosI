# PROBLEMA DEL VIAJANTE
#

#Conjuntos
set CIUDADES;
set CIUDADES_SO;

#Parámetros
param N; # cantidad de ciudades a visitar
param M1; # número suficientemente grande como para que supere la cantidad de ciudades a visitar
param M2; # número suficientemente grande como para que supere la cantidad de dÃ­as que requiere todo el recorrido
param M3; # número suficientemente grande como para que supere la cantidad máxima de tiempo de estadía en una ciudad
param TEF; # tiempo fijo de estadÃ­a en todas las ciudades
param TD; # Tiempo de descanso
param VEL; # Velocidad constante de traslado
param K0;
param ARG; #indice de país correspondiente a Argentina
param PER; #indice de país correspondiente a Peru
param BRA; #indice de país correspondiente a Brasil

param C{i in CIUDADES, j in CIUDADES};

var Y{ i in CIUDADES, j in CIUDADES}, binary; # Si se realiza el trayecto de i a j es igual a 1, sino es igual a 0.

var W{ i in CIUDADES, j in CIUDADES}, binary; # Si la ciudad i fue visitada antes que la j vale 1, sino 0.
var Z{ i in CIUDADES, j in CIUDADES, k in CIUDADES}, binary; # Es un and de Yij con W ik

var U{ i in CIUDADES}; # Representa el orden en el que es visitada la ciudad i
var TE{ i in CIUDADES} >= 0; # Tiempo de estadia en la ciudad i
var TEA{ i in CIUDADES} >= 0; # Tiempo de estadía acumulado antes de llegar a la ciudad i
var TVA{ i in CIUDADES} >= 0; # Tiempo de viaje acumulado antes de llegar a la ciudad i
var TTA{ i in CIUDADES} >= 0; # Tiempo total acumulado antes de llegar a la ciudad i
var T{ i in CIUDADES, j in CIUDADES}>=0; # Vale TEi si Wij es 1, sino 0.
var D{ i in CIUDADES}; # Representa la cantidad de descansos que debe realizar el equipo en la ciudad i. 
var K{ i in CIUDADES} >= 0, integer; # Representa la cantidad de veces que ya se recorrieron 3000 km antes de llegar a la ciudad i.

var P, binary; # Variable bivalente utilizada solo para el equipo de SudamÃ©rica. Si se visita Perú Antes de Febrero vale 1,
				# si se visita después de Febrero, vale 0


minimize total: sum{i in CIUDADES, j in CIUDADES} C[i,j] * Y[i,j];

s.t. salida{i in CIUDADES}: sum{j in CIUDADES: j!=i } Y[i,j] = 1;

s.t. llegada{j in CIUDADES}: sum{i in CIUDADES: i!=j } Y[i,j] = 1;

s.t. evitarSubTours{i in CIUDADES_SO, j in CIUDADES_SO: i!=j }: U[i] - U[j] + N * Y[i,j] <= N-1;

s.t. rangoOrden{i in CIUDADES_SO}: 1 <= U[i] <= N;

s.t. definicion1W{i in CIUDADES_SO, j in CIUDADES_SO: i!=j}: U[j] <= U[i] + M1 * W[i,j];

s.t. definicion2W{i in CIUDADES_SO, j in CIUDADES_SO: i!=j}: U[i] <= U[j] + M1 * (1 - W[i,j]);

s.t. definicion1Z{i in CIUDADES_SO, j in CIUDADES_SO, k in CIUDADES_SO: i != k}: 2*Z[i,j,k] <= Y[i,j]+W[i,k];  #VER SI HAY QUE DIFERENCIAR I,J,K

s.t. definicion2Z{i in CIUDADES_SO, j in CIUDADES_SO, k in CIUDADES_SO: i != k}: Y[i,j]+W[i,k] <= 1 + Z[i,j,k];

s.t. tiempoViajeAntesDeK{k in CIUDADES_SO}: TVA[k] = sum{j in CIUDADES_SO} ((C[0,j]*Y[0,j])/VEL) + sum{i in CIUDADES_SO, j in CIUDADES_SO: i != k} (C[i,j] * Z[i,j,k] / VEL);

#s.t. definicionK{i in CIUDADES_SO}: 3000 * K[i] = TVA[i] * VEL;

#s.t. definicionK0: K[0] = K0;

#s.t. definicionD{i in CIUDADES_SO}: D[i] = K[i] - K[i-1];

s.t. tiempoEstadiaEnI{i in CIUDADES}: TE[i] = TEF; #+ TD * D[i];

s.t. definicion1T{i in CIUDADES_SO, j in CIUDADES_SO: j != i}: TE[i] - (1-W[i,j])*M3 <= T[i,j];

s.t. definicion2T{i in CIUDADES_SO, j in CIUDADES_SO: j != i}: T[i,j] <= M3 * W[i,j];

s.t. definicion3T{i in CIUDADES_SO, j in CIUDADES_SO: j != i}: 0 <= T[i,j];

s.t. definicion4T{i in CIUDADES_SO, j in CIUDADES_SO: j != i}: T[i,j] <= TE[i];

s.t. tiempoEstadiaAntesDeJ{j in CIUDADES_SO}: TEA[j] == sum{i in CIUDADES: i != j} T[i,j]; 

s.t. tiempoTotalAntesDeJ{j in CIUDADES_SO}: TTA[j] = TEA[j] + TVA[j];

s.t. estadiaArgentina: TTA[ARG] + TE[ARG] <= 31;

s.t. estadiaBrasil1: TTA[BRA] >= 31;

s.t. estadiaBrasil2: TTA[BRA]+TE[BRA] <= 59;

s.t. estadiaPeru1: TTA[PER]+TE[PER] <= 31 + M2*(1-P);

s.t. estadiaPeru2: TTA[PER] >= 59 - M2 * P;

solve;

end;
