### Debug and Logging controls
DEBUG_FLAG = True
HARDWARE_FLAG = False
LIGHT_DEBUG = True
import logging
logger_config = {#'filename': 'conference_timer.log',
                 'format': '%(asctime)s - %(message)s',
                 'datefmt': '%Y-%m-%d %H:%M:%S'}
logging.basicConfig(**logger_config)
if DEBUG_FLAG:
    #logger_config['level'] = logging.INFO
    logger_config['level'] = logging.DEBUG
else:
    logger_config['level'] = logging.WARNING
logging = logging.getLogger('conference_timer_logger')
logging.setLevel(logger_config['level'])


### Schedule management
import path, pathlib
with open(path.Path.joinpath(str(pathlib.Path.home()), 'conferenceTimer/scripts/computername.txt'), 'r') as fin:
    ROOM_CODE = fin.read().splitlines()[0]
SCHEDULE_FILE = path.Path.joinpath(str(pathlib.Path.home()), 'conferenceTimer/schedule.csv')
del path, pathlib


### Light timing
from datetime import timedelta
STARTING_WARNING = timedelta(minutes=1)
TALK_WARNING = timedelta(minutes=3)
QUESTION_WARNING = timedelta(minutes=1)
del timedelta


### Hardware configuration
if HARDWARE_FLAG:
    import RPi.GPIO as gpio
    PIN_MODE = gpio.BOARD
    GREEN_LIGHT = 36
    ORANGE_LIGHT = 38
    RED_LIGHT = 40

    gpio.setmode(PIN_MODE)
    gpio.setup(GREEN_LIGHT, gpio.OUT)
    gpio.setup(ORANGE_LIGHT, gpio.OUT)
    gpio.setup(RED_LIGHT, gpio.OUT)

    del gpio
