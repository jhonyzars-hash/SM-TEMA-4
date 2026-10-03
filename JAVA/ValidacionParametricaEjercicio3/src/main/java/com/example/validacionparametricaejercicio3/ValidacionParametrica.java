package com.example.validacionparametricaejercicio3;

import java.util.ArrayList;
import java.util.List;
import java.util.Random;

public class ValidacionParametrica {
    private double mediaTeorica;
    private double desviacionEstandar;
    private int tamanoMuestra;

    public ValidacionParametrica(double mediaTeorica, double desviacionEstandar, int tamanoMuestra) {
        this.mediaTeorica = mediaTeorica;
        this.desviacionEstandar = desviacionEstandar;
        this.tamanoMuestra = tamanoMuestra;
    }

    public List<Double> generarMuestraSimulada() {
        List<Double> muestra = new ArrayList<>();
        Random random = new Random();
        for (int i = 0; i < tamanoMuestra; i++) {
            double valor = mediaTeorica + random.nextGaussian() * desviacionEstandar;
            muestra.add(valor);
        }
        return muestra;
    }

    public double calcularMedia(List<Double> muestra) {
        double suma = 0;
        for (double v : muestra) suma += v;
        return suma / muestra.size();
    }

    public double calcularEstadisticoT(List<Double> muestra, double mediaObtenida) {
        double sumaCuadrados = 0;
        for (double v : muestra) {
            sumaCuadrados += Math.pow(v - mediaObtenida, 2);
        }
        double varianzaMuestral = sumaCuadrados / (muestra.size() - 1);
        double desviacionMuestral = Math.sqrt(varianzaMuestral);
        return (mediaObtenida - mediaTeorica) / (desviacionMuestral / Math.sqrt(muestra.size()));
    }
}