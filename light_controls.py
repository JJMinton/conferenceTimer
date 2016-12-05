import asyncio
import time

import RPi.GPIO as io

from controller import Controller

io.setmode(io.BOARD)
io.setup(11, io.OUT)
io.setup(13, io.OUT)
io.setup(15, io.OUT)

def green(on=True):
    io.output(11, on)
def orange(on=True):
    io.output(13, on)
def red(on=True):
    io.output(15, on)
def lights(state):
    if type(state) == int:
        green(bool(state/100))
        orange(bool(state/10 % 10))
        red(bool(state % 10))
    if type(state) == tuple:
        green(state[0])
        orange(state[1])
        red(state[2])
    if type(state) == str:
        green(state[0] in ['1','g'])
        orange(state[1]  in ['1', 'o'])
        red(state[1] in ['1', 'r'])

async def starting():
    while True:
        lights('-or')
        await asyncio.sleep(2.0);
async def speaking():
    while True:
        lights('g--');
        await asyncio.sleep(2.0);
async def speakingwarning():
    while True:
        lights('go-');
        await asyncio.sleep(2.0);
async def questions():
    while True:
        lights('-o-');
        await asyncio.sleep(2.0);
async def questionswarning():
    while True:
        lights('---');
        await asyncio.sleep(1.0);
        lights('-o-');
        await asyncio.sleep(1.0);
async def change():
    while True:
        lights('--r');
        await asyncio.sleep(2.0);
def clear():
    lights('---');


if __name__ == '__main__':

    light_control = Controller(universal_callbacks=clear)
    light_control.start(starting())
    light_control.sleep(2.1)
    light_control.stop_all()
    light_control.start(speaking())
    light_control.sleep(3)
    light_control.stop_all()
    light_control.start(questionswarning())
    light_control.sleep(2)
    light_control.stop_all()

