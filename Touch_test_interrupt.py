import tft_config
import s3lcd
import vga1_8x8 as font
from machine import SPI, Pin
from xpt2046 import Touch
from time import sleep

t_x,t_y = 0,0
def int_handler(x,y):
    global t_x,t_y
    t_x = x
    t_y = y

spi = SPI(1, baudrate=1000000)
spi.init(sck=Pin(01), mosi=Pin(03), miso=Pin(04))
cs = Pin(2, mode=Pin.OUT, value=1) 
int_pin = Pin(9)

try:
    tft = tft_config.config(tft_config.WIDE)
    tft.init()
    tft.clear(s3lcd.BLACK)
    
    width = tft.height()
    height = tft.width()
    print(f'width= {tft.width()}, height= {tft.height()}')
    
    xmin = 150
    xmax = 1830
    ymin = 150
    ymax = 1830
    orientation = 1
    xpt = Touch(spi, cs=cs, int_pin=int_pin, int_handler=int_handler)
    xpt.calibrate(xmin, xmax, ymin, ymax, width, height, orientation)

    tft.fill(s3lcd.WHITE)
    tft.rotation(orientation)
    message = 'Click on the display'
    tft.text(font, message, 25, 25, s3lcd.BLACK, s3lcd.WHITE)
    tft.show()

    while True:
        if xpt.is_touched():
            print(t_x,t_y)
        sleep(0.05)
        
finally:
    tft.deinit()
