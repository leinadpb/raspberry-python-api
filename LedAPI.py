from quart import Blueprint
import RPi.GPIO as GPIO
import settings
#import pigpio
#pi = pigpio.pi()

# GPIO
## Common
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False) # GPIO

## Red LED
GPIO.setup(settings.red_led_pin, GPIO.OUT)
GPIO.setup(settings.blue_led_pin, GPIO.OUT)
GPIO.setup(settings.green_led_pin, GPIO.OUT)

led_api = Blueprint('led_api', __name__)

# LEDs
red = GPIO.PWM(settings.red_led_pin, 100)
blue = GPIO.PWM(settings.blue_led_pin, 100)
green = GPIO.PWM(settings.green_led_pin, 100)

#r = 0.0
#g = 0.0
#b = 0.0

#pi.set_mode(settings.red_led_pin, pigpio.OUTPUT)
#pi.set_mode(settings.blue_led_pin, pigpio.OUTPUT)
#pi.set_mode(settings.green_led_pin, pigpio.OUTPUT)

#pi.set_PWM_dutycycle(settings.red_led_pin, 0)
#pi.set_PWM_dutycycle(settings.green_led_pin, 0)
#pi.set_PWM_dutycycle(settings.blue_led_pin, 0)

def getColorWithBright(color, bright):
    val = int(int(color) * (float(bright) / 255.0))
    print('Color value to be set: ' + str(val))
    return val

def getColorFromPercentage(percentage, color):
    return int((percentage * color) / 100)

def adjustColorInPin(amount,color, led):
    try:
        val = int(amount)
        if (val < 0 or val > 100):
            return "Not valid request."
        #bright = getColorFromPercentage(val, 255)
        #print('New bright set: ' + str(bright))
        print('New percentage to be set: ' + str(amount))
        led.ChangeDutyCycle(val)
        #pi.set_PWM_dutycycle(pin, getColorWithBright(255, bright))
        return "LED is at: " + str(val)
    except Exception as e:
        print('Error Details: ----')
        print(amount)
        print(bright)
        print(e)
        led.stop()
        return "Invalid amount in request."

@led_api.route("/purple/on")
async def turnPurpleOn():
    #pi.set_PWM_dutycycle(settings.red_led_pin, getColorWithBright(128, settings.initial_led_value))
    #pi.set_PWM_dutycycle(settings.blue_led_pin, getColorWithBright(128, settings.initial_led_value))
    green.stop()
    red.start(getColorWithBright(128, settings.initial_led_value))
    blue.start(getColorWithBright(128, settings.initial_led_value))
    return "OK > Started purple light at " + str(settings.initial_led_value) + "% of intensity."

@led_api.route("/red/on")
async def turnRedOn():
    #pi.set_PWM_dutycycle(settings.red_led_pin, getColorWithBright(255, settings.initial_led_value))
    #pi.set_PWM_dutycycle(settings.blue_led_pin, 0)
    #pi.set_PWM_dutycycle(settings.green_led_pin, 0)
    red.start(getColorWithBright(255, settings.initial_led_value))
    blue.stop()
    green.stop()
    return "OK > Started red light at " + str(settings.initial_led_value) + "% of intensity."

@led_api.route("/blue/on")
async def turnBlueOn():
    #pi.set_PWM_dutycycle(settings.red_led_pin, 0)
    #pi.set_PWM_dutycycle(settings.blue_led_pin, getColorWithBright(255, settings.initial_led_value))
    #pi.set_PWM_dutycycle(settings.green_led_pin, 0)
    red.stop()
    green.stop()
    blue.start(getColorWithBright(255, settings.initial_led_value))
    return "OK > Started Blue light at " + str(settings.initial_led_value) + "% of intensity."

@led_api.route("/green/on")
async def turnGreenOn():
    #pi.set_PWM_dutycycle(settings.red_led_pin, 0)
    #pi.set_PWM_dutycycle(settings.blue_led_pin, 0)
    #pi.set_PWM_dutycycle(settings.green_led_pin, getColorWithBright(255, settings.initial_led_value))
    red.stop()
    blue.stop()
    green.start(getColorWithBright(255,settings.initial_led_value))
    return "OK > Started Green light at " + str(settings.initial_led_value) + "% of intensity."

@led_api.route("/off")
async def turnOff():
    #pi.set_PWM_dutycycle(settings.red_led_pin, 0)
    #pi.set_PWM_dutycycle(settings.blue_led_pin, 0)
    #pi.set_PWM_dutycycle(settings.green_led_pin, 0)
    red.stop()
    green.stop()
    blue.stop()
    return "OK > Stopped LED Strip lights."

@led_api.route("/red/adjust/<amount>")
async def adjustRed(amount):
    return adjustColorInPin(amount, 255, red)

@led_api.route("/blue/adjust/<amount>")
async def adjustBlue(amount):
    return adjustColorInPin(amount, 255, blue)

@led_api.route("/green/adjust/<amount>")
async def adjustGreen(amount):
    return adjustColorInPin(amount, 255, green)

@led_api.route("/purple/adjust/<amount>")
async def adjustPurple(amount):
    adjustColorInPin(amount, 128, red)
    adjustColorInPin(amount, 128, blue)
    return "OK: Adjusted Purple Color"
