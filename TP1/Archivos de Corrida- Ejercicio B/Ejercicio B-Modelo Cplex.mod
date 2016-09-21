//Constantes
 dvar float+ DINERO_DISPONIBLE;
 dvar float+ SEGUNDOS_TV_DISPONIBLES;
 dvar float+ CANTIDAD_PUBLICISTAS;
 dvar float+ CANTIDAD_PRINCIPALES_CAPITALES;
 
//Variables
dvar float+ TV; // cantidad de segundos de publicidad en televisión contratados
dvar float+ GR; // cantidad de gráficas contratadas en unidades
dvar float+ EV; // cantidad de eventos contratados en unidades

dvar float+ P; // cantidad de personas que mirararán la serie gracias a la campaña publicitaria, en unidades

dvar float+ CST; // costos de la contratación de las distintas actividades de publicidad, en dolares

 
//Funcional
 maximize 
 	P;
 	
//Restricciones
subject to 
{
	//Inicialización de constantes
	DINERO_DISPONIBLE == 10000000;
	SEGUNDOS_TV_DISPONIBLES == 1000;
	CANTIDAD_PUBLICISTAS == 300;
	CANTIDAD_PRINCIPALES_CAPITALES == 194;
	
	//Recursos Disponibles
	SegundosDisponibles: TV <= SEGUNDOS_TV_DISPONIBLES;
	DineroDisponible: CST <= DINERO_DISPONIBLE;
	Publicistas: (GR / 20) + (TV / 100) + EV <= CANTIDAD_PUBLICISTAS;
	
	//1 Grafica por capital
	GraficasMinimas: GR >= CANTIDAD_PRINCIPALES_CAPITALES;
	
	//Atraccion de Espectadores
	Espectadores: P == TV * 50 + GR * 150 + EV * 800;
	
	//Costos
	Costos: CST == TV * 5000 + GR * 20000 + EV * 100000;
	
}