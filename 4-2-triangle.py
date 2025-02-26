import RPi.GPIO as GPIO
import time

dac = [8, 11, 7, 1, 0, 5, 12, 6]

GPIO.setmode(GPIO.BCM)

GPIO.setup(dac, GPIO.OUT)

def decimal2binary(value):
    return [int(bit) for bit in bin(value)[2:].zfill(8)]

x = 0
inc = True

try:
    period = float(input("Введите период: "))

    while (True):
        GPIO.output(dac, decimal2binary(x))

        if (x == 0): inc = True
        elif (x == 255): inc = False

        if (inc): x += 1
        else: x -= 1

        print(x, " ")

        time.sleep(period/512)

except ValueError:
    print("Неправильно введен период!")

finally:
    GPIO.output(dac, 0)
    GPIO.cleanup()
