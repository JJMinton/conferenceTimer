import time;
import pandas as pd;
from watchdog.observers import Observer;
from watchdog.events import PatternMatchingEventHandler

ROOM_CODE = 'MVL';

class MyHandler(PatternMatchingEventHandler):
	patterns = ['*schedule.css'];
		
	def process(self, event):
		print(event.src_path);
		print(event.event_type);
		#read in data
		dateparser = lambda x: pd.datetime.strptime(x, '%d/%m/%Y:%H%M')
		with open(event.src_path) as file:
			df = pd.read_csv(file, parse_dates=['start_time'], date_parser=dateparser);
		#select speakers for this raspberry pi that haven't already spoken
		df = df.loc[df['room_code'] == ROOM_CODE];
		df = df.loc[df['start_time'] > pd.datetime.today()];
		#sort selected speakers in starting order
		df = df.sort_values('start_time')
		#pass speaker list to lighting system
		print(df);

	def on_created(self, event):
		self.process(event);
	def on_modified(self, event):
		self.process(event);

if __name__=="__main__":
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
