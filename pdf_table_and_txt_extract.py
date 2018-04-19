import io
import os
import tabula
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage

def convert_pdf_to_txt(path, filename):
    filepath = path+'\\'+filename
    rsrcmgr = PDFResourceManager()
    retstr = io.StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    fp = open(filepath, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 0
    caching = True
    pagenos = set()

    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages,
                                  password=password,
                                  caching=caching,
                                  check_extractable=True):
        interpreter.process_page(page)

    text = retstr.getvalue()

    fp.close()
    device.close()
    retstr.close()

    file = open(path+'\\'+filename.replace(".pdf", "")+'\\'+filename.replace(".pdf", ".txt"), 'w', encoding='utf8')
    file.write(text)
    file.close()

def extract_table_from_pdf(path, filename):
    # PDF into CSV
    tabula.convert_into(path+'\\'+filename, path+'\\'+filename.replace(".pdf", "")+'\\'+filename.replace(".pdf", ".csv"), output_format='csv')

if __name__ == '__main__':
    dir_path = input("Директория с PDF файлами (без \ в конце): ")
    filename = [x for x in os.listdir(dir_path) if x.endswith(".pdf")]

    for x in filename:
        os.mkdir(x.replace(".pdf", ""))
        convert_pdf_to_txt(dir_path, x)
        extract_table_from_pdf(dir_path, x)
