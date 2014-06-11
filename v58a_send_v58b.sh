#!/bin/bash

address="172.16.2.58"

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
