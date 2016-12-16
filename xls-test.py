import xlwt
#from datetime import datetime

#style0 = xlwt.easyxf('font: name Times New Roman, color-index red, bold on',
#    num_format_str='#,##0.00')
#style1 = xlwt.easyxf(num_format_str='D-MMM-YY')

#wb = xlwt.Workbook()
#ws = wb.add_sheet('Tweets', cell_overwrite_ok=True)


names = ['Μαρία','Ελένη']


for i, name in enumerate(names):
    wb = xlwt.Workbook(i)
    namedec = name.decode('utf-8')
    
    ws = wb.add_sheet(namedec)
    
    ws.write(0, 0, namedec)

    wb.save('example%s.xls' % namedec)
    

