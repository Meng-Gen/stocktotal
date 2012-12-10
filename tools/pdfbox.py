import os
import sys

def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('stocks', metavar='stocks', type=str, nargs='+', help='convert pdf to image for stocks')
    args = parser.parse_args()
    
    REPORT_DIR = '../report/report'
    REPORT_PDF_FILENAME = '''StocktotalReport-%s.pdf'''
    CMDLINE = '''java -jar ./pdfbox/pdfbox-app-1.7.1.jar PDFToImage %s -imageType png'''
    
    for stock in args.stocks:
        src_file = os.path.join(REPORT_DIR, REPORT_PDF_FILENAME % stock)
        cmdline = CMDLINE % src_file
        os.system(cmdline)

        

if __name__ == '__main__':
    sys.exit(main())
