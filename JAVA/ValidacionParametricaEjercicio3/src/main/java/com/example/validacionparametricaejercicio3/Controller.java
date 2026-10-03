package com.example.validacionparametricaejercicio3;

import javafx.fxml.FXML;
import javafx.scene.chart.NumberAxis;
import javafx.scene.chart.ScatterChart;
import javafx.scene.chart.XYChart;
import javafx.scene.control.TextArea;
import javafx.scene.control.TextField;

import java.util.List;

public class Controller {

    @FXML
    private TextField txtMediaTeorica;

    @FXML
    private TextField txtDesviacion;

    @FXML
    private TextField txtMuestra;

    @FXML
    private TextArea txtResultados;

    @FXML
    private ScatterChart<Number, Number> chartScatter;

    @FXML
    protected void onValidarButtonClick() {
        try {
            double mediaTeorica = Double.parseDouble(txtMediaTeorica.getText());
            double desviacion = Double.parseDouble(txtDesviacion.getText());
            int n = Integer.parseInt(txtMuestra.getText());

            ValidacionParametrica val = new ValidacionParametrica(mediaTeorica, desviacion, n);
            List<Double> muestra = val.generarMuestraSimulada();
            double mediaObtenida = val.calcularMedia(muestra);
            double tCalculado = val.calcularEstadisticoT(muestra, mediaObtenida);

            StringBuilder sb = new StringBuilder();
            sb.append("--- RESULTADOS DE VALIDACIÓN PARAMÉTRICA ---\n");
            sb.append(String.format("Media Teórica (H0): %.2f\n", mediaTeorica));
            sb.append(String.format("Media Muestral Obtenida: %.4f\n", mediaObtenida));
            sb.append(String.format("Estadístico t-Calculado: %.4f\n\n", tCalculado));
            if (Math.abs(tCalculado) < 1.96) {
                sb.append("CONCLUSIÓN: No se rechaza H0. El simulador está validado.");
            } else {
                sb.append("CONCLUSIÓN: Se rechaza H0. El simulador difiere de la teoría.");
            }
            txtResultados.setText(sb.toString());

            chartScatter.getData().clear();
            XYChart.Series<Number, Number> series = new XYChart.Series<>();
            series.setName("Muestras Simuladas");

            for (int i = 0; i < muestra.size(); i++) {
                series.getData().add(new XYChart.Data<>(i + 1, muestra.get(i)));
            }
            chartScatter.getData().add(series);

        } catch (NumberFormatException e) {
            txtResultados.setText("Error: Ingrese valores numéricos válidos.");
        }
    }
}