control software for raspberry pi to provide a timing funcitonality for parrallel conference sessions.
controllers provided for mointor display and traffic light system

## Requirements
* \>Python3.5 with pandas
* internet connection (for correct time and file syncing)
* XDG-compliant desktop environment (for program auto-start)

## Todo
* document and implement time update
* trigger watchdog from rsync
* run rsync on startup
* document rsync on startup
* screen display format
* logging


# Auto-start
The auto-start must occur after the user has logged in and the window manager is loaded because it starts a gui.
XDG-compliant desktop environment, such as GNOME or KDE, will autostart all *.desktop files in locations including ~/.config/autostart

Using this approach, a file containing
```
[Desktop Entry]
Type=Application
Exec=/path/to/python3.5 /path/to/repo/file_change_handler.py
```

# Schedule sync and program restart

Auto-start is also necessary for code and schedule syncronisation.
I will come back to this.


# Time synchronisation

todo


# Pin layout

Marked pins are the default configuratin; however, config.py should be checked for specific implementation.
```
 -----------
 | sd card |
 -----------

3v3 power         1 : o o : 2         5v power
BCM 2 (SDA)       3 : o + : 4         5v power
BCM 3 (SCL)       5 : o - : 6           Ground
BCM 4 (GPCLK0)    7 : o o : 8     BCM 14 (TXD)
Ground            9 : o o : 10    BCM 15 (RXD)
BCM 17           11 : o o : 12   BCM 18 (PWMO)
BCM 27           13 : o o : 14          Ground 
BCM 22           15 : o o : 16          BCM 23
3v3 power        17 : o o : 18          BCM 24
BCM 10 (MOSI)    19 : o o : 20          Ground 
BCM 9 (MISO)     21 : o o : 22          BCM 25
BCM 11 (SCLK)    23 : o o : 24     BCM 8 (CE0)
Ground           25 : o o : 26     BCM 7 (CE1)
BCM 0 (ID_SD)    27 : o o : 28   BCM 1 (ID_SC)
BCM 5            29 : o o : 30          Ground
BCM 6            31 : o o : 32   BCM 12 (PWMO)
BCM 13 (PWM1)    33 : o o : 34          Ground
BCM 19 (MISO)    35 : o G : 36          BCM 16
BCM 26           37 : o O : 38   BCM 20 (MOSI)
Ground           39 : o R : 40   BCM 21 (SCLK)

          --------------
          |  usb ports |
          --------------
```
