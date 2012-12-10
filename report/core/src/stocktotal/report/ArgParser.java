package stocktotal.report;

import org.apache.commons.cli.CommandLine;
import org.apache.commons.cli.CommandLineParser;
import org.apache.commons.cli.GnuParser;
import org.apache.commons.cli.HelpFormatter;
import org.apache.commons.cli.Option;
import org.apache.commons.cli.OptionBuilder;
import org.apache.commons.cli.Options;
import org.apache.commons.cli.ParseException;

public class ArgParser {
    
    @SuppressWarnings("static-access")
    public ArgParser() {
        Option help = new Option("h", "print this message");
        help.setLongOpt("help");
        
        Option stock = OptionBuilder.withArgName("stockCode")
                .hasArg()
                .withDescription("set stock code")
                .create("s");
        stock.setLongOpt("stock");
        
        Option type = OptionBuilder.withArgName("types")
                .hasArgs()
                .withDescription("set report types (default: pdf)")
                .create("t");
        type.setLongOpt("type");
        
        Option config = OptionBuilder.withArgName("file")
                .hasArg()
                .withDescription("use given file for config (default: ReportGenerator.config)")
                .create("c");
        config.setLongOpt("config");
        
        this.options = new Options();
        options.addOption(help);
        options.addOption(stock);
        options.addOption(type);
        options.addOption(config);
        
        this.parser = new GnuParser();
    }
    
    public void parse(String[] args) throws ParseException {
        this.cmdline = this.parser.parse(this.options, args);
    }
    
    public boolean hasHelp() {
        return cmdline.hasOption("help");
    }
    
    public void printHelp() {
        HelpFormatter formatter = new HelpFormatter();
        formatter.printHelp("java -jar stocktotal-report.jar", options);
    }
    
    public String getStock() {
        assert this.cmdline != null;
        return cmdline.hasOption("stock") ? cmdline.getOptionValue("stock") : null;
    }
    
    public String[] getTypes() {
        assert this.cmdline != null;
        return cmdline.hasOption("type") ? cmdline.getOptionValues("type") : new String[] { "PDF" } ;
    }
    
    public String getConfig() {
        assert this.cmdline != null;
        return cmdline.getOptionValue("config", "ReportGenerator.config");
    }    

    private Options options;
    
    private CommandLineParser parser;
    
    private CommandLine cmdline;
}
