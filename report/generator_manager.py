import os
import sys

class GeneratorManager():

    def __init__(self):
        self.REPORT_WORKING_DIR = './build/release'
        self.REPORT_JAR = 'stocktotal-report.jar'

    def generate(self, stocks):
        os.chdir(self.REPORT_WORKING_DIR)
        for stock in stocks:
            cmdline = '''java -jar %s -stock %s''' % (self.REPORT_JAR, stock)
            os.system(cmdline)


        
def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('stocks', metavar='stocks', type=str, nargs='+', help='generate reports for stocks')
    args = parser.parse_args()
    
    m = GeneratorManager()
    m.generate(args.stocks)

        
    
if __name__ == '__main__':
    sys.exit(main())
