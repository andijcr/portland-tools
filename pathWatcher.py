"""pathwatcher.py - Monitor a directory for file additions / deletions
Watch a named directory for any new or removed files. More sophisticated
 notifications could be added, for example looking for changes in file
 sizes etc. It doesn't seem possible to determine from the system call
 *which* files were added or removed, so the simple expedient is adopted
 of listing all files before waiting and then comparing with the
 equivalent list when notified.
"""

import os
import time

import win32file
import win32con

#
# The path to be watched is passed in the masterconfig.py (Sorry larman)
# path_to_watch

from masterconfig import *

print "Watching %s at %s" % (path_to_watch, time.asctime ())

ACTIONS = {
	"Created" : 1,
	"Deleted" : 2,
	"Updated" : 3,
	"Renamed from something" : 4,
	"Renamed to something" : 5
}
# permission request to read a directory
FILE_LIST_DIRECTORY = 0x0001

handle_to_Dir = win32file.CreateFile (
	path_to_watch,
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

	new_log_present = len([i for i in results if i[0] == ACTIONS["Renamed to something"] and i[1] == log_filename]) > 0

	if new


	for action, file in results:
		full_filename = os.path.join (path_to_watch, file)
		print full_filename, ACTIONS.get (action, "Unknown")