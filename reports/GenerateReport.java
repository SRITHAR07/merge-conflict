import net.sf.jasperreports.engine.*;
import java.sql.Connection;
import java.sql.DriverManager;
import java.util.HashMap;
import java.util.Map;

public class GenerateReport {
    public static void main(String[] args) {
        if (args.length < 3) {
            System.out.println("Error: Missing required arguments (Plantcode, Shiftcode, Status).");
            return;
        }

        String plantcode = args[0].trim();
        String shiftcode = args[1].trim();
        String status = args[2].trim();

        try {
            String dbUrl = "jdbc:mysql://localhost:3306/gennhr";
            String dbUsername = "root";
            String dbPassword = "sri123";

            Connection connection = DriverManager.getConnection(dbUrl, dbUsername, dbPassword);

            String jasperReportPath = "new.jrxml";
            JasperReport jasperReport = JasperCompileManager.compileReport(jasperReportPath);

            Map<String, Object> parameters = new HashMap<>();
            parameters.put("Plantcode", plantcode.equals("ALL") ? "" : plantcode);
            parameters.put("Shiftcode", shiftcode.equals("ALL") ? "" : shiftcode);
            parameters.put("Status", status.equals("ALL") ? "" : status);

            JasperPrint jasperPrint = JasperFillManager.fillReport(jasperReport, parameters, connection);

            String outputHtmlPath = "output/generated_report.html";
            JasperExportManager.exportReportToHtmlFile(jasperPrint, outputHtmlPath);

            System.out.println("Report generated successfully at " + outputHtmlPath);
        } catch (Exception e) {
            System.out.println("Error generating report:");
            e.printStackTrace();
        }
    }
}



// javac -cp ".;D:/gtn/reports/jasperreports-6.20.0.jar;D:/gtn/reports/mysql-connector-j-8.0.33.jar;D:/gtn/reports/commons-logging-1.2.jar;D:/gtn/reports/commons-digester-2.1.jar;D:/gtn/reports/commons-collections4-4.4.jar;D:/gtn/reports/commons-beanutils-1.9.4.jar" GenerateReport.java


// java -cp ".;D:/gtn/reports/jasperreports-6.20.0.jar;D:/gtn/reports/mysql-connector-j-8.0.33.jar;D:/gtn/reports/commons-logging-1.2.jar;D:/gtn/reports/commons-digester-2.1.jar;D:/gtn/reports/commons-collections4-4.4.jar;D:/gtn/reports/commons-beanutils-1.9.4.jar" GenerateReport

