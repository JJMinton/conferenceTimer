import logging
logging.basicConfig(#filename='conference_timer.log',
                    level=logging.INFO,
                    format='%(asctime)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

import asyncio

from datetime import datetime, timedelta
import pandas as pd;
from watchdog.observers import Observer;
from watchdog.events import PatternMatchingEventHandler

from controller import Controller
import printed_light_controls as light_controls
import screen_controls

ROOM_CODE = 'MVL'
STARTING_WARNING = timedelta(minutes=0.5)
TALK_WARNING = timedelta(minutes=0.5)
QUESTION_WARNING = timedelta(minutes=0.5)

class FileChangeHandler(PatternMatchingEventHandler):
    def __init__(self, watch_file, controller_function, args=[]):
        PatternMatchingEventHandler.__init__(self, patterns=[watch_file])
        self.controller_function = controller_function
        self.args = args
        self.loop = asyncio.SelectorEventLoop()
        self.async_task = None
        
    def process(self, schedule_file_name):
        logging.info('Processing {}'.format(schedule_file_name))
        df = read_schedule(schedule_file_name)
        #Stop current run_schedule
        if self.async_task is not None:
            logging.info('Stopping previous async_task')
            self.async_task.cancel()
            #self.loop.run_until_complete(self.async_task)
            self.async_task = None
        #Start new run_schedule
        logging.info('Starting new async_task')
        self.async_task = asyncio.ensure_future(self.controller_function(df, self.loop, *self.args), loop=self.loop)
        logging.info('Return from processing')
        return
        #ensure immediate return

    def on_created(self, event):
        logging.info('File creation detected')
        self.process(event.src_path)

    def on_modified(self, event):
        logging.info('File change detected')
        self.process(event.src_path)

def read_schedule(fileName):
    #read in data
    dateparser = lambda x: pd.datetime.strptime(x, '%d/%m/%Y:%H%M')
    with open(fileName) as file:
        df = pd.read_csv(file, parse_dates=['start_time'], date_parser=dateparser, converters={'talk_length': lambda s: timedelta(minutes=int(s)), 'question_length': lambda s: timedelta(minutes=int(s))});
    #select speakers for this raspberry pi that haven't already spoken
    df = df.loc[df['room_code'] == ROOM_CODE];
    df = df.loc[df['start_time'] + df['talk_length'] + df['question_length'] > pd.datetime.today()];
    #sort selected speakers in starting order
    df = df.sort_values('start_time')
    return df;

class Schedule_Runner:
    def __init__(self):
        self.screen = screen_controls.Screen()
        self.controller = Controller(universal_callbacks=[light_controls.clear, self.screen.clear], loop=asyncio.SelectorEventLoop())
        
    async def run_schedule(self, df, loop):
        self.controller.stop_all()
        for row in df.iterrows():
            starting_time =  row[1]['start_time']-STARTING_WARNING
            start_time =     row[1]['start_time']
            warning_time =   row[1]['start_time'] + row[1]['talk_length'] - TALK_WARNING
            questions_time = row[1]['start_time'] + row[1]['talk_length']
            q_warning_time = row[1]['start_time'] + row[1]['talk_length'] + row[1]['question_length'] - QUESTION_WARNING
            end_time =       row[1]['start_time'] + row[1]['talk_length'] + row[1]['question_length']
            
            if seconds_until(start_time) > 0:
                logging.debug('start until {}'.format(start_time))
                self.controller.start([light_controls.starting, self.screen.starting(row[1]['name'], row[1]['title'], start_time)])
                await asyncio.sleep(seconds_until(start_time), loop=loop)
            if seconds_until(warning_time) > 0:
                logging.debug('speaking until {}'.format(warning_time))
                self.controller.stop_all()
                self.controller.start([light_controls.speaking, self.screen.speaking(row[1]['name'], row[1]['title'], questions_time)])
                await asyncio.sleep(seconds_until(warning_time), loop=loop)
            if seconds_until(questions_time) > 0:
                logging.debug('speakingwarning until {}'.format(questions_time))
                self.controller.stop_all()
                self.controller.start([light_controls.speakingwarning, self.screen.speakingwarning(row[1]['name'], row[1]['title'], questions_time)])
                await asyncio.sleep(seconds_until(questions_time), loop=loop)
            if seconds_until(q_warning_time) > 0:
                logging.debug('questions until {}'.format(q_warning_time))
                self.controller.stop_all()
                self.controller.start([light_controls.questions, self.screen.questions(row[1]['name'], row[1]['title'], end_time)])
                await asyncio.sleep(seconds_until(q_warning_time), loop=loop)
            if seconds_until(end_time) > 0:
                logging.debug('question warning until {}'.format(end_time))
                self.controller.stop_all()
                self.controller.start([light_controls.questionswarning, self.screen.questionswarning(row[1]['name'], row[1]['title'], end_time)])
                await asyncio.sleep(seconds_until(end_time), loop=loop)
            logging.debug('end')
            self.controller.stop_all()

async def run_schedule(df, loop=None):
    #self.controller.stop_all()
    logging.debug('running_schedule')
    for row in df.iterrows():
        print('row')
        starting_time =  row[1]['start_time']-STARTING_WARNING
        start_time =     row[1]['start_time']
        warning_time =   row[1]['start_time'] + row[1]['talk_length'] - TALK_WARNING
        questions_time = row[1]['start_time'] + row[1]['talk_length']
        q_warning_time = row[1]['start_time'] + row[1]['talk_length'] + row[1]['question_length'] - QUESTION_WARNING
        end_time =       row[1]['start_time'] + row[1]['talk_length'] + row[1]['question_length']
        
        if seconds_until(start_time) > 0:
            print('start until {}'.format(start_time))
            await asyncio.sleep(seconds_until(start_time), loop=loop)
        if seconds_until(warning_time) > 0:
            print('speaking until {}'.format(warning_time))
            await asyncio.sleep(seconds_until(warning_time), loop=loop)
        if seconds_until(questions_time) > 0:
            print('speakingwarning until {}'.format(questions_time))
            await asyncio.sleep(seconds_until(questions_time), loop=loop)
        if seconds_until(q_warning_time) > 0:
            print('questions until {}'.format(q_warning_time))
            await asyncio.sleep(seconds_until(q_warning_time), loop=loop)
        if seconds_until(end_time) > 0:
            print('question warning until {}'.format(end_time))
            await asyncio.sleep(seconds_until(end_time), loop=loop)
        print('end')

def seconds_until(time_to):
    return max(0,(time_to - datetime.now()).total_seconds())

if __name__=="__main__":
    schedule_file = './schedule.csv'

    schedule_runner = Schedule_Runner()
    file_change_handler = FileChangeHandler(schedule_file, schedule_runner.run_schedule);

    obs = Observer(); 
    obs.schedule(file_change_handler, '.') #Define what file to watch and how
    obs.start() #start watching file
    file_change_handler.process(schedule_file) #start first schedule
    try:
        while True:
            logging.debug('loop step')
            file_change_handler.loop.run_until_complete(asyncio.ensure_future(asyncio.sleep(0.5, loop=file_change_handler.loop), loop=file_change_handler.loop)) #arbitrary sleep time here I think. Could it be forever?
            schedule_runner.controller.loop.run_until_complete(asyncio.ensure_future(asyncio.sleep(0.5, loop=schedule_runner.controller.loop), loop=schedule_runner.controller.loop))
            #pass
    except KeyboardInterrupt:
        obs.stop();
    finally:
        obs.join();
