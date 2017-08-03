### Debug and Logging controls
DEBUG_FLAG = True
HARDWARE_FLAG = True
import logging
logger_config = {#'filename': 'conference_timer.log',
                 'format': '%(asctime)s - %(message)s',
                 'datefmt': '%Y-%m-%d %H:%M:%S'}

if DEBUG_FLAG:
    logger_config['level'] = logging.INFO
    #logger_config['level'] = logging.DEBUG
else:
    logger_config['level'] = logging.WARNING


### Schedule management
ROOM_CODE = 'MVL'
SCHEDULE_FILE = '/home/pi/conferenceTimer/schedule.csv'


### Light timing
from datetime import timedelta
STARTING_WARNING = timedelta(minutes=0.5)
TALK_WARNING = timedelta(minutes=0.5)
QUESTION_WARNING = timedelta(minutes=0.5)


### Hardware configuration
if HARDWARE_FLAG:
    import RPi.GPIO as gpio
    PIN_MODE = gpio.BOARD
    GREEN_LIGHT = 36
    ORANGE_LIGHT = 38
    RED_LIGHT = 40

