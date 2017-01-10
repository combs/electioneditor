#!/bin/bash
SCRIPT=/home/pi/git/electioneditor/electioneditor.py

trap "echo exiting...;sleep 3; exit 1" SIGTERM SIGINT SIGHUP EXIT


echo "starting `basename $SCRIPT`:"
ls -l $SCRIPT
while sleep 1
do python2.7 $SCRIPT
echo Exited $?...
done
