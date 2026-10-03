validar_simulador <- function(mu_0, n, media, std) {
  error_estandar <- std / sqrt(n)
  
  if (error_estandar == 0) {
    t_stat <- 0
  } else {
    t_stat <- (media - mu_0) / error_estandar
  }
  
  return(t_stat)
}

ejecutar_ejercicio3 <- function(mu_0 = 50.0, n = 30, media = 51.2, std = 3.5) {
  t_calc <- validar_simulador(mu_0, n, media, std)
  t_critico <- 2.045
  pasa_prueba <- abs(t_calc) <= t_critico
  
  cat("=== EVALUACIÓN PRUEBA T DE STUDENT (R) ===\n")
  cat(sprintf("Valor t Calculado: %.3f\n", t_calc))
  cat(sprintf("Valor t Crítico: ±%.3f\n\n", t_critico))
  
  cat("--- DICTAMEN ---\n")
  if (pasa_prueba) {
    cat("RESULTADO: ACEPTADO\n")
    cat("El simulador es confiable y no presenta diferencias significativas.\n\n")
  } else {
    cat("RESULTADO: RECHAZADO\n")
    cat("El simulador difiere de la media teórica esperada.\n\n")
  }
  
  par(bg = "#11111b", fg = "#cdd6f4", col.axis = "#cdd6f4", col.lab = "#cdd6f4", col.main = "#f38ba8")
  
  set.seed(123)
  datos <- rnorm(n, mean = media, sd = std)
  
  plot(
    1:n, datos,
    col = "#f38ba8",
    pch = 19,
    cex = 1.2,
    main = "Distribución de Muestras vs Valor Teórico (R)",
    xlab = "Número de Muestra",
    ylab = "Valor Generado"
  )
  grid(nx = NULL, ny = NULL, col = "#313244", lty = "dotted")
  abline(h = mu_0, col = "#89b4fa", lty = 2, lwd = 2)
  legend("topright", legend = c("Muestras", sprintf("Media Teórica (%.1f)", mu_0)),
         col = c("#f38ba8", "#89b4fa"), pch = c(19, NA), lty = c(NA, 2),
         bg = "#1e1e2e", box.col = "#45475a", text.col = "#cdd6f4", cex = 0.8)
}

ejecutar_ejercicio3(mu_0 = 50.0, n = 30, media = 51.2, std = 3.5)