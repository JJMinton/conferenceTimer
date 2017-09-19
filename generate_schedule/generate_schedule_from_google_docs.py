import sys, os, requests
import json, ast
from datetime import datetime, timedelta
import pandas as pd
import argparse

import gspread
from oauth2client.client import OAuth2WebServerFlow
from oauth2client import tools
from oauth2client.tools import run_flow
from oauth2client.file import Storage
from oauth2client.service_account import ServiceAccountCredentials


import private

def authenticate_google_docs(creds):
    scope = ['https://spreadsheets.google.com/feeds', 'https://docs.google.com/feeds']

    
    with open(os.path.join('traffic-lights-d42b9c17ee92.json'), 'r') as f:
        json_dict = json.load(f)
    #credentials = SignedJwtAssertionCredentials('username@gmail.com', SIGNED_KEY, scope)
    credentials = ServiceAccountCredentials.from_json_keyfile_dict(json_dict, scopes=scope)

    #data = {
    #    'refresh_token' : creds.refresh_token,
    #    'client_id' : CLIENT_ID,
    #    'client_secret' : CLIENT_SECRET,
    #    'grant_type' : 'refresh_token',
    #}

    #r = requests.post('https://accounts.google.com/o/oauth2/token', data = data)
    #print(ast.literal_eval(r.text))
    credentials.access_token = creds.access_token#ast.literal_eval(r.text)['access_token']

    gc = gspread.authorize(credentials)
    return gc


if __name__ == '__main__':
    

    CLIENT_ID = '174275065291-8u2p10943v0vjrh3nppeu2mquvitf6l9.apps.googleusercontent.com'
    CLIENT_SECRET = private.CLIENT_SECRET
    STORAGE_FILE = 'creds.data'
    storage = Storage(STORAGE_FILE)
    credentials = storage.get()
    if not credentials or (credentials.token_expiry < datetime.now()):
        flow = OAuth2WebServerFlow(
                  client_id = CLIENT_ID,
                  client_secret = CLIENT_SECRET,
                  scope = 'https://spreadsheets.google.com/feeds https://docs.google.com/feeds',
                  redirect_uri = 'http://127.0.0.1:8081/'
               )
        parser = argparse.ArgumentParser(
            description=__doc__,
            formatter_class=argparse.RawDescriptionHelpFormatter,
            parents=[tools.argparser])
        #credentials = run_flow(flow, storage)
        credentials = run_flow(flow, storage, parser.parse_args(['--auth_host_name', '127.0.0.1']))
    gc = authenticate_google_docs(credentials)
    #sh = gc.open("My Expenses") # Open by name
    #sh = gc.open_by_key('0BmgG6nO_6dprdS1MN3d3MkdPa142WFRrdnRRUWl1UFE') # Open by key which can be extracted from spreadsheet's url
    sh = gc.open_by_url('https://docs.google.com/spreadsheets/d/1b1HXr2HU5Hq-zM-b1KMY3uDq047cNIdWEODzM9P6T70/edit#gid=0')

    start_date = datetime(year=2017, month=9, day=18) + timedelta(minutes=0)
    room_converter = {'LR3': 'ictp-rpi-1',
                      'LR3A': 'ictp-rpi-2',
                      'LR3B': 'ictp-rpi-3',
                      'LR5': 'ictp-rpi-4',
                      'LT0': 'ictp-rpi-5',
                      'LT1': 'ictp-rpi-6',
                      'LT2': 'ictp-rpi-7',
                      'LT6': 'ictp-rpi-8',
                      'JDBSR': 'ictp-rpi-9',
                      'LR4': 'ictp-rpi-10',
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

    df = pd.DataFrame(columns=['name', 'title', 'room_code', 'start_time', 'talk_length', 'question_length', 'chair'])



    #add regular talks
    ws = sh.worksheet('Talks')
    talks = ws.get_all_records()
    for talk in talks:
        if talk['Day'] == '':
            continue
        day = day_converter[talk['Day']]
        start_time = datetime.strptime(talk['Start Time'], '%H:%M')
        start_time = start_date + timedelta(days=day, hours=start_time.hour, minutes=start_time.minute)#################### add time
        df = df.append({
                        'name': talk['Presenting Authors'],
                        'title': talk['Title'],
                        'start_time': start_time.strftime(date_format),
                        'chair': talk['Session Chair'],
                        'room_code': room_converter[talk['Room']],
                        'talk_length': 15,
                        'question_length': 4,
                       }, ignore_index=True)

    #add plenary talks/industry workshops/poster sessions
    ws = sh.worksheet('Plenary Talks')
    talks = ws.get_all_records()
    for talk in talks:
        if 'Title' not in talk:
            continue
        day = day_converter[talk['Day']]
        start_time = datetime.strptime(talk['Start Time'], '%H:%M')
        start_time = start_date + timedelta(days=day, hours=start_time.hour, minutes=start_time.minute)#################### add time
        df = df.append({
                        'name': talk['Presenting Authors'],
                        'title': talk['Title'],
                        'start_time': start_time.strftime(date_format),
                        'chair': talk['Chair'],
                        'room_code': room_converter[talk['Room']],
                        'talk_length': talk['Talk Length'],
                        'question_length': talk['Question Length'],
                       }, ignore_index=True)

df.to_csv('schedule.csv', index=False, float_format='%.0f')
