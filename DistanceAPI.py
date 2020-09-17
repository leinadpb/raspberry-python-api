

from quart import Blueprint
import RPi.GPIO as GPIO
import time
import settings
import threading

trigPin = settings.ultrasonic_trigger_pin
echoPin = settings.ultrasonic_echo_pin
MAX_DISTANCE = 220
timeOut = MAX_DISTANCE * 60

GPIO.setup(trigPin, GPIO.OUT)
GPIO.setup(echoPin, GPIO.IN)

distance_api = Blueprint('distance_api', __name__)

shouldContinueDistance = True

# Obtain pulse time of a pin
def pulseIn(pin, level, timeOut):
    t0 = time.time()
    while(GPIO.input(pin) != level):
        if( (time.time() - t0) > timeOut * 0.000001):
            return 0;
    t0 = time.time()
    while(GPIO.input(pin) == level):
        if( (time.time() - t0 ) > timeOut * 0.000001):
            return 0;
    pulseTime = (time.time() - t0) * 1000000
    return pulseTime


# Get the measurement results of ultrasonic module, unit: cm
def getDistance():
    GPIO.output(trigPin, GPIO.HIGH)   # make trigPin send 10us high  level
    time.sleep(0.00001)   # 10us
    GPIO.output(trigPin, GPIO.LOW)
    pingTime = pulseIn(echoPin, GPIO.HIGH, timeOut)  # read plus time of echoPin
    distance = pingTime * 340.0 / 2.0 / 10000.0  # the total sound speed is 340m/s, and calculate distance
    return distance

def distance_async_task():
    global shouldContinueDistance
    while shouldContinueDistance:
        distance = getDistance()
        print("Distance Read: " + str(distance))
        if (distance <= 5):
            print("too close !!!!!")
        time.sleep(1)
    shouldContinueDistance = True
    print("Ultrasonic has stopped!")

@distance_api.route("/start")
async def start():
    thread = threading.Thread(target = distance_async_task)
    thread.start()
    return "Ultrasonic started!"

@distance_api.route("/stop")
async def stop():
    global shouldContinueDistance
    shouldContinueDistance = False
    return "Ultrasonic sent to stop.. Wait a few millisenconds."



