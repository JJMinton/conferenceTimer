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
        w, h = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
        if not config.DEBUG_FLAG:
            self.root.geometry("{:}x{:}".format(w,h));
            self.root.attributes("-fullscreen", True);
            self.root.focus_set() # <-- move focus to this widget #root.bind("<Escape>", lambda e: e.widget.quit());
        
        self.helv = {24: tkFont.Font(family='Helvetica', size=36, weight='bold'),
                     36: tkFont.Font(family='Helvetica', size=24, weight='bold'),
                     72: tkFont.Font(family='Helvetica', size=72, weight='bold'),
                    }

        #Create color bars
        #w,h = self.root.winfo_width(), self.root.winfo_height()
        #self.canvas = tk.Canvas(self.root, borderwidth=0, highlightThickness=0)
        #self.canvas.grid(row=0,column=0)
        self.top_color = tk.Label(self.root, bg='yellow')
        self.top_color.pack(fill=tk.BOTH, expand=True)
        self.bottom_color = tk.Label(self.root, bg='magenta')
        self.bottom_color.pack(fill=tk.BOTH, expand=True)

        #Create Text
        self.speaker = tk.StringVar()
        self.title = tk.StringVar()
        self.message = tk.StringVar()
        self.labels = []
        self.labels.append(tk.Label(self.top_color, text='Speaker:', font=self.helv[24], wraplength=w))
        self.labels.append(tk.Label(self.top_color, textvariable=self.speaker, font=self.helv[36], wraplength=w))#place(_in=container);
        self.labels.append(tk.Label(self.top_color, text='Title:', font=self.helv[24], wraplength=w))#place(_in=container);
        self.labels.append(tk.Label(self.top_color, textvariable=self.title, font=self.helv[24], wraplength=w))#place(_in=container);
        self.labels.append(tk.Label(self.bottom_color, textvariable=self.message, font=self.helv[72], wraplength=w))#place(_in=container);
        for i, l in enumerate(self.labels[:-1]):
            l.pack(anchor=tk.CENTER)
        self.labels[-1].place(rely=.5, relx=.5, anchor=tk.CENTER)
        self.root.update()

    def update(self, name=None, title=None, message=None, color=None, color2=None):
        if color is None:
            color = 'grey'
        if color2 is None:
            color2 = color
        if self.top_color['bg'] != color:
            self.top_color.configure(background=color)
            for l in self.labels[:-1]:
                l.config(bg=color)
        if self.bottom_color['bg'] != color2:
            self.bottom_color.configure(background=color2)
            self.labels[-1].config(bg=color2)

        self.speaker.set('' if name is None else name)
        self.title.set('' if title is None else title)
        self.message.set('' if message is None else message)
        self.root.update()

    def clear(self):
        self.update()

    def stop(self, name=None, title=None, endTime=None):
        async def stop(loop):
            while True:
                self.update('', '', 'Nothing for: {}'.format(formatted_count_down(endTime)), 'red')
                await asyncio.sleep(1., loop=loop)
        return stop

    def starting(self, name=None, title=None, endTime=None):
        async def starting(loop):
            while True:
                self.update(name, title, 'Starting in: {}'.format(formatted_count_down(endTime)), 'orange', 'grey')
                await asyncio.sleep(1.0, loop=loop)
                self.update(name, title, 'Starting in: {}'.format(formatted_count_down(endTime)), 'grey', 'orange')
                await asyncio.sleep(1.0, loop=loop)
        return starting

    def speaking(self, name=None, title=None, endTime=None):
        async def speaking(loop):
            while True:
                self.update(name, title, 'Speaking for: {}'.format(formatted_count_down(endTime)), 'green')
                await asyncio.sleep(0.01, loop=loop)
        return speaking

    def speaking_warning(self, name=None, title=None, endTime=None):
        async def speakingwarning(loop):
            while True:
                self.update(name, title, 'Speaking for: {}'.format(formatted_count_down(endTime)), 'green', 'orange')
                await asyncio.sleep(0.01, loop=loop)
        return speakingwarning

    def questions(self, name=None, title=None, endTime=None):
        async def questions(loop):
            while True:
                self.update(name, title, 'Questions for: {}'.format(formatted_count_down(endTime)), 'orange')
                await asyncio.sleep(0.01, loop=loop)
        return questions

    def questions_warning(self, name=None, title=None, endTime=None):
        async def questions(loop):
            while True:
                self.update(name, title, 'Questions for: {}'.format(formatted_count_down(endTime)), 'orange', 'red')
                await asyncio.sleep(0.01, loop=loop)
        return questions
    def empty_schedule(self):
        async def questions(loop):
            while True:
                self.update('', '', "That's it, there's no more", random.choice(['red','orange','green']), random.choice(['red','orange','green']))
                await asyncio.sleep(0.4, loop=loop)
        return questions

def formatted_count_down(end_time):
    dt = (end_time - datetime.now()).total_seconds()
    hours = math.floor(dt/(60*60))
    minutes = math.floor((dt%(60*60))/60)
    seconds = math.floor(dt%(60))
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

