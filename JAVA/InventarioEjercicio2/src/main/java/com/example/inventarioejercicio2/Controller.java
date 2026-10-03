package com.example.inventarioejercicio2;

import javafx.fxml.FXML;
import javafx.scene.chart.LineChart;
import javafx.scene.chart.XYChart;
import javafx.scene.control.TextArea;
import javafx.scene.control.TextField;

import java.util.List;

public class Controller {

    @FXML
    private TextField txtInicial;

    @FXML
    private TextField txtReorden;

    @FXML
    private TextField txtPedido;

    @FXML
    private TextField txtDias;

    @FXML
    private TextArea txtResultados;

    @FXML
    private LineChart<String, Number> chartInventario;

    @FXML
    protected void onSimularButtonClick() {
        try {
            int inicial = Integer.parseInt(txtInicial.getText());
            int reorden = Integer.parseInt(txtReorden.getText());
            int pedido = Integer.parseInt(txtPedido.getText());
            int dias = Integer.parseInt(txtDias.getText());

            Inventario sim = new Inventario(inicial, reorden, pedido, dias);
            List<Integer> niveles = sim.simularInventario();

            StringBuilder sb = new StringBuilder();
            sb.append("Simulación de Inventario:\n");
            for (int i = 0; i < Math.min(niveles.size(), 15); i++) {
                sb.append(String.format("Día %d: %d unid. | ", (i + 1), niveles.get(i)));
                if ((i + 1) % 3 == 0) sb.append("\n");
            }
            txtResultados.setText(sb.toString());

            chartInventario.getData().clear();
            XYChart.Series<String, Number> series = new XYChart.Series<>();
            series.setName("Comportamiento del Stock");

            for (int i = 0; i < niveles.size(); i++) {
                series.getData().add(new XYChart.Data<>("D" + (i + 1), niveles.get(i)));
            }
            chartInventario.getData().add(series);

        } catch (NumberFormatException e) {
            txtResultados.setText("Error: Ingrese valores enteros válidos.");
        }
    }
}