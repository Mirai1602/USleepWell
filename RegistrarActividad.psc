Algoritmo RegistrarActividad
	Dimensionar  dias[7], horasLevantarse[7] 
    Definir i Como Entero
	
    dias[1] <- "Lunes"
    dias[2] <- "Martes"
    dias[3] <- "Mi�rcoles"
    dias[4] <- "Jueves"
    dias[5] <- "Viernes"
    dias[6] <- "S�bado"
    dias[7] <- "Domingo"
	
    Para i <- 1 Hasta 7
        Escribir "�A qu� hora te levantas el ", dias[i], "? (formato HH:MM)"
        Leer horasLevantarse[i]
    FinPara
	Escribir "Resumen de horas de levantarse:"
    Para i <- 1 Hasta 7
        Escribir dias[i], ": ", horasLevantarse[i]
    FinPara


	
FinAlgoritmo
