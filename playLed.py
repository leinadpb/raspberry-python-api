import RPi.GPIO as GPIO
import settings
from random import randrange
import time

# GPIO
## Common
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False) # GPIO

## Red LED
GPIO.setup(settings.red_led_pin, GPIO.OUT)
GPIO.setup(settings.blue_led_pin, GPIO.OUT)
GPIO.setup(settings.green_led_pin, GPIO.OUT)


# LEDs
red = GPIO.PWM(settings.red_led_pin, 50)
blue = GPIO.PWM(settings.blue_led_pin, 50)
green = GPIO.PWM(settings.green_led_pin, 50)

red.start(100)
blue.start(40)
green.start(20)

d = 0
while True:
    d = randrange(101)
    red.ChangeDutyCycle(d)
    d = randrange(101)
    blue.ChangeDutyCycle(d)
    d = randrange(101)
    green.ChangeDutyCycle(d)
    time.sleep(0.4)
