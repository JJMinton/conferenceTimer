import openpyxl
import pandas as pd
from datetime import datetime, timedelta

start_date = datetime(year=2017, month=8, day=29)
room_converter = {'S1': 'ictp-rpi-1',
                  'S2': 'ictp-rpi-2',
                  'S3': 'ictp-rpi-3',
                  'S4': 'ictp-rpi-4',
                  'S5': 'ictp-rpi-5',
                  'S6': 'ictp-rpi-6',
                  'S7': 'ictp-rpi-7',
                  'S8': 'ictp-rpi-8',
                  'S9': 'ictp-rpi-9',
                 }
day_converter = {'Mon': 0,
                 'Tue': 1,
                 'Wed': 2,
                 'Thu': 3,
                 'Fri': 4,
                 'Sat': 5,
                 'Sun': 6,
                }
date_format = '%d/%m/%Y:%H%M'



df = pd.DataFrame(columns=['OPENCONF ID', 'room_code', 'start_time', 'talk_length', 'question_length', 'chair'])
wb = openpyxl.load_workbook(filename='ICTP_timetable_Jose.xlsx')
for ws_name in ['S{}'.format(i+1) for i in range(9)]:
    data = wb[ws_name].values
    next(data); cols = next(data) #first row blank

    day = None
    chair = None
    for d in data:
        #print(ws_name, d)
        number = d[cols.index('Presentation number')]
        if number is None:
            continue
        if type(number) == int:
            talk_length = 15; question_length = 4;
        elif number == 'Poster session':
            talk_length = 39; question_length = 0; chair = ''
            next(data)
        elif number[:2] == 'IW':
            talk_length = 59; question_length = 0; chair = ''
            next(data); next(data)
        else:#number in ['Coffee Break', 'No presentation']:
            print(number)
            continue

   
        if d[cols.index('Chair')] is not None:
            chair = d[cols.index('Chair')]
        ## Calculate start time
        if d[cols.index('Session')] is not None:
            day = day_converter[d[cols.index('Session')][:3]]
        time = d[cols.index('Starting time')]
        start_time = start_date + timedelta(days=day, hours=time.hour, minutes=time.minute)#################### add time

        df = df.append({
                        'start_time': start_time.strftime(date_format),
                        'OPENCONF ID': number,
                        'chair': chair,
                        'room_code': room_converter[ws_name],
                        'talk_length': talk_length,
                        'question_length': question_length,
                       }, ignore_index=True)
        
db = pd.read_csv('ictp.csv')
schedule = pd.merge(df,db,on=['OPENCONF ID'] )
schedule = schedule.rename(columns={'OPENCONF ID': 'id',
                         'PRESENTING AUTHOR': 'name',
                         'TITLE': 'title'})
del schedule['ICTP MANUSCRIPT NUMBER']

schedule.to_csv('schedule.csv', index=False, float_format='%.0f')
