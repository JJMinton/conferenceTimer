import time;
import pandas as pd;
from watchdog.observers import Observer;
from watchdog.events import PatternMatchingEventHandler

import light_control;

ROOM_CODE = 'MVL'
STARTING_WARNING = 0
TALK_WARNING = 3
QUESTION_WARNING = 1

class FileChangeHandler(PatternMatchingEventHandler):
	patterns = ['*schedule.css'];
		
	def process(self, event):
		print(event.src_path);
		print(event.event_type);
		df = readSchedule(event.src_path);
		#pass speaker list to lighting system
		lightingProcess(df);

	def on_created(self, event):
		self.process(event);
	def on_modified(self, event):
		self.process(event);

def read_schedule(fileName):
	#read in data
	dateparser = lambda x: pd.datetime.strptime(x, '%d/%m/%Y:%H%M')
	with open(fileName) as file:
		df = pd.read_csv(file, parse_dates=['start_time'], date_parser=dateparser);
	#select speakers for this raspberry pi that haven't already spoken
	df = df.loc[df['room_code'] == ROOM_CODE];
	df = df.loc[df['start_time'] > pd.datetime.today()];
	#sort selected speakers in starting order
	df = df.sort_values('start_time')
	return df;

def lighting_process(df):
	lc = light_control.lighting_control;
	for column in df:
		starting_time =  column['start_time']-STARTING_WARNING;
		start_time =     column['start_time'];
		warning_time =   column['start_time'] + column['talk_length'] - TALK_WARNING;
		questions_time = column['start_time'] + column['talk_length'];
		q_warning_time = column['start_time'] + column['talk_length'] + column['question_length'] - QUESTION_WARNING;
		end_time =       column['start_time'] + column['talk_length'] + column['question_length'];

		control.change(column['name'], start_time)
		wait_until(lambda control.starting(column['name'], start), starting_time)
		wait_until(lambda control.speaking(column['name'], questions), start_time)
		wait_until(lambda control.speakingwarning(column['name'], questions), warning_time)
		wait_until(lambda control.questions(column['name'], end), questions_time)
		wait_until(lambda control.questionswarning(column['name'], end), q_warning_time)

def wait_until(action, time, wait=1):
	while(time < datetime):
		time.sleep(wait);
	action();

if __name__=="__main__":
	light_control.change();
	file_change_handler = FileChangeHandler();
	obs = Observer();
	obs.schedule(file_change_handler, '.')
	obs.start()
	try:
		while True:
			time.sleep(1);
	except KeyboardInterrupt:
		obs.stop();
    finally:
        obs.join();
