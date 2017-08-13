import logging
import asyncio
from datetime import datetime, timedelta

from controller import Controller
import light_controls as light_controls
import screen_controls as screen_controls

import config
logging.basicConfig(**config.logger_config)

class Schedule_Runner:
    def __init__(self, loop=None):
        self.screen = screen_controls.Screen()
        loop = asyncio.SelectorEventLoop() if loop is None else loop
        self.controller = Controller(universal_callbacks=[light_controls.clear, self.screen.clear], loop=loop)
        
    async def run_schedule(self, schedule, loop):
        logging.debug('run_schedule: calling controller.stop_all()')
        self.controller.stop_all() #This is currently unnecessary with the processes cancelling in the processes method. Which is better?
        for i, row in enumerate(schedule):
            logging.info('running {} at {}'.format(row['name'], row['start_time']))
            starting_time =  row['start_time']-config.STARTING_WARNING
            start_time =     row['start_time']
            warning_time =   row['start_time'] + row['talk_length'] - config.TALK_WARNING
            questions_time = row['start_time'] + row['talk_length']
            q_warning_time = row['start_time'] + row['talk_length'] + row['question_length'] - config.QUESTION_WARNING
            end_time =       row['start_time'] + row['talk_length'] + row['question_length']
            
            if seconds_until(starting_time) > 0:
                logging.debug('start until {}'.format(start_time))
                self.controller.start([light_controls.stop, self.screen.stop(row['name'], row['title'], start_time)])
                await asyncio.sleep(seconds_until(start_time), loop=loop)
            if seconds_until(start_time) > 0: #before talk start
                logging.debug('start until {}'.format(start_time))
                self.controller.start([light_controls.starting, self.screen.starting(row['name'], row['title'], start_time)])
                await asyncio.sleep(seconds_until(start_time), loop=loop)
            if seconds_until(warning_time) > 0: #before talk warning
                logging.debug('speaking until {}'.format(warning_time))
                self.controller.stop_all()
                self.controller.start([light_controls.speaking, self.screen.speaking(row['name'], row['title'], questions_time)])
                await asyncio.sleep(seconds_until(warning_time), loop=loop)
            if seconds_until(questions_time) > 0: #before question time
                logging.debug('speaking warning until {}'.format(questions_time))
                self.controller.stop_all()
                self.controller.start([light_controls.speaking_warning, self.screen.speaking_warning(row['name'], row['title'], questions_time)])
                await asyncio.sleep(seconds_until(questions_time), loop=loop)
            if seconds_until(q_warning_time) > 0: #before question warning
                logging.debug('questions until {}'.format(q_warning_time))
                self.controller.stop_all()
                self.controller.start([light_controls.questions, self.screen.questions(row['name'], row['title'], end_time)])
                await asyncio.sleep(seconds_until(q_warning_time), loop=loop)
            if seconds_until(end_time) > 0: #before end of talk
                logging.debug('questions warning until {}'.format(end_time))
                self.controller.stop_all()
                self.controller.start([light_controls.questions_warning, self.screen.questions_warning(row['name'], row['title'], end_time)])
                await asyncio.sleep(seconds_until(end_time), loop=loop)

            logging.debug('end')
        self.controller.stop_all()
        self.controller.start([light_controls.empty_schedule, self.screen.empty_schedule()])
        await asyncio.sleep(60*60*6, loop=loop)
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
