import pandas as pd
import logging
from datetime import timedelta

import config
logging.basicConfig(**config.logger_config)


def read_schedule(fileName):
    #read in data
    logging.info('Reading new schedule')
    dateparser = lambda x: pd.datetime.strptime(x, '%d/%m/%Y:%H%M')
    with open(fileName) as file:
        df = pd.read_csv(file, parse_dates=['start_time'], date_parser=dateparser, converters={'talk_length': lambda s: timedelta(minutes=int(s)), 'question_length': lambda s: timedelta(minutes=int(s))});
    #select speakers for this raspberry pi that haven't already spoken
    df = df.loc[df['room_code'] == config.ROOM_CODE];
    df = df.loc[df['start_time'] + df['talk_length'] + df['question_length'] > pd.datetime.today()];
    #sort selected speakers in starting order
    df = df.sort_values('start_time')
    if len(df) == 0:
        logging.info('Empty schedule') 
    return df;
