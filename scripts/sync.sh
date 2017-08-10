#!/bin/sh
rsync jjm61@jjm.nz:~/conferenceTimer/* $HOME/conferenceTimer -r --inplace --exclude-from=$HOME/conferenceTimer/scripts/sync_exclude.txt
