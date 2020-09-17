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

vibration_api = Blueprint('vibration_api', __name__)

GPIO.setup(settings.vibration_pin, GPIO.OUT)

vibrationMotor = GPIO.PWM(settings.vibration_pin, 80) # 50 = 50Hz pulse

vibrationMotor.start(0)

@vibration_api.route("/start")
async def start():
    vibrationMotor.ChangeDutyCycle(40)
    return "Vibration Motors Started with 80Hz."

@vibration_api.route("/stop")
async def stop():
    vibrationMotor.ChangeDutyCycle(0)
    return "Vibration Motors Stopped."


