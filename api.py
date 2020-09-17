from quart import Quart
import RPi.GPIO as GPIO

GPIO.cleanup()

# custom APIs
from LedAPI import led_api
from SoundAPI import sound_api
from VibrationAPI import vibration_api
#from DistanceAPI import distance_api

# Rest API
app = Quart(__name__)

# Register other APIs
app.register_blueprint(led_api, url_prefix="/v1/led")
app.register_blueprint(sound_api, url_prefix="/v1/sound")
app.register_blueprint(vibration_api, url_prefix="/v1/vibration")

# Test Endpoint
@app.route("/v1/test")
async def hello():
    return "It works! > From RPi 4"

if (__name__ == "__main__"):
    app.run(debug=True, host="0.0.0.0", port=80)
