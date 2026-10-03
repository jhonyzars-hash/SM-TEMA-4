package com.example.inventarioejercicio2;

import java.util.ArrayList;
import java.util.List;
import java.util.Random;

public class Inventario {
    private int inventarioInicial;
    private int puntoReorden;
    private int cantidadPedido;
    private int diasSimulacion;

    public Inventario(int inventarioInicial, int puntoReorden, int cantidadPedido, int diasSimulacion) {
        this.inventarioInicial = inventarioInicial;
        this.puntoReorden = puntoReorden;
        this.cantidadPedido = cantidadPedido;
        this.diasSimulacion = diasSimulacion;
    }

    public List<Integer> simularInventario() {
        List<Integer> nivelesInventario = new ArrayList<>();
        Random random = new Random();
        int inventarioActual = inventarioInicial;
        int diasParaEntrega = -1;

        for (int dia = 1; dia <= diasSimulacion; dia++) {
            if (diasParaEntrega == 0) {
                inventarioActual += cantidadPedido;
                diasParaEntrega = -1;
            } else if (diasParaEntrega > 0) {
                diasParaEntrega--;
            }

            int demanda = random.nextInt(10);
            inventarioActual = Math.max(0, inventarioActual - demanda);

            if (inventarioActual <= puntoReorden && diasParaEntrega == -1) {
                diasParaEntrega = 2;
            }

            nivelesInventario.add(inventarioActual);
        }

        return nivelesInventario;
    }
}