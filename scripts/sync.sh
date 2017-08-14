#!/bin/sh
rsync jjm61@jjm.nz:~/conferenceTimer/ ~/conferenceTimer -rt --delay-updates --exclude-from=$HOME/conferenceTimer/scripts/sync_exclude.txt
