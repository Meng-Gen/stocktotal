package stocktotal.report;

import java.io.File;
import java.sql.Connection;
import java.sql.DriverManager;
import java.util.HashMap;
import java.util.Map;

import net.sf.jasperreports.engine.JRDataset;
import net.sf.jasperreports.engine.JRParameter;
import net.sf.jasperreports.engine.JasperCompileManager;
import net.sf.jasperreports.engine.JasperExportManager;
import net.sf.jasperreports.engine.JasperFillManager;
import net.sf.jasperreports.engine.JasperPrint;
import net.sf.jasperreports.engine.JasperReport;
import net.sf.jasperreports.engine.design.JRDesignDataset;
import net.sf.jasperreports.engine.design.JRDesignExpression;
import net.sf.jasperreports.engine.design.JRDesignParameter;
import net.sf.jasperreports.engine.design.JasperDesign;
import net.sf.jasperreports.engine.xml.JRXmlLoader;

import org.apache.commons.configuration.XMLConfiguration;
import org.apache.log4j.Logger;

public class ReportGenerator {
	
	public void generate(String stockCode, String[] reportTypes, String configFile) throws Exception {
		this.config = new XMLConfiguration(configFile);		

		logger.info("Prepare jrxml for JasperDesign");
		String designFile = config.getString("report.designFile");
		this.jasperDesign = JRXmlLoader.load(designFile);

		logger.info("Set parameters for sub dataset");
		setDatasetStockCode(stockCode);
		
		logger.info("Compile to JasperReport file");
		jasperReport = JasperCompileManager.compileReport(jasperDesign);
		
		logger.info("Prepare parameters for main report");
		HashMap<String, Object> parameters = new HashMap<String, Object>();
		parameters.put(STOCK_CODE, stockCode);
		
		logger.info("Prepare datasource for main report");
		Connection conn = getConn();
		
		logger.info("Fill report with prepared parameters and datasource");
		JasperPrint jasperPrint = JasperFillManager.fillReport(jasperReport, parameters, conn);

		makeReportDirectory(stockCode);
		
		for (String type : reportTypes) {
			if (type.toUpperCase().equalsIgnoreCase("html")) {
				logger.info("Export to HTML format report");
				JasperExportManager.exportReportToHtmlFile(jasperPrint, getReportFilePath(stockCode, "html"));
			} 
			else if (type.toUpperCase().equalsIgnoreCase("pdf")) {
				logger.info("Export to PDF format report");
				JasperExportManager.exportReportToPdfFile(jasperPrint, getReportFilePath(stockCode, "pdf"));
			}
			else {
				logger.warn(String.format("Cannot support %s format report", type.toUpperCase()));
			}
		}
		
		logger.info("Close datasource connection");
		conn.close();
	}

	private void setDatasetStockCode(String stockCode) throws Exception {
		Map<String, JRDataset> datasetMap = jasperDesign.getDatasetMap();
		Object[] names = datasetMap.keySet().toArray();
		for (Object name : names) {
			JRDesignDataset dataset = (JRDesignDataset)datasetMap.get((String)name);
			
			jasperDesign.removeDataset(dataset);
			
			Map<String, JRParameter> parametersMap = dataset.getParametersMap();
			if (!parametersMap.containsKey(STOCK_CODE)) {
				continue;
			}
			JRDesignParameter stockCodeParameter = (JRDesignParameter)parametersMap.get(STOCK_CODE);
			JRDesignExpression expression = new JRDesignExpression(stockCode);
			stockCodeParameter.setDefaultValueExpression(expression);
			jasperDesign.addDataset(dataset);
		}		
	}
	
	private Connection getConn() throws Exception {
		Class.forName(config.getString("database.driver"));		
		String url = config.getString("database.url");
		String username = config.getString("database.username");
		String password = config.getString("database.password");
		return DriverManager.getConnection(url, username, password);	
	}
	
	private void makeReportDirectory(String stockCode) {
		String reportFilePath = config.getString("report.destFilePathTemplate");
		String reportDir = (new File(reportFilePath)).getParent();
		(new File(reportDir)).mkdir();
	}
	
	private String getReportFilePath(String stockCode, String type) {
		return String.format(config.getString("report.destFilePathTemplate"), stockCode, type);
	}
	
	final static Logger logger = Logger.getLogger(ReportGenerator.class);
	
	private String STOCK_CODE = "STOCK_CODE";
	
	private XMLConfiguration config;
	
	private JasperDesign jasperDesign;
	
	private JasperReport jasperReport; 
}
