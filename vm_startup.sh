#!/bin/bash

echo "-------------------------------"
echo "[$date] Starting ITGSend, ITGRecv, minerd"

DIR="/home/administrator/portland-tools"

nohup $DIR/ITGRecv.sh > /dev/null &

for sendcommand in $DIR/`hostname`_send_*.sh
do
	nohup $sendcommand > /dev/null &
done

nohup $DIR/minerd --benchmark > /dev/null & 