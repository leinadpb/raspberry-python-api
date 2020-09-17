from quart import Blueprint
import RPi.GPIO as GPIO
import asyncio
import settings
import time
import threading

# GPIO
## Common
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

servo_api = Blueprint('servo_api', __name__)

GPIO.setup(settings.servo_pin, GPIO.OUT)

servoMotor = GPIO.PWM(settings.servo_pin, 50) # 50 = 50Hz pulse

duty = 2  # 0 degress

shouldContinue = True

servoMotor.start(duty)

def smooth90DegreesMovement():
    for i in range(2,7,0.5):
        servoMotor.ChangeDutyCycle(i)
        time.sleep(0.08)
    for i in range(7,2,0.5):
        servoMotor.ChangeDutyCycle(i)
        time.sleep(0.08)
    servoMotor.stop() 

def servo_async_task():
    cycle = 0
    top = False
    global shouldContinue
    while shouldContinue:
        servoMotor.ChangeDutyCycle(cycle)
        time.sleep(1)
        if cycle >= 12:
            top = True
        if cycle <= 0:
            top = False
        if top:
            cycle = cycle - 1
        else:
            cycle = cycle + 1
    shouldContinue = True
    print("Finishing Thread successfully.")

@servo_api.route("/start")
async def start():
    # servoMotor.start(0)  # 0 => Pulse off
    runningThread = threading.Thread(target=smooth90DegreesMovement)
    runningThread.start()
    return "Servo Motor Started with 0Hz."

@servo_api.route("/stop")
async def stop():
    global shouldContinue
    shouldContinue = False
    servoMotor.ChangeDutyCycle(duty)
    # servoMotor.stop()
    return "Servo Motor Stopped."




