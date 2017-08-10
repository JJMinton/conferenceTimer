import logging
import path
import asyncio
from datetime import datetime, timedelta
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

from read_schedule import read_schedule

import config
logging.basicConfig(**config.logger_config)

class FileChangeHandler(PatternMatchingEventHandler):
    def __init__(self, watch_file, controller_function, args=[], loop=None):
        PatternMatchingEventHandler.__init__(self, patterns=[watch_file])
        self.controller_function = controller_function
        self.args = args
        self.loop = asyncio.SelectorEventLoop() if loop is None else loop
        self.async_task = None
        self.watch_file = watch_file
        
    def process(self, schedule_file_name=None):
        if schedule_file_name is None:
            schedule_file_name = self.watch_file
        logging.debug('FileChangeHnadler.process: Processing {}'.format(schedule_file_name))
        df = read_schedule(schedule_file_name)
        #Stop current run_schedule
        if self.async_task is not None:
            logging.debug('Stopping previous async_task')
            self.async_task.cancel()
            asyncio.wait_for(self.async_task, 100, loop=self.loop)
            del self.async_task
            self.async_task = None
        #Start new run_schedule
        logging.debug('FileChangeHandler.process: Starting new async_task')
        self.async_task = asyncio.ensure_future(self.controller_function(df, self.loop, *self.args), loop=self.loop)
        logging.debug('FileChangeHandler.process: Return from processing')
        return
        #ensure immediate return

    def on_created(self, event):
        logging.info('FileChangeHandler.on_created: File creation detected')
        self.process(event.src_path)

    def on_modified(self, event):
        logging.info('FileChangeHandler.on_modified: File change detected')
        self.process(event.src_path)

if __name__=="__main__":
    from schedule_handler import Schedule_Runner

    schedule_runner = Schedule_Runner()
    loop = schedule_runner.controller.loop 

    file_change_handler = FileChangeHandler(config.SCHEDULE_FILE, schedule_runner.run_schedule, loop=loop)

    obs = Observer();
    obs.schedule(file_change_handler, path.Path(config.SCHEDULE_FILE).abspath().dirname()) #Define what file to watch and how
    obs.start() #start watching file
    file_change_handler.process() #start schedule running
    try:
        while True:
            logging.debug('loop step')
            #This does nothing except step through the loops (why is this necessary?)
            file_change_handler.loop.run_until_complete(asyncio.ensure_future(asyncio.sleep(0.1, loop=file_change_handler.loop), loop=file_change_handler.loop)) #arbitrary sleep time here I think. Could it be forever?
    except KeyboardInterrupt:
        obs.stop();
    #finally:
    #    obs.join();
