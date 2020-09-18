import PyPDF2

with open("IPLSchedule.pdf", mode='rb') as f:
    r = PyPDF2.PdfFileReader(f)
    page = r.getPage(0) 
    print(page.extractText())