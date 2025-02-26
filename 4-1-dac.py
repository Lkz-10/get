import RPi.GPIO as GPIO

dac = [8, 11, 7, 1, 0, 5, 12, 6]

GPIO.setmode(GPIO.BCM)

GPIO.setup(dac, GPIO.OUT)

def decimal2binary(value):
    return [int(bit) for bit in bin(value)[2:].zfill(8)]

def isint(s):
    try:
        int(s)
        return True
    except ValueError:
        return false

try:
    while (True):
        num = input("Введите число от 0 до 255: ")

        if num == 'q':
            break

        if (not num.isdigit()):
            print("Введите целое положительное число!")
            continue

        if 0 <= int(num) <= 255:

            out_val = decimal2binary(int(num))
        
            GPIO.output(dac, out_val)

            u = 0
            for i in range(8):
                u += 3.3 / 2**(i+1) * out_val[i]

            print("Предполагаемое напряжение: ", u, " В")

        else:
            print("Необходимо число от 0 до 255!")

finally:
    GPIO.output(dac, 0)
    GPIO.cleanup()
