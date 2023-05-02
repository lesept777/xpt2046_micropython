import tft_config
import s3lcd
import vga1_8x8 as font
from machine import SPI, Pin
from xpt2046 import Touch
from time import sleep

spi = SPI(1, baudrate=1000000)
spi.init(sck=Pin(01), mosi=Pin(03), miso=Pin(04))
cs = Pin(2, mode=Pin.OUT, value=1) 
int_pin = Pin(9)

try:
    tft = tft_config.config(tft_config.WIDE)
    tft.init()
    tft.clear(s3lcd.BLACK)
    orientation = 0
    tft.rotation(orientation)
    
    width = tft.width()
    height = tft.height()
    print(f'width= {tft.width()}, height= {tft.height()}')
    
    xpt = Touch(spi, cs=cs, int_pin=int_pin)

    if orientation%2 == 1:
        # Touch upper left corner
        tft.fill(s3lcd.WHITE)    
        tft.line(2,2,2,20,s3lcd.BLACK)
        tft.line(2,2,20,2,s3lcd.BLACK)
        tft.line(2,2,20,20,s3lcd.BLACK)
        message = 'click here'
        tft.text(font, message, 25, 25, s3lcd.BLACK, s3lcd.WHITE)
        tft.show()

        while not xpt.is_touched():
            pass
        x1, y1 = xpt.raw_touch()
        sleep(1)
        
        # Touch lower right corner
        tft.fill(s3lcd.WHITE)    
        tft.line(width-2,height-2,width-2,height-20,s3lcd.BLACK)
        tft.line(width-2,height-2,width-20,height-2,s3lcd.BLACK)
        tft.line(width-2,height-2,width-20,height-20,s3lcd.BLACK)
        message = 'click here'
        tft.text(font, message, width-105, height-35, s3lcd.BLACK, s3lcd.WHITE)
        tft.show()

        while not xpt.is_touched():
            pass
        x2, y2 = xpt.raw_touch()

    else:
        # Touch upper right corner
        tft.fill(s3lcd.WHITE)    
        tft.line(width-2,2,width-2,20,s3lcd.BLACK)
        tft.line(width-2,2,width-20,2,s3lcd.BLACK)
        tft.line(width-2,2,width-20,20,s3lcd.BLACK)
        message = 'click here'
        tft.text(font, message, width-105, 25, s3lcd.BLACK, s3lcd.WHITE)
        tft.show()

        while not xpt.is_touched():
            pass
        x1, y1 = xpt.raw_touch()
        sleep(1)
        
        # Touch lower left corner
        tft.fill(s3lcd.WHITE)    
        tft.line(2,height-2,2,height-20,s3lcd.BLACK)
        tft.line(2,height-2,20,height-2,s3lcd.BLACK)
        tft.line(2,height-2,20,height-20,s3lcd.BLACK)
        message = 'click here'
        tft.text(font, message, 25, height-35, s3lcd.BLACK, s3lcd.WHITE)
        tft.show()

        while not xpt.is_touched():
            pass
        x2, y2 = xpt.raw_touch()

    # Compute calibration
    print('Put this line into your code:')
    xpt.calibrate(x2, y2, y1, x1, height, width, orientation)
    print(f'xpt.calibrate({x2}, {y2}, {y1}, {x1}, {height}, {width}, {orientation})')
    
    # Testing
    print('\nTesting: CTRL C to quit')
    tft.fill(s3lcd.WHITE)
    message = 'Click on the display'
    tft.text(font, message, width//2 - 70, height//2 - 15, s3lcd.BLUE, s3lcd.WHITE)
    message = 'CTRL C to quit'
    tft.text(font, message, width//2 - 50, height//2 + 15, s3lcd.BLUE, s3lcd.WHITE)
    tft.show()

    while True:
        x, y = xpt.get_touch(True)
        
        if xpt.is_touched():
            print(f'x={x}, y={y}')
            tft.rect(x, y, 2, 2, s3lcd.RED)
            tft.show()
        sleep(0.1)

except KeyboardInterrupt:
    pass

finally:
    tft.clear(s3lcd.BLACK) # Clear display
    tft.show()
    Pin(38).value(0) # Backlight OFF
    tft.deinit()