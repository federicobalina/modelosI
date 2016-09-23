//Constantes
 int N = 13; // cantidad de ciudades a visitar
 int M1 = 13; // número suficientemente grande como para que supere la cantidad de ciudades a visitar
 int M2 = 150; // número suficientemente grande como para que supere la cantidad de días que requiere todo el recorrido
 int TEF = 7; // tiempo fijo de estadía en todas las ciudades
 int TD = 3; // Tiempo de descanso
 int VEL = 167; // Velocidad constante de traslado
 int K0 = 0;

 /*{string} Ciudades = { "BuenosAires", "Sucre", "Brasilia", "Santiago", "Bogota", "Quito", "Georgetown", "Asuncion", 
 						"Lima", "Paramaribo", "Montevideo", "Caracas" };*/
 			
 range ciudades = 1..N;
 range sinOrigen = 2..N;
 		
// Costo (en este caso distancia) para ir desde i hasta j.	
 //SheetConnection fue lo mas cerca que encontre a cargar CSV, pero no lo reconoce
 
 //SAQUE LAS ISLAS MALVINAS
 float C[1..N][1..N] = 
 [[1882.76,1902.92,2277.82,2938.89,3694.22,4094.55,4741.25,6048.67,6455.33,6325.87,6413.76,6512.26,6977.30],
  [203.69,0.00,1138.40,1038.83,1862.78,2341.92,3141.36,4363.31,4666.14,4447.13,4518.82,4609.80,5100.06],
  [1341.54,1138.40,0.00,1552.69,1693.29,3013.15,2471.21,3789.63,4253.32,4689.42,4672.96,4671.89,4908.78],
  [1070.24,1038.83,1552.69,0.00,1050.35,1464.23,2516.18,3581.78,3774.24,3413.84,3480.11,3573.80,4108.26],
  [1974.31,1862.78,1693.29,1050.35,0.00,1875.12,1481.96,2544.95,2803.55,3020.47,2984.58,2979.02,3290.96],
  [2274.62,2341.92,3013.15,1464.23,1875.12,0.00,3169.20,3779.89,3667.78,2355.86,2538.75,2755.00,3593.55],
  [3297.44,3141.36,2471.21,2516.18,1481.96,3169.20,0.00,1324.95,1882.01,3323.17,3135.37,2960.01,2747.75],
  [4497.95,4363.31,3789.63,3581.78,2544.95,3779.89,1324.95,0.00,730.81,2968.08,2682.26,2392.85,1756.31],
  [4774.69,4666.14,4253.32,3774.24,2803.55,3667.78,1882.01,730.81,0.00,2412.97,2100.82,1780.03,1029.16],
  [4444.34,4447.13,4689.42,3413.84,3020.47,2355.86,3323.17,2968.08,2412.97,0.00,331.68,678.30,1719.56],
  [4531.92,4518.82,4672.96,3480.11,2984.58,2538.75,3135.37,2682.26,2100.82,331.68,0.00,346.63,1388.62],
  [4638.95,4609.80,4671.89,3573.80,2979.02,2755.00,2960.01,2392.85,1780.03,678.30,346.63,0.00,1043.71],
  [5169.92,5100.06,4908.78,4108.26,3290.96,3593.55,2747.75,1756.31,1029.16,1719.56,1388.62,1043.71,0.00]];
 
 
//Variables de decisión
dvar boolean Y[ciudades][ciudades]; // Si se realiza el trayecto de i a j es igual a 1, sino es igual a 0.
dvar boolean W[ciudades][ciudades]; // Si la ciudad i fue visitada antes que la j vale 1, sino 0.
dvar boolean Z[ciudades][ciudades][ciudades]; // Es un and de Yij con W ij

