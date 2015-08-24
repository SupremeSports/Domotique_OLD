import RPi.GPIO as GPIO
import time

LED = 33

GPIO.setwarnings(False)

GPIO.setmode(GPIO.BOARD)
GPIO.setup(LED, GPIO.OUT)

while True:
        GPIO.output(LED, True)
        time.sleep(0.1)
        GPIO.output(LED, False)
        time.sleep(0.1)