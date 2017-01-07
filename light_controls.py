import asyncio;
import time;

import RPi.GPIO as gpio

gpio.setmode(gpio.BCM)
gpio.setup(23, gpio.OUT)
gpio.setup(24, gpio.OUT)
gpio.setup(25, gpio.OUT)

def switch_light(cmd_str):
    if cmd_str[0] == 'g':
        gpio.output(23, 0)
    elif cmd_str[0] == '-':
        gpio.output(23, 1)
    else:
        raise ValueError('incorrect input for green light')
    if cmd_str[1] == 'o':
        gpio.output(24, 0)
    elif cmd_str[1] == '-':
        gpio.output(24, 1)
    else:
        raise ValueError('incorrect input for orange light')
    if cmd_str[2] == 'r':
        gpio.output(25, 0)
    elif cmd_str[2] == '-':
        gpio.output(25, 1)
    else:
        raise ValueError('incorrect input for red light')


from controller import Controller

async def starting():
    while True:
        switch_light('-or');
        await asyncio.sleep(2.0);
async def speaking():
    while True:
        switch_light('g--');
        await asyncio.sleep(2.0);
async def speakingwarning():
    while True:
        switch_light('go-');
        await asyncio.sleep(2.0);
async def questions():
    while True:
        switch_light('-o-');
        await asyncio.sleep(2.0);
async def questionswarning():
    while True:
        switch_light('---');
        await asyncio.sleep(1.0);
        switch_light('-o-');
        await asyncio.sleep(1.0);
async def change():
    while True:
        switch_light('--r');
        await asyncio.sleep(2.0);
def clear():
    switch_light('---');


if __name__ == '__main__':

    light_control = Controller(universal_callbacks=clear)
    light_control.start(starting())
    light_control.sleep(4.1)
    light_control.stop_all()
    light_control.start(speaking())
    light_control.sleep(6)
    light_control.stop_all()
    light_control.start(questionswarning())
    light_control.sleep(4)
    light_control.stop_all()

