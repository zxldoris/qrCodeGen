from reportlab.pdfgen import canvas
from reportlab.graphics.barcode import code128, code39, code93, usps, ecc200datamatrix
from reportlab.graphics.barcode import qr, usps4s
from reportlab.graphics.shapes import Drawing
from reportlab.graphics import renderPDF
import re
import time
import win32api
import win32print
import os

f = open("configure.txt")
configure = f.read()
currentprinter_regex = re.compile('CurrentPrinter="(.*?)"')
currentprinter = re.search(currentprinter_regex, configure).group(1)
qr_str_regex = re.compile('QR-Prefix="(.*?)"')
QR_Prefix = re.search(qr_str_regex, configure).group(1)
f.close()

def createBarCodes(c, barcode_value):
    # 条码生成
    barcode128 = code128.Code128(barcode_value)
    barcode128.barWidth = 1.1
    barcode128.drawOn(c, -7.15, 15)
    # 字符添加
    c.setFont('Helvetica-Bold', 9,)
    c.drawString(35, 3, barcode_value)
    # 二维码生成
    qrstr = QR_Prefix + barcode_value
    qr_code = qr.QrCodeWidget(qrstr)
    bounds = qr_code.getBounds()
    width = bounds[2] - bounds[0]
    height = bounds[3] - bounds[1]
    d = Drawing(45, 40, transform=[45. / (width-15), 0, 0, 45. / (height-15), 0, 0])
    d.add(qr_code)
    renderPDF.draw(d, c, 60, 33)
    # 添加图片
    c.drawImage('.\img\img.jpg', 12.85, 40)


if __name__ == '__main__':
    while True:
        # 输入判断
        while True:
            v = input("请刷卡：")
            regex_c = re.compile('^\\d{10}$')
            m = re.match(regex_c, v)
            if m:
                barcode_value = m.group(0)
                break
            else:
                print("wrong input")
                continue
        fname = 'p' + str(barcode_value) + '.pdf'
        c = canvas.Canvas(fname, pagesize=(114, 85))
        # 保存日志: 编号 时间
        # 获取时间
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
        string = barcode_value + '\t\t' + t
        with open('log.txt', 'a+') as f:
            f.write(string + '\n')
        createBarCodes(c, barcode_value)
        c.showPage()
        c.save()

        GHOSTSCRIPT_PATH = "GHOSTSCRIPT\\bin\\gswin32.exe"
        GSPRINT_PATH = "GSPRINT\\gsprint.exe"
        loc = ".\\"  # 当前文件夹
        x = 0
        for file in os.listdir(loc):
            if file.endswith('.pdf') and file != '':
                string = '-ghostscript "' + GHOSTSCRIPT_PATH + \
                         '" -printer "' + currentprinter + '" ' + file
                win32api.ShellExecute(0, 'open', GSPRINT_PATH, string, '.', 0)
                print('printing file >> ' + str(file))
                x = x + 1
                time.sleep(1)
                os.remove(fname)
