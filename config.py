### Schedule management
ROOM_CODE = 'RM1'
SCHEDULE_FILE = '/home/pi/conferenceTimer/schedule.csv'


### Light timing
STARTING_WARNING = timedelta(minutes=0.5)
TALK_WARNING = timedelta(minutes=0.5)
QUESTION_WARNING = timedelta(minutes=0.5)


### Hardware configuration
PIN_MODE = gpio.BOARD
GREEN_LIGHT = 36
ORANGE_LIGHT = 38
RED_LIGHT = 40

### Debug controls
DEBUG_FLAG = True
