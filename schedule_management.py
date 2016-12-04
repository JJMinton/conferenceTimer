import logging

from datetime import datetime, timedelta
import pandas as pd;
from watchdog.observers import Observer;
from watchdog.events import PatternMatchingEventHandler

from controller import Controller
import light_controls
import screen_controls

ROOM_CODE = 'MVL'
STARTING_WARNING = timedelta(minutes=0)
TALK_WARNING = timedelta(minutes=3)
QUESTION_WARNING = timedelta(minutes=1)

class FileChangeHandler(PatternMatchingEventHandler):
    def __init__(self, controller_function, watch_file):
        PatternMatchingEventHandler.__init__(self, patterns=[watch_file])
        self.controller_function = controller_function
        self.master_task = self.process(watch_file)
        
    def process(self, schedule_file_name):
        logging.info('Processing {}'.format(schedule_file_name))
        df = read_schedule(schedule_file_name)
        #pass speaker list to controllersystem
        self.controller_function(df)
        #return master_task

    def on_created(self, event):
        #cancel self.master_task
        logging.info('File creation detected')
        self.master_task = self.process(event.src_path)

    def on_modified(self, event):
        #cancel self.master_task
        logging.info('File change detected')
        self.master_task = self.process(event.src_path)

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

def main_loop(df, controller):
    controller.stop_all()
    for row in df.iterrows():
        starting_time =  row[1]['start_time']-STARTING_WARNING
        start_time =     row[1]['start_time']
        warning_time =   row[1]['start_time'] + row[1]['talk_length'] - TALK_WARNING
        questions_time = row[1]['start_time'] + row[1]['talk_length']
        q_warning_time = row[1]['start_time'] + row[1]['talk_length'] + row[1]['question_length'] - QUESTION_WARNING
        end_time =       row[1]['start_time'] + row[1]['talk_length'] + row[1]['question_length']
        
        controller.start([light_controls.starting(), screen.starting(row[1]['name'], row[1]['title'], start_time)])
        controller.sleep_until(start_time)
        controller.stop_all()
        controller.start([light_controls.speaking(), screen.speaking(row[1]['name'], row[1]['title'], questions_time)])
        controller.sleep_until(warning_time)
        controller.stop_all()
        controller.start([light_controls.speakingwarning(), screen.speakingwarning(row[1]['name'], row[1]['title'], questions_time)])
        controller.sleep_until(questions_time)
        controller.stop_all()
        controller.start([ligt_control.questions(), screen.questions(row[1]['name'], row[1]['title'], end_time)])
        controller.sleep_until(q_warning_time)
        controller.stop_all()
        controller.start([light_control.questionswarning(), screen.questionswarning(row[1]['name'], row[1]['title'], end_time)])
        controller.sleep_until(end_time)
        controller.stop_all()

if __name__=="__main__":
    logging.basicConfig(filename='conference_timer.log',
                        level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S'))
    screen = screen_controls.Screen()
    controller = Controller(universal_callbacks=[light_controls.clear, screen.clear])
    initial_file = './schedule.csv'
    file_change_handler = FileChangeHandler(lambda df: main_loop(df, controller), initial_file);
    obs = Observer();
    obs.schedule(file_change_handler, '.')
    obs.start()
    try:
        while True:
            pass
    except KeyboardInterrupt:
        obs.stop();
    finally:
        obs.join();
