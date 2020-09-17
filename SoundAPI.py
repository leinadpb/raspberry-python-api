from quart import Blueprint
import settings
import os
sound_api = Blueprint('sound_api', __name__)

import pygame
pygame.init()

BIRD = settings.sound_birds_path
RAIN = settings.sound_rain_path
SEA = settings.sound_sea_path
SEA_ANIMALS = settings.sound_seaAnimals_path
LEAFS = settings.sound_leafs_path
WIND = settings.sound_wind_path

def playSound(type):
    if type == 'birds':
        pygame.mixer.music.load(BIRD)
    elif type == 'rain':
        pygame.mixer.music.load(RAIN)
    elif type == 'sea':
        pygame.mixer.music.load(SEA)
    elif type == 'sea_animals':
        pygame.mixer.music.load(SEA_ANIMALS)
    elif type == 'leafs':
        pygame.mixer.music.load(LEAFS)
    elif type == 'wind':
        pygame.mixer.music.load(WIND)
    # Play selected sound
    pygame.mixer.music.play()


@sound_api.route('/birds/play')
async def playBirdsSound():
    playSound('birds')
    return 'Playing BIRDS.'

@sound_api.route('/sea/play')
async def playSeaSound():
    playSound('sea')
    return 'Playing SEA.'

@sound_api.route('/sea_animals/play')
async def playSeaAnimalsSound():
    playSound('sea_animals')
    return 'Playing SEA ANIMALS.'

@sound_api.route('/wind/play')
async def playWindSound():
    playSound('wind')
    return 'Playing WIND.'

@sound_api.route('/leafs/play')
async def playLeafsSound():
    playSound('leafs')
    return 'Playing LEAFS.'

@sound_api.route('/rain/play')
async def playRainSound():
    playSound('rain')
    return 'Playing RAIN.'

@sound_api.route('/stop')
async def stopSound():
    pygame.mixer.music.fadeout(3)
    return 'Stopping music being played.'

@sound_api.route('/volume/<amount>')
async def changeVolume(amount):
    try:
        val = int(amount)
        if val < 0 or val > 100:
            return 'Monto invalido. Debe estar entre 0 y 100.'
        os.popen('amixer set Headphone ' + str(val) + '%', 'w')
        return "Volumen adjusted to: " + str(val) + " successfully."
    except Exception as e:
        print(e)
        return 'Hubo un error cambiando el volumen, favr intentelo de nuevo.'
