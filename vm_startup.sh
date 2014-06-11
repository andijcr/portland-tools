#!/bin/bash

echo "-------------------------------"
echo "[$date] Starting ITGSend, ITGRecv"

DIR="/home/administrator/portland-tools"

nohup $DIR/ITGRecv.sh &

for sendcommand in $DIR/`hostname`_send_*.sh
do
	nohup $sendcommand &
done
