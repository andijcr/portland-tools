"""
host_log_recevier

uses ZeroMQ (ØMQ), in particular the python binding 'pyzmq', to collect log rows from a sender (installed in each guest vm)
"""

import time
import os
import shutil
import zmq

def receiverWorker(bind_addr, saveFilePath, exportPath, saveThresholdSecs):

	def backup(path, destinationPath):
		shutil.move(path, os.path.join(destinationPath, "{:.0f}".format(time.time()) + ".internal.log"))

	if os.path.exists(saveFilePath):
		backup(saveFilePath, exportPath)

	ctx = zmq.Context()
	sinker = ctx.socket(zmq.PULL)
	sinker.bind(bind_addr)

	save = open(saveFilePath, "w")

	lastTime = time.time()
	while True:
		save.write(sinker.recv_string() + "\n")
		if time.time() - lastTime > saveThresholdSecs:
			save.close()
			backup(saveFilePath, exportPath)
			save = open(saveFilePath, "w")
			lastTime=time.time()