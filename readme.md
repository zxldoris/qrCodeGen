###python版本
#python 3.6.3

###功能
- 通过cmd输入10位数字，生成条码和二维码，并实时打印生成的pdf

###库
- 用reportlab库生成条码和二维码，并保存到pdf中
- 使用ghostscript、gsprint打印该pdf
- 使用pyinstaller生成.exe文件，在生成.exe时，没有使用-F，如pyinstaller -F xxx.py。在生成后，使用cmd打开该xxx.exe，检查是否提示没有找到库，若是，在程序中导入该库，直至运行正确。

###使用要点
- 需自行设定默认打印机，若默认打印机不可用或者没有打印，检查打印机设置
- 取消勾选打印前预览，可能会导致打印错误