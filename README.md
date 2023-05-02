# xpt2046_micropython
## Micropython drive for XPT2046 touch, especially for Lilygo T-HMI device

For T-HMI, use the firmware from [russhughes](https://github.com/russhughes/s3lcd/tree/c666663ea9ce005ca8271c470c389054274f0192/firmware/S3LCD_OCT_16M). 

Flashing instructions: Place device into flash mode by pressing and holding the BOOT button, then press and release the RESET button and finally release the BOOT button.

### Erase flash

On Linux:
```
esptool.py --chip esp32s3 --port /dev/ttyACM0 erase_flash
```
On Windows:
```
./python.exe -u -m esptool --chip esp32s3 --port COM27 erase_flash
```

### Flash firmware

On Linux:
```
esptool.py --chip esp32s3 --port /dev/ttyACM0 write_flash -z 0 firmware.bin
```
On Windows:
```
/python.exe -u -m esptool --chip esp32s3 --port COM27 --baud 460800 write_flash -z 0x0 firmware.bin
```
Finalyy, unplug and plug the device.

*This driver is based on the original version from [rdagger](https://github.com/rdagger/micropython-ili9341/blob/d080d5bac95c0da972b26e3599f56bb0311d9ebd/xpt2046.py). The calibration is quite simple (and can be improved in the future).*

# Methods
First, a SPI bus must be created.
```
from machine import SPI, Pin
spi = SPI(1, baudrate=1000000)
spi.init(sck=Pin(01), mosi=Pin(03), miso=Pin(04))
cs = Pin(2, mode=Pin.OUT, value=1) 
```

## init
Declare the touch device
```
xpt = Touch(spi, cs=cs, int_pin=int_pin)
```
The `int_pin` argument is mandatory. For T-HMI, use:
```
int_pin = Pin(9)
```

## calibrate
Arguments are: xmin, xmax, ymin, ymax, width, height, orientation. Use the `Calibration.py` script to get the values. On my T-HMI device, I found that
```
    xmin = 150
    xmax = 1830
    ymin = 150
    ymax = 1830
```
are fairly good. Then:
```
    xpt = Touch(spi, cs=cs, int_pin=int_pin)
    xpt.calibrate(xmin, xmax, ymin, ymax, width, height, orientation)
```
Note that here, width is the `largest` value and `height` is the lowest one. So, *independently of the orientation of the display*, on the T-HMI 320 x 240 display, you have either:
```
xpt.calibrate(150, 1830, 150, 1830, 320, 240, 0)
```
or
```
xpt.calibrate(150, 1830, 150, 1830, 320, 240, 1)
```

## get_touch
Provides the x and y coordinates using the display reference. The origin is in the upper left corner.
```
x, y = xpt.get_touch()
```
This method can only be used after calling the `calibrate()` method. Depending on the calibration accuracy, it can provide negative coordinates or coordinates higher than the size of the display. An optional argument is used to clip the provided values to the display size:
```
x, y = xpt.get_touch(True)
```

## is_touched()
Returns `True` if the display was touched or `False` otherwise.

## set_orientation()
Used to change the orientation of the display. Argument values are the same as russhugjes's:

Index | Rotation
----- | --------
0     | Portrait (0 degrees)
1     | Landscape (90 degrees)
2     | Reverse Portrait (180 degrees)
3     | Reverse Landscape (270 degrees)

## raw_touch
Provides the raw values from the device, without any reference to the display size. The origin is in the lower right corner. This is only used in the calibration script, but you may not want to use it.
```
x, y = xpt.raw_touch()
```

# Examples
## Calibration.py
Use this to get the calibration values for your touch device. Change the orientation value in line 17 as desired.

## Touch_test.py
A simple example of how to use the driver. It is based on calibration values for my T-HMI: change the lines 22-25 accroding to the values provided by the above script.

## Touch_test_interrupt.py
Similar but using the interrupt to get the coordinates.

