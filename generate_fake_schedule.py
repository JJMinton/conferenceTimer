import pandas as pd
from datetime import datetime, timedelta
_start_time = datetime(year=2017, month=8, day=13, hour=9, minute=34)
talk_length = 4
question_length = 2
date_format = '%d/%m/%Y:%H%M'

room_list = ['ictp-rpi-1',
             'ictp-rpi-2',]


talks =[('Green Lantern','Well that was a rubbish Movie'),
        ('Deadpool','R18 super hero'),
        ('Rogers','Marvel super Heroes'),
        ('Bucky','Marvel Bad Guys'),
        ('The Joker','DC Bad Guys'),
        ('Batman','DC Good Guys'),
        ('Spiderman',"DC can't actually fly"),
        ('Superman','DC can fly'),
        ('Hulk','Marvel jump good'),
        ('Ironman','Marvel Can actually Fly'),
        ('Black widow','Marvel lady Avenger'),
        ('The Flash','Super fast hero'),]

id_number = 0
df = pd.DataFrame(columns=['id', 'room_code', 'start_time', 'talk_length', 'question_length', 'chair', 'name', 'title'])
for room in room_list:
    start_time = _start_time
    for name, title in talks:
        df = df.append({
                        'start_time': start_time.strftime(date_format),
                        'id': id_number,
                        'chair': 'Paul Blart',
                        'room_code': room,
                        'talk_length': talk_length,
                        'question_length': question_length,
                        'name': name,
                        'title': title,
                       }, ignore_index=True)
        id_number += 1
        start_time += timedelta(minutes=talk_length+question_length+2)
            
df.to_csv('schedule.csv', index=False, float_format='%.0f')
