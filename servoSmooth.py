import RPi.GPIO as GPIO
import asyncio
import settings
import time 

# GPIO
## Common
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(settings.servo_pin, GPIO.OUT)

servoMotor = GPIO.PWM(settings.servo_pin, 50) # 50 = 50Hz pulse

duty = 2  # 0 degress


waitTime = 0.33

def smooth90DegreesMovement():
    servoMotor.start(0)
    c = 2
    while c <= 7.5:
        servoMotor.ChangeDutyCycle(c)
        c = c + 0.5
        time.sleep(waitTime)
    while c >= 0:
        servoMotor.ChangeDutyCycle(c)
        c = c - 0.5
        time.sleep(waitTime) 
    time.sleep(0.4)
    servoMotor.ChangeDutyCycle(0)
    servoMotor.stop()

smooth90DegreesMovement()
