'''
Game of Simon, for Lilygo T-HMI
Made by Lesept (May 2023)
'''

import tft_config
import s3lcd
import vga1_bold_16x32 as font
from machine import SPI, Pin
from xpt2046 import Touch
from time import sleep
from random import randint

# Touch handler
t_x,t_y = 0,0
def touch_handler(x,y):
    global t_x,t_y
    t_x = x
    t_y = y

# Display the 4 buttons
def displayButtons(cols, radius, xc, yc):
    for i in range(2):
        for j in range(2):
            ncol = j * 2 + i
            tft.fill_circle(xc[i], yc[j], radius + 5, s3lcd.WHITE)
            tft.fill_circle(xc[i], yc[j], radius, cols[ncol])
    tft.show()

# Animate button touch
def animateButton(color, xc, yc, radius):
    tft.fill_circle(xc, yc, radius + 5, s3lcd.WHITE)
    for i in range (int(radius) // 2):
        tft.fill_circle(xc, yc, int(radius) // 2 + i, color)
        tft.show()

# Display
tft = tft_config.config(tft_config.WIDE)
tft.init()
tft.clear(s3lcd.BLACK)
orientation = 0
tft.rotation(orientation)
width = tft.width()
height = tft.height()

# Touch interface
spi = SPI(1, baudrate=1000000)
spi.init(sck=Pin(01), mosi=Pin(03), miso=Pin(04))
cs = Pin(2, mode=Pin.OUT, value=1) 
int_pin = Pin(9)
xpt = Touch(spi, cs=cs, int_pin=int_pin, int_handler=touch_handler)
xpt.calibrate(170, 1842, 139, 1830, 320, 240, 0)

# Game variables
colors = []
score = 0
cols = [s3lcd.GREEN, s3lcd.RED, s3lcd.YELLOW, s3lcd.BLUE]
space = 30
radius = int((width - 3 * space) / 4)
xCenter = [space + radius, width - space - radius]
yCenter = [100, 230]
displayButtons(cols, radius, xCenter, yCenter)
gameOver = False
delay = 0.5

try:
    while not gameOver:
        # Draw new color
        newColor = randint(0, 3)
        colors.append(newColor)
#        print(colors)
        sleep(1)
        
        # Animate buttons
        for color in colors:
            xc = xCenter[color % 2]
            yc = yCenter[color // 2]
            animateButton(cols[color], xc, yc, radius)
            sleep(delay)
        
        # Player's turn
        count = 0
        while count < len(colors):
            # Wait for button touches
            while not xpt.is_touched():
                pass
            button = -1
            # Check if it is correct
            for i in range(4):
                xc = xCenter[i % 2]
                yc = yCenter[i // 2]
                if xc - radius < t_x < xc + radius and yc - radius < t_y < yc + radius:
                    button = i
                    break
            # Animate the button touched
#            print(f'Expected color: {colors[count]} - Button touched is {button}')
            if button != -1:
                animateButton(cols[button], xc, yc, radius)
                # Stop if wrong button
                if colors[count] != button:
                    gameOver = True
                    break
                count += 1

    
    score = len(colors) - 1
    print(f'Score: {score}')
    tft.fill_rect(40, 130, 180, 80, s3lcd.MAGENTA)
    tft.text(font, "GAME OVER", 55, 140, s3lcd.WHITE, s3lcd.MAGENTA)
    text = f'SCORE: {score}'
    tft.text(font, text, 65, 170, s3lcd.WHITE, s3lcd.MAGENTA)
    tft.show()
    sleep(3)

except KeyboardInterrupt:
    pass

tft.clear(s3lcd.BLACK) # Clear display
tft.show()
Pin(38).value(0) # Backlight OFF
tft.deinit()
