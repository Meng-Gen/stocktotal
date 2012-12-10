package stocktotal.report;

import org.apache.log4j.Logger;

public class Program {

	public static void main(String[] args) {
		try {
			ArgParser parser = new ArgParser();
		    parser.parse(args);
		    
		    if (parser.hasHelp()) {
		    	parser.printHelp();
		    	return;
		    }
		    
		    String stock = parser.getStock();
		    String[] types = parser.getTypes();
		    String config = parser.getConfig();
		    
		    logger.info(String.format("Stock: %s", stock));
		    for (String type : types) {
		    	logger.info(String.format("Type: %s", type));
		    }
		    logger.info(String.format("Config: %s", config));

		    ReportGenerator generator = new ReportGenerator();
		    generator.generate(stock, types, config);
		} catch (Exception e) {
			logger.error(e.getMessage(), e);
		}
	}

	final static Logger logger = Logger.getLogger(Program.class);

}
