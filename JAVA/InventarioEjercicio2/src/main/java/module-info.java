module com.example.inventarioejercicio2 {
    requires javafx.controls;
    requires javafx.fxml;

    opens com.example.inventarioejercicio2 to javafx.fxml;
    exports com.example.inventarioejercicio2;
}