import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)

dac    = [8, 11, 7, 1, 0, 5, 12, 6]
comp   = 14
troyka = 13

GPIO.setmode(GPIO.BCM)
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

try:
    while True:
        n = adc()
        volt = n * 3.3 / 256.0
        print("{:.2f} V, ".format(volt), n)

finally:
    GPIO.output(dac, 0)
    GPIO.output(troyka, 0)
    GPIO.cleanup()
