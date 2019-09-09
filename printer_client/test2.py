from escpos import *

#dit werkt, opl: https://github.com/python-escpos/python-escpos/issues/230
p = printer.Usb(0x0456,0x0808,0,0x81,0x03)
#p.text("Hello world\n")
p.cut()
p.close()
