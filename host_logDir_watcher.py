"""
host_logDir_watcher.py
Monitor a directory for file additions (in this case, logs) to be copied in another directory
"""

import os
import time

import win32file
import win32con

# 
# The list of VMs name to monitor 
# vm_name
#
# The path to be watched is passed in the masterconfig.py (Sorry larman)
# path_to_watch
#
#	The log file to copy
# log_filename
# 
# Where to save the log
# path_to_sync_log

ACTIONS = {
	"Created" : 1,
	"Deleted" : 2,
	"Updated" : 3,
	"Renamed from something" : 4,
	"Renamed to something" : 5
}
# permission request to read a directory
FILE_LIST_DIRECTORY = 0x0001


def dirWatcherWorker(dir_to_watch, tag, log_filename, path_to_sync_log):
	handle_to_Dir = win32file.CreateFile (
		dir_to_watch,
		FILE_LIST_DIRECTORY,
		win32con.FILE_SHARE_READ | win32con.FILE_SHARE_WRITE | win32con.FILE_SHARE_DELETE,
		None,
		win32con.OPEN_EXISTING,
		win32con.FILE_FLAG_BACKUP_SEMANTICS,
		None
	)

	while 1:
		#
		# ReadDirectoryChangesW takes a previously-created
		# handle to a directory, a buffer size for results,
		# a flag to indicate whether to watch subtrees and
		# a filter of what changes to notify.
		results = win32file.ReadDirectoryChangesW (
			handle_to_Dir,
			1024,
			False,
			win32con.FILE_NOTIFY_CHANGE_FILE_NAME,
			None,
			None
		)
		print "events! " + str(len(results))

		new_log_present = len([i for i in results if i[0] == ACTIONS["Renamed to something"] and i[1] == log_filename]) > 0

		if new_log_present:
			fromPath = os.path.join(dir_to_watch, log_filename)
			print "new log present!" + fromPath
			now = "{:.0f}".format(time.time()) 		# likely to cause concurrency bug, if the time is set back in the host system
			toPath= os.path.join(path_to_sync_log,  now + "_"+ tag + ".log")
			print "copying to " + toPath
			win32file.CopyFile(fromPath, toPath, 1)
