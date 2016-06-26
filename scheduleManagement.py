import time;
import pandas as pd;
from watchdog.observers import Observer;
from watchdog.events import PatternMatchingEventHandler

import control;

ROOM_CODE = 'MVL';
TALK_WARNING = 3;
QUESTION_WARNING = 1;

class MyHandler(PatternMatchingEventHandler):
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

def readSchedule(fileName):
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

def lightingProcess(df):
	lc = control.lightingControl;
	for column in df:
		starting =  column['start_time']-STARTING_WARNING;
		start =     column['start_time'];
		warning =   column['start_time'] + column['talk_length'] - TALK_WARNING;
		questions = column['start_time'] + column['talk_length'];
		q_warning = column['start_time'] + column['talk_length'] + column['question_length'] - QUESTION_WARNING;
		end =       column['start_time'] + column['talk_length'] + column['question_length'];

		control.change(column['name'], start);
		wait_until(lambda control.starting(column['name'], start), starting);
		wait_until(lambda control.speaking(column['name'], questions), start);
		wait_until(lambda control.speakingwarning(column['name'], questions), warning);
		wait_until(lambda control.questions(column['name'], end), questions);
		wait_until(lambda control.questionswarning(column['name'], end), q_warning);

def wait_until(action, time, wait=1):
	while(time < datetime):
		time.sleep(wait);
	action();

if __name__=="__main__":
	control.change();
	event_handler = MyHandler();
	obs = Observer();
	obs.schedule(event_handler, '.')
	obs.start()
	try:
		while True:
			time.sleep(1);
	except KeyboardInterrupt:
		obs.stop();
	obs.join();
