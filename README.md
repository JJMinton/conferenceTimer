# conferenceTimer
control software for raspberry pi to provide a timing funcitonality for parrallel conference sessions.

TODO:
x write watch script (script that checks locally for schedule file changes)
x write lights control (program that issues running lights commands at given system times)
x write screen control (program that displays count down timer to a screen)
x integrate watch, and control scripts
_ run rsync to update files from server
x raspberry pi light control
x raspberry pi screen control
_ run on startup
_ add auto time update
x externalise config

x format and timing check script
_ screen display format

#Auto-start



# Pin layout
Marked pins are the default configuratin; however, config.py should be checked for specific implementation.
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
