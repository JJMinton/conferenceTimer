# conferenceTimer
Control software for raspberry pi to provide a timing functionality for parallel conference sessions.
Controllers are provided for monitor display and traffic light system

Server synchronisation is also included, where the program will update to changes in the schedule file and the new program will be loaded after restart.

### Requirements
* \>Python3.5 with pandas
* internet connection (for correct time and file syncing)
* XDG-compliant desktop environment (for program auto-start)

### To do
* screen display format
* correct light codes and behaviour
* empty schedule behaviour
* prevent light flashes with schedule update


## Auto-start
The auto-start must occur after the user has logged in and the window manager is loaded because it starts a GUI.
XDG-compliant desktop environment, such as GNOME or KDE, will auto-start all *.desktop files in locations including ~/.config/autostart. This method requires all addresses to absolute. A more robust approach may be to run as a systemd application.

The .desktop file should look like
```
[Desktop Entry]
Type=Application
Exec=/path/to/python3.5 /path/to/repo/file_change_handler.py
```
A version is provided in the ./scripts folder and can be copied or symlinked to ~/.config/autostart after modification.
This implementation assumes that the repo is located at `$HOME/conferenceTimer` and python3.5 is on the path.


## Schedule sync and program restart
A restart of the control loops occur when a new schedule is detected, using watchdog.
Syncronisation to a server can be achieved with an rsync script and called by cron or systemd.
If rsync is used, the --inplace flag is required to triger watchdog events.

Rsync script (`sync.sh`) and systemd timer files (`sync-schedule.timer` and `sync-schedule.service`) are included in `./scripts`.
The latter can be copied or symlinked to `/etc/systemd/system` after modification.
These scripts assume that the conferenceTimer repo is located at `$HOME/conferenceTimer` and the username is `pi`.

NOTE: an ssh key will have to be set up between the local host and the server using ssh-keygen
On the local host run `ssh-keygen' to generate key.
Then copy the new key to remote using `ssh-copy-id -i ~/.ssh/id_rsa.pub <remote-address>`.

## Time synchronisation
Time synchronisation is achieved with ntp run from systemd.

## SSH configuration (recommended)
It is recommended to set up and ssh server so that the raspberry pis can be accessed easily for fixes.
This can be achieved by...

## Pin layout
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
