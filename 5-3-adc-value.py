import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)

led    = [2, 3, 4, 17, 27, 22, 10, 9]
dac    = [8, 11, 7, 1, 0, 5, 12, 6]
comp   = 14
troyka = 13

GPIO.setmode(GPIO.BCM)
GPIO.setup(led, GPIO.OUT)
GPIO.setup(dac, GPIO.OUT)
GPIO.setup(troyka, GPIO.OUT, initial = GPIO.HIGH)
GPIO.setup(comp, GPIO.IN)

def dec2bin(value):
    return [int(bit) for bit in bin(value)[2:].zfill(8)]

def adc():
    for i in range(256):
        GPIO.output(dac, dec2bin(i))
        time.sleep(0.005)
        if (GPIO.input(comp) == 1):
            return i
    return 0

# def adc():
#     m = 0
#     for i in range(7, -1, -1):
#         m += 2**i
#         GPIO.output(dac, dec2bin(m))
#         time.sleep(0.005)
#         if (GPIO.input(comp) == 1):
#             m -= 2**i
#     return m

def Volume(val):
    val = int(val*10/256)
    arr = [0]*8
    for i in range(val - 1):
        arr[i] = 1
    return arr

try:
    while True:
        n = adc()
        volt = n * 3.3 / 256.0
        vol = Volume(n)
        GPIO.output(led, vol)
        print("{:.2f} V, volume = ".format(volt), int(n/256*10))


finally:
    GPIO.output(led, 0)
    GPIO.output(dac, 0)
    GPIO.output(troyka, 0)
    GPIO.cleanup()
