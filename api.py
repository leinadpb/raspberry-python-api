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


def CreateWifiConfig(SSID, password):
  config_lines = [
    '\n',
    'network={',
    '\tssid="{}"'.format(SSID),
    '\tpsk="{}"'.format(password),
    '\tkey_mgmt=WPA-PSK',
    '}'
  ]

  config = '\n'.join(config_lines)
  print(config)

  with open("/etc/wpa_supplicant/wpa_supplicant.conf", "a+") as wifi:
    wifi.write(config)

  print("Wifi config added")


# Test Endpoint
@app.route("/v1/test")
async def hello():
    return "It works! > From RPi 4"

# TODO: Add some kind of authentication here.. As this can only be called from inside this ROBOT.
@app.route("/v1/config/wifi/<ssid>/<password>")
async def wifi(ssid, password):
    CreateWifiConfig(ssid, password)
    return "WiFi configuration!" + str(ssid) + ":" + str(password)

if (__name__ == "__main__"):
    app.run(debug=True, host="0.0.0.0", port=80)
