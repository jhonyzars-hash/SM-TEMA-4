simular_colas <- function(lambda, mu, n_clientes) {
  tiempos_llegada <- rexp(n_clientes, rate = lambda)
  tiempos_servicio <- rexp(n_clientes, rate = mu)
  
  tiempo_llegada_abs <- cumsum(tiempos_llegada)
  tiempo_inicio_servicio <- numeric(n_clientes)
  tiempo_salida <- numeric(n_clientes)
  tiempo_espera <- numeric(n_clientes)
  
  tiempo_inicio_servicio[1] <- tiempo_llegada_abs[1]
  tiempo_espera[1] <- 0
  tiempo_salida[1] <- tiempo_inicio_servicio[1] + tiempos_servicio[1]
  
  if (n_clientes > 1) {
    for (i in 2:n_clientes) {
      tiempo_inicio_servicio[i] <- max(tiempo_llegada_abs[i], tiempo_salida[i - 1])
      tiempo_espera[i] <- tiempo_inicio_servicio[i] - tiempo_llegada_abs[i]
      tiempo_salida[i] <- tiempo_inicio_servicio[i] + tiempos_servicio[i]
    }
  }
  
  return(data.frame(
    Cliente = 1:n_clientes,
    Llegada = tiempo_llegada_abs,
    Espera = tiempo_espera,
    Servicio = tiempos_servicio,
    Salida = tiempo_salida
  ))
}

ejecutar_ejercicio1 <- function(lambda = 2.5, mu = 3.0, n_clientes = 100) {
  if (lambda >= mu) {
    stop("La tasa de llegada (lambda) debe ser menor a la tasa de servicio (mu).")
  }
  
  resultados <- simular_colas(lambda, mu, n_clientes)
  espera_promedio <- mean(resultados$Espera)
  uso_servidor <- (lambda / mu) * 100
  
  cat("=== RESULTADOS SIMULACIÓN DE COLAS (R) ===\n")
  cat(sprintf("Clientes simulados: %d\n", n_clientes))
  cat(sprintf("Uso estimado del servidor: %.1f%%\n", uso_servidor))
  cat(sprintf("Tiempo promedio de espera: %.2f min\n", espera_promedio))
  cat(sprintf("Tiempo máximo de espera: %.2f min\n\n", max(resultados$Espera)))
  
  par(bg = "#1e1e2e", fg = "#cdd6f4", col.axis = "#cdd6f4", col.lab = "#cdd6f4", col.main = "#89b4fa")
  
  muestras <- head(resultados$Espera, 25)
  barplot(
    muestras,
    names.arg = 1:length(muestras),
    col = "#89b4fa",
    border = NA,
    main = "Tiempo de Espera por Cliente (Primeros 25)",
    xlab = "Cliente",
    ylab = "Tiempo de Espera (min)"
  )
  grid(nx = NA, ny = NULL, col = "#45475a", lty = "dotted")
}

ejecutar_ejercicio1(lambda = 2.5, mu = 3.0, n_clientes = 100)