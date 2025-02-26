import RPi.GPIO as GPIO
GPIO.setwarnings(False)

GPIO.setmode(GPIO.BCM)

n = 10

GPIO.setup(n, GPIO.OUT)

p = GPIO.PWM(n, 1000)
p.start(0)

try:
    while True:
        dc = int(input("Введите коэффициент заполнения: "))
        p.ChangeDutyCycle(dc)
        print("Напряжение: ", 3.3 * dc / 100)

finally:
    p.stop()
    GPIO.output(n, 0)
    GPIO.cleanup()