dvar int+ U[ciudades]; // Representa el orden en el que es visitada la ciudad i
dvar int+ TE[ciudades]; // Tiempo de estadía en la ciudad i
dvar int+ TEA[ciudades]; // Tiempo de estadía acumulado antes de llegar a la ciudad i
dvar int+ TVA[ciudades]; // Tiempo de viaje acumulado antes de llegar a la ciudad i
dvar int+ TTA[ciudades]; // Tiempo total acumulado antes de llegar a la ciudad i
dvar int+ D[ciudades]; // Representa la cantidad de descansos que debe realizar el equipoen la ciudad i. 
dvar int+ K[ciudades]; // Representa la cantidad de veces que ya se recorrieron 3000kmantes de llegar a la ciudad i.

dvar boolean P; // Variable bivalente utilizada solo para el equipo de Sudamérica. Si se visita Perú Antes de Febrero vale 1,
				// si se visita después de Febrero, vale 0

//Funcional
 minimize 
 	sum(i in ciudades, j in ciudades: j != i) 
 		C[i][j] * Y[i][j];
 	
 	
//Restricciones
subject to 
{
	Salida: 
	sum(i in ciudades: i != 0)
		Y[i][1] == 1;
	
	Entrada: 
	sum(j in ciudades: j != 0)
		Y[1][j] == 1;
	
	EvitarSubTours: 
	forall (i in sinOrigen, j in sinOrigen: j != i)
		U[i] - U[j] + N * Y[i][j] <= N - 1;
		
	RangoDelOrden:
	forall(i in sinOrigen)	
		2 <= U[i] <= N;
		
	Ecuacion1W: 
	forall(i in sinOrigen, j in sinOrigen: i != j)
		U[j] <= U[i] + M1 * W[i][j];
	
	Ecuacion2W:
	forall(i in sinOrigen, j in sinOrigen: i != j)
		U[i] <= U[j] + M1 * (1 - W[i][j]);
		
	TiempoEstadiaEnI:
	forall(i in ciudades)
		TE[i] >= TEF + TD * D[i];
	
/*TiempoEstadiaAntesDeI: // REVEER. En el informe decia TEA[j] = TEi * Wij, con i = 0 y variando j en el rango sinOrigen
							//Me suena raro el i fijo
	forall(j in sinOrigen: j != 1)
	  TEA[j] == sum(j in sinOrigen) TE[1] * W[1][j];						
	
	/*DefinicionZ: // En 1 sola ecuación creo que tiraba error
	forall(i in sinOrigen, j in sinOrigen, k in sinOrigen)
		2 * Z[i][j][k] <= Y[i][j] + W[i][k];
		
	forall(i in sinOrigen, j in sinOrigen, k in sinOrigen)
		Y[i][j] + W[i][k] <= 1 + Z[i][j][k];*/
		
	/*TiempoViajeAntesCiudadK:
	forall(k in sinOrigen)
	  TVA[k] == (sum(j in sinOrigen) (C[1][j]/VEL) * Y[1][j])
	  			+ (sum(i in sinOrigen, j in sinOrigen) (C[i][j]/VEL) * Z[i][j][k]);*/
		
	TiempoTotalAntesDeCiudadJ:
	forall(j in sinOrigen)
		TTA[j] == TEA[j] + TVA[j];
	  
	DefinicionKi:
	forall(i in sinOrigen)
		3000 * K[i] == TVA[i] * VEL;
		
	DefinicionDi:
	forall(i in sinOrigen)
		D[i] == K[i] - K[i - 1];
		
	EstadiaArgentina: //ver indice de argentina. Creo que en verdad habria que definir con strings las ciudades como deje comentado arriba
					  // pero si se puede subir el csv, no se como será cargar los strings tmb del csv.
	//Suponiendo indice 2 a argentina
	TTA[2] + TE[2] <= 31;
	
	EstadiaBrasil:
	//Suponiendo indice 6
	TTA[6] >= 31; // o 32?
	TTA[6] <= 59; //o 60?
	
	EstadiaPeru:
	//Suponiendo indice 7 - cambiar dsp al si se arma las distancias a mano
	TTA[7] + TE[7] <= 31 + M2 * (1 - P);
	TTA[7] >= 59 - M2 * P;
}