import datetime
import csv
import logging
import config
logging.basicConfig(**config.logger_config)

date_format = '%d/%m/%Y:%H%M'

def read_schedule(fileName):
    logging.info('Reading new schedule')
    talks = []
    with open(fileName, 'r') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',')
        for row in reader:
            if (row['room_code'] == config.ROOM_CODE): #if in this room
                #field parsing
                row['start_time'] = datetime.datetime.strptime(row['start_time'], date_format)
                row['talk_length'] = datetime.timedelta(minutes=int(row['talk_length']))
                row['question_length'] = datetime.timedelta(minutes=int(row['question_length']))
                print(row['start_time']+row['talk_length']+row['question_length'])
                if row['start_time']+row['talk_length']+row['question_length'] > datetime.datetime.today():#if not finished
                    talks.append(row)
    talks = sorted(talks, key=lambda x: x['start_time'])
    if len(talks) == 0:
        logging.info('Empty schedule')
    return talks




