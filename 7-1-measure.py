import RPi.GPIO as GPIO
import time
import matplotlib.pyplot as plt

dac    = [8, 11, 7, 1, 0, 5, 12, 6]
led    = [2, 3, 4, 17, 27, 22, 10, 9]
comp   = 14
troyka = 13

GPIO.setmode(GPIO.BCM)
GPIO.setup(dac, GPIO.OUT)
GPIO.setup(led, GPIO.OUT)
GPIO.setup(comp, GPIO.IN)
GPIO.setup(troyka, GPIO.OUT, initial = GPIO.HIGH)

# DEC number to list of 0 and 1 (BIN number)
def dec2bin(value):
    return [int(bit) for bit in bin(value)[2:].zfill(8)]

# Fn returning current voltage
def adc():
    m = 0
    for i in range(7, -1, -1):
        m += 2**i
        GPIO.output(dac, dec2bin(m))
        time.sleep(0.005)
        if (GPIO.input(comp) == 1):
            m -= 2**i
    GPIO.output(led, dec2bin(m))
    volt = m * 3.3 / 256.0
    print("current voltage: ", volt)
    return volt

try:
    data = []
    print("CHARGING")

    start_time = time.time()

    # Charging
    curr_volt = adc()
    while (curr_volt < 2.66):
        data.append(curr_volt)
        curr_volt = adc()

    half_time = time.time()

    print("DISCHARGING")

    GPIO.output(troyka, 0)

    # Discharging
    curr_volt = adc()
    while (curr_volt > 2.27):
        data.append(curr_volt)
        curr_volt = adc()

    end_time = time.time()

    # Counting duration of the experiment
    duration = end_time - start_time

    print("Charging time: ", half_time - start_time, " sec\n", "Discharging time: ", end_time - half_time, " sec")

    data_str = [str(item) for item in data]

    # Writing to the files
    with open("data.txt", "w") as data_file:
        data_file.write("\n".join(data_str))

    with open("settings.txt", "w") as settings_file:
        settings_file.write(str(len(data) / duration) + "\n" + str(3.3 / 256.0))

    # Writing to terminal
    print("Total duration: ", duration)
    print("Period: ", duration / len(data))
    print("Sampling frequency: ", len(data) / duration)
    print("Quantization step: ", 3.3 / 256.0)

    # Graph
    plt.plot(data)
    plt.show()

finally:
    GPIO.output(led, 0)
    GPIO.output(dac, 0)
    GPIO.output(troyka, 0)
    GPIO.cleanup()
