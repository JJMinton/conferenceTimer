import logging
logging.basicConfig(#filename='conference_timer.log',
                    level=logging.DEBUG,
                    format='%(asctime)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

import asyncio
from datetime import datetime, timedelta

from controller import Controller
import printed_light_controls as light_controls
import printed_screen_controls as screen_controls

ROOM_CODE = 'MVL'
STARTING_WARNING = timedelta(minutes=0.5)
TALK_WARNING = timedelta(minutes=0.5)
QUESTION_WARNING = timedelta(minutes=0.5)

class Schedule_Runner:
    def __init__(self, loop=None):
        self.screen = screen_controls.Screen()
        loop = asyncio.SelectorEventLoop() if loop is None else loop
        self.controller = Controller(universal_callbacks=[light_controls.clear, self.screen.clear], loop=loop)
        
    async def run_schedule(self, df, loop):
        logging.debug('Run Schedule: controller.stop_all()')
        self.controller.stop_all() #This is currently unnecessary with the processes cancelling in the processes method. Which is better?
        for i, row in df.iterrows():
            starting_time =  row['start_time']-STARTING_WARNING
            start_time =     row['start_time']
            warning_time =   row['start_time'] + row['talk_length'] - TALK_WARNING
            questions_time = row['start_time'] + row['talk_length']
            q_warning_time = row['start_time'] + row['talk_length'] + row['question_length'] - QUESTION_WARNING
            end_time =       row['start_time'] + row['talk_length'] + row['question_length']
            
            if seconds_until(start_time) > 0:
                logging.debug('start until {}'.format(start_time))
                self.controller.start([light_controls.starting, self.screen.starting(row['name'], row['title'], start_time)])
                await asyncio.sleep(seconds_until(start_time), loop=loop)
            if seconds_until(warning_time) > 0:
                logging.debug('speaking until {}'.format(warning_time))
                self.controller.stop_all()
                self.controller.start([light_controls.speaking, self.screen.speaking(row['name'], row['title'], questions_time)])
                await asyncio.sleep(seconds_until(warning_time), loop=loop)
            if seconds_until(questions_time) > 0:
                logging.debug('speakingwarning until {}'.format(questions_time))
                self.controller.stop_all()
                self.controller.start([light_controls.speakingwarning, self.screen.speakingwarning(row['name'], row['title'], questions_time)])
                await asyncio.sleep(seconds_until(questions_time), loop=loop)
            if seconds_until(q_warning_time) > 0:
                logging.debug('questions until {}'.format(q_warning_time))
                self.controller.stop_all()
                self.controller.start([light_controls.questions, self.screen.questions(row['name'], row['title'], end_time)])
                await asyncio.sleep(seconds_until(q_warning_time), loop=loop)
            if seconds_until(end_time) > 0:
                logging.debug('question warning until {}'.format(end_time))
                self.controller.stop_all()
                self.controller.start([light_controls.questionswarning, self.screen.questionswarning(row['name'], row['title'], end_time)])
                await asyncio.sleep(seconds_until(end_time), loop=loop)
            logging.debug('end')
            self.controller.stop_all()


def seconds_until(time_to):
    return max(0,(time_to - datetime.now()).total_seconds())

if __name__=="__main__":
    from file_change_handler import read_schedule

    schedule_file = './schedule.csv'
    df = read_schedule(schedule_file)

    schedule_runner = Schedule_Runner()
    loop = schedule_runner.controller.loop 
    asyncio.ensure_future(schedule_runner.run_schedule(df, loop), loop=loop)
    while True:
        loop.run_until_complete(asyncio.sleep(0.1))
    loop.close()
