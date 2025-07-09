Algoritmo RutinaSleep
	Dimensionar dias[7], horasLevantarse[7], horasDormir[7] 
    Definir i, hora, minuto, totalMinutos, dormirHora, dormirMinuto Como Entero
	
    dias[0] <- "Lunes"
    dias[1] <- "Martes"
    dias[2] <- "Miércoles"
    dias[3] <- "Jueves"
    dias[4] <- "Viernes"
    dias[5] <- "Sábado"
    dias[6] <- "Domingo"
	
    Para i <- 1 Hasta 7
        Escribir "¿A qué hora te levantas el ", dias[i], "? (HH:MM)"
        Leer horasLevantarse[i]
		
        // Separar hora y minuto
        hora = ConvertirAEntero(horasLevantarse[i], 0, 2)
        minuto = ConvertirAEntero(horasLevantarse[i], 3, 2)
		
        totalMinutos <- hora * 60 + minuto
        totalMinutos <- totalMinutos - (5 * 90)  // Restar 5 ciclos de 90 min
		
        Si totalMinutos < 0 Entonces
            totalMinutos <- totalMinutos + 1440  // Ajustar si pasa a día anterior
        FinSi
		
        dormirHora <- trunc(totalMinutos / 60)
        dormirMinuto <- totalMinutos MOD 60
		
        horasDormir[i] <- ConvertirATexto(dormirHora) + ":" + ConvertirATexto(dormirMinuto)
		
        Escribir "?? El ", dias[i], " deberías dormir a las ", horasDormir[i]
    FinPara

	
	
FinAlgoritmo
