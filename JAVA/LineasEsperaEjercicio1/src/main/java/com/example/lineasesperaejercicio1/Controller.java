package com.example.lineasesperaejercicio1;

import javafx.fxml.FXML;
import javafx.scene.chart.BarChart;
import javafx.scene.chart.XYChart;
import javafx.scene.control.TextArea;
import javafx.scene.control.TextField;

import java.util.List;

public class Controller {

    @FXML
    private TextField txtLambda;

    @FXML
    private TextField txtMu;

    @FXML
    private TextField txtClientes;

    @FXML
    private TextArea txtResultados;

    @FXML
    private BarChart<String, Number> chartFrecuencias;

    @FXML
    protected void onSimularButtonClick() {
        try {
            double lambda = Double.parseDouble(txtLambda.getText());
            double mu = Double.parseDouble(txtMu.getText());
            int clientes = Integer.parseInt(txtClientes.getText());

            LineasEspera sim = new LineasEspera(lambda, mu, clientes);
            List<Double> tiempos = sim.simularTiemposEspera();

            StringBuilder sb = new StringBuilder();
            sb.append("Resultados de la Simulación:\n");
            double sumaTiempos = 0;
            for (int i = 0; i < Math.min(tiempos.size(), 20); i++) {
                sb.append(String.format("Cliente %d: Espera = %.2f min\n", (i + 1), tiempos.get(i)));
            }
            for (double t : tiempos) sumaTiempos += t;
            sb.append(String.format("\nTiempo promedio de espera: %.2f min", (sumaTiempos / clientes)));
            txtResultados.setText(sb.toString());

            chartFrecuencias.getData().clear();
            XYChart.Series<String, Number> series = new XYChart.Series<>();
            series.setName("Tiempos de Espera");

            for (int i = 0; i < Math.min(tiempos.size(), 15); i++) {
                series.getData().add(new XYChart.Data<>("C" + (i + 1), tiempos.get(i)));
            }
            chartFrecuencias.getData().add(series);

        } catch (NumberFormatException e) {
            txtResultados.setText("Error: Ingrese valores numéricos válidos.");
        }
    }
}