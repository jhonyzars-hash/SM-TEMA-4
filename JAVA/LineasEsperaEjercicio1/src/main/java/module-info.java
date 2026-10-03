module com.example.lineasesperaejercicio1 {
    requires javafx.controls;
    requires javafx.fxml;

    opens com.example.lineasesperaejercicio1 to javafx.fxml;
    exports com.example.lineasesperaejercicio1;
}