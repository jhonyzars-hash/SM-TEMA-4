package com.example.lineasesperaejercicio1;

import java.util.ArrayList;
import java.util.List;
import java.util.Random;

public class LineasEspera {
    private double lambda;
    private double mu;
    private int totalClientes;

    public LineasEspera(double lambda, double mu, int totalClientes) {
        this.lambda = lambda;
        this.mu = mu;
        this.totalClientes = totalClientes;
    }

    public List<Double> simularTiemposEspera() {
        List<Double> tiemposEspera = new ArrayList<>();
        Random random = new Random();
        double tiempoActual = 0;
        double tiempoSalidaAnterior = 0;

        for (int i = 0; i < totalClientes; i++) {
            double tiempoEntreLlegada = -Math.log(1 - random.nextDouble()) / lambda;
            tiempoActual += tiempoEntreLlegada;

            double tiempoServicio = -Math.log(1 - random.nextDouble()) / mu;

            double inicioServicio = Math.max(tiempoActual, tiempoSalidaAnterior);
            double tiempoEspera = inicioServicio - tiempoActual;

            tiemposEspera.add(tiempoEspera);
            tiempoSalidaAnterior = inicioServicio + tiempoServicio;
        }

        return tiemposEspera;
    }
}