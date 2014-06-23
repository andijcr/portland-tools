"""
guest_log_sender.py
requires as argument a tag, used to identify log lines
requires pyzmq, the python binding for ZeroMQ
to generate log lines, merge a timestamp (seconds from the epoch), the tag, and a json array of the results of "ps axhk +args o args" (every process with the arguments from all the users in the system, ordered by process name)
"""

import masterconfig

save_addr=masterconfig.save_addr
sleepSecs = masterconfig.sleepSecs

ps_args = ["ps", "axhk", "+args", "o", "args"]

import time
import zmq
import sys
import subprocess
import json
import sys

logTag= sys.argv[1]

ctx = zmq.Context()

saver = ctx.socket(zmq.PUSH)
saver.connect(save_addr)

while True:
	startTime = time.time()

	processes= subprocess.check_output(ps_args).decode("utf-8").splitlines()

	toSendData = "{:.0f}".format(startTime) + ' | ' + logTag + ' | ' + json.dumps(processes)

	saver.send_string(toSendData)

	finishTime = time.time()

	deltaToNextCycle= sleepSecs - (finishTime - startTime)
	if deltaToNextCycle > 0:
		time.sleep(deltaToNextCycle)
