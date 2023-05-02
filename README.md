# xpt2046_micropython
Micropython drive for XPT2046 touch, especially for Lilygo T-HMI device

For T-HMI, use the firmware from [russhughes](https://github.com/russhughes/s3lcd/tree/c666663ea9ce005ca8271c470c389054274f0192/firmware/S3LCD_OCT_16M)

This driver is based on the original version from [rdagger](https://github.com/rdagger/micropython-ili9341/blob/d080d5bac95c0da972b26e3599f56bb0311d9ebd/xpt2046.py). The calibration is quite simple (and can be improved in the future).

# Methods
First, a SPI bus must be created.
```
spi = SPI(1, baudrate=1000000)
spi.init(sck=Pin(01), mosi=Pin(03), miso=Pin(04))
cs = Pin(2, mode=Pin.OUT, value=1) 
```

## init
Declare the touch device
```
xpt = Touch(spi, cs=cs, int_pin=int_pin)
```
