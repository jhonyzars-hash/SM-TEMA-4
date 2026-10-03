simular_inventario <- function(inicial, reorden, pedido, dias) {
  niveles <- numeric(dias)
  stock <- inicial
  dias_entrega <- -1
  
  for (d in 1:dias) {
    if (dias_entrega == 0) {
      stock <- stock + pedido
      dias_entrega <- -1
    } else if (dias_entrega > 0) {
      dias_entrega <- dias_entrega - 1
    }
    
    demanda <- sample(0:9, 1)
    stock <- max(0, stock - demanda)
    
    if (stock <= reorden && dias_entrega == -1) {
      dias_entrega <- 2
    }
    
    niveles[d] <- stock
  }
  
  return(niveles)
}

ejecutar_ejercicio2 <- function(inicial = 50, reorden = 15, pedido = 30, dias = 30) {
  niveles <- simular_inventario(inicial, reorden, pedido, dias)
  
  cat("=== RESUMEN CONTROL DE INVENTARIO (R) ===\n")
  cat(sprintf("Días simulados: %d\n", dias))
  cat(sprintf("Stock mínimo registrado: %d unidades\n", min(niveles)))
  cat(sprintf("Stock máximo registrado: %d unidades\n", max(niveles)))
  cat(sprintf("Stock promedio: %.1f unidades\n\n", mean(niveles)))
  
  cat("--- DETALLE PRIMEROS 15 DÍAS ---\n")
  for (i in 1:min(15, dias)) {
    cat(sprintf("Día %d: %d unidades\n", i, niveles[i]))
  }
  
  par(bg = "#1e1e2e", fg = "#cdd6f4", col.axis = "#cdd6f4", col.lab = "#cdd6f4", col.main = "#a6e3a1")
  
  plot(
    1:dias, niveles,
    type = "o",
    col = "#a6e3a1",
    pch = 19,
    lwd = 2,
    main = "Evolución del Stock Diario (R)",
    xlab = "Día",
    ylab = "Unidades en Stock"
  )
  grid(nx = NULL, ny = NULL, col = "#313244", lty = "dotted")
  abline(h = reorden, col = "#f38ba8", lty = 2, lwd = 1.5)
}

ejecutar_ejercicio2(inicial = 50, reorden = 15, pedido = 30, dias = 30)