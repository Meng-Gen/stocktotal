import os
import sys

class GeneratorManager():

    def __init__(self):
        self.REPORT_WORKING_DIR = './build/release'
        self.PDFBOX_WORKING_DIR = '../../tools'
        self.REPORT_CMDLINE = '''java -jar stocktotal-report.jar -stock %s'''
        self.PDFBOX_CMDLINE = '''java -jar pdfbox-app-1.7.1.jar PDFToImage ../report/StocktotalReport-%s.pdf -imageType png'''
        
    def generate(self, stocks, type):
        for stock in stocks:
            # always generate pdf
            os.chdir(self.REPORT_WORKING_DIR)
            report_cmdline = self.REPORT_CMDLINE % stock
            os.system(report_cmdline)
            
            # convert to other type if necessary
            os.chdir(self.PDFBOX_WORKING_DIR)
            if type in ['png']:
                pdfbox_cmdline = self.PDFBOX_CMDLINE % stock
                print(pdfbox_cmdline)
                os.system(pdfbox_cmdline)
            

            
def main():
    import argparse
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('stocks', metavar='stocks', type=str, nargs='+', help='generate reports for stocks')
    parser.add_argument('-t', '--type', default='pdf', help='set report type: pdf, png')

    args = parser.parse_args()
    assert args.type in ['pdf', 'png']

    m = GeneratorManager()
    m.generate(args.stocks, args.type)


    
if __name__ == '__main__':
    sys.exit(main())
