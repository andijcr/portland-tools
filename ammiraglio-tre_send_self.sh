#!/bin/bash

address="127.0.0.1"

while [ 1 ]
do
	toSend=$RANDOM
	let "toSend %= 8000"
	let "toSend += 7000"

	ITGSend -a $address -T TCP -O 20000 -u 1000 1500 -l /dev/null -t $toSend > /dev/null

	toSleep=$RANDOM
	let "toSleep %= 4"
	sleep $toSleep
done
