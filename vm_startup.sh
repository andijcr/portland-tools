#!/bin/bash

echo "-------------------------------"
echo "[$date] Starting ITGSend, ITGRecv"

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

nohup $DIR/ITGRecv.sh &

for sendcommand in $DIR/`hostname`_send_*.sh
do
	nohup $sendcommand &
done
