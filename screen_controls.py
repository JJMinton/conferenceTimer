import asyncio
import time
import sys
import math
import random
from datetime import datetime, timedelta

import tkinter as tk
from tkinter import font as tkFont

import config

class Screen():
    def __init__(self):
        self.root = tk.Tk()
        if not config.DEBUG_FLAG:
            w, h = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
            self.root.geometry("{:}x{:}".format(w,h));
            self.root.attributes("-fullscreen", True);
            self.root.focus_set() # <-- move focus to this widget #root.bind("<Escape>", lambda e: e.widget.quit());
        
        self.helv = {24: tkFont.Font(family='Helvetica', size=36, weight='bold'),
                     36: tkFont.Font(family='Helvetica', size=24, weight='bold'),
                     72: tkFont.Font(family='Helvetica', size=72, weight='bold'),
                    }

        #Create Text
        #self.text_frame = tk.Frame(self.root, width=w, height=h, bg="red")
        #self.text_frame.place(in_=self.root, anchor='c', relx=0.5, rely=0.5);#pack(side = tk.LEFT);#, width=200, height=200, background="red").pack();
        self.text_frame = self.root
        self.speaker = tk.StringVar()
        self.title = tk.StringVar()
        self.message = tk.StringVar()
        self.labels = []
        self.labels.append(tk.Label(self.text_frame, text='Speaker:', font=self.helv[24]))
        self.labels.append(tk.Label(self.text_frame, textvariable=self.speaker, font=self.helv[36]))#place(_in=container);
        self.labels.append(tk.Label(self.text_frame, text='Title:', font=self.helv[24]))#place(_in=container);
        self.labels.append(tk.Label(self.text_frame, textvariable=self.title, font=self.helv[24]))#place(_in=container);
        self.labels.append(tk.Label(self.text_frame, textvariable=self.message, font=self.helv[72]))#place(_in=container);
        for l in self.labels:
            l.pack()
        self.root.update()

    def update(self, name=None, title=None, message=None, color=None):
        if color is not None:
            self.text_frame.configure(background=color)
            for l in self.labels:
                l.config(bg=color)
        self.speaker.set('' if name is None else name)
        self.title.set('' if title is None else title)
        self.message.set('' if message is None else message)
        self.root.update()

    def clear(self):
        self.update()

    def stop(self, name=None, title=None, endTime=None):
        async def stop(loop):
            while True:
                self.update('', '', 'Next talk starting in: {}'.format(formatted_count_down(endTime)), 'red')
                await asyncio.sleep(1., loop=loop)
        return stop

    def starting(self, name=None, title=None, endTime=None):
        async def starting(loop):
            while True:
                self.update(name, title, 'Starting in: {}'.format(formatted_count_down(endTime)), 'orange')
                await asyncio.sleep(1., loop=loop)
                self.update(name, title, 'Starting in: {}'.format(formatted_count_down(endTime)), 'grey')
                await asyncio.sleep(1., loop=loop)
        return starting

    def speaking(self, name=None, title=None, endTime=None):
        async def speaking(loop):
            while True:
                self.update(name, title, 'Speaking for: {}'.format(formatted_count_down(endTime)), 'green')
                await asyncio.sleep(1.0, loop=loop)
        return speaking

    def speaking_warning(self, name=None, title=None, endTime=None):
        async def speakingwarning(loop):
            while True:
                self.update(name, title, 'Speaking for: {}'.format(formatted_count_down(endTime)), 'green')
                await asyncio.sleep(1.0, loop=loop)
                
                self.update(name, title, 'Speaking for: {}'.format(formatted_count_down(endTime)), 'orange')
                await asyncio.sleep(1.0, loop=loop)
        return speakingwarning

    def questions(self, name=None, title=None, endTime=None):
        async def questions(loop):
            while True:
                self.update(name, title, 'Questions for: {}'.format(formatted_count_down(endTime)), 'orange')
                await asyncio.sleep(1.0, loop=loop)
        return questions

    def questions_warning(self, name=None, title=None, endTime=None):
        async def questions(loop):
            while True:

                self.update(name, title, 'Questions for: {}'.format(formatted_count_down(endTime)), 'orange')
                await asyncio.sleep(1.0, loop=loop)

                self.update(name, title, 'Questions for: {}'.format(formatted_count_down(endTime)), 'red')
                await asyncio.sleep(1.0, loop=loop)
        return questions
    def empty_schedule(self):
        async def questions(loop):
            while True:
                self.update('', '', "That's it, there's no more!", random.choice(['red','orange','green']))
                await asyncio.sleep(1.0, loop=loop)
        return questions

def formatted_count_down(end_time):
    dt = (end_time - datetime.now()).total_seconds()
    hours = math.floor(dt/(60*60))
    print(hours)
    minutes = math.floor((dt%(60*60))/60)
    print(minutes)
    seconds = math.floor(dt%(60))
    print(seconds)
    if hours > 0:
        return '{:}:{:0>2}:{:0>2}'.format(hours, minutes, seconds)
    else:
        return '{:}:{:0>2}'.format(minutes, seconds)

if __name__ == '__main__':
    from controller import Controller
    screen = Screen()
    screen_control = Controller(universal_callbacks=screen.clear)
    start_time = datetime.now() + timedelta(seconds=3)
    warn_time = datetime.now() + timedelta(seconds=7)
    q_time = datetime.now() + timedelta(seconds=10)
    end_time = datetime.now() + timedelta(seconds=13)

    screen_control.start(screen.starting('Johnny Bravo', 'Cancelled cartoons', start_time))
    screen_control.sleep_until(start_time)
    screen_control.stop_all()
    screen_control.start(screen.speaking('Johnny Bravo', 'Cancelled cartoons', warn_time))
    screen_control.sleep_until(warn_time)
    screen_control.stop_all()
    screen_control.start(screen.speakingwarning('Johnny Bravo', 'Cancelled cartoons', q_time))
    screen_control.sleep_until(q_time)
    screen_control.stop_all()
    screen_control.start(screen.questions('Johnny Bravo', 'Cancelled cartoons', end_time))
    screen_control.sleep_until(end_time)
    screen_control.stop_all()

