"""
host_main_service.py: installs a new windows service that will execute 
host_log_receiver.py
	and
host_logDir_watcher.py
as workers, to receive and store data from the guest machines and to watch a dir for log rotation
"""

import time

#import pythoncom
import win32serviceutil
import win32service
import win32event
import servicemanager
#import socket


import masterconfig

import host_log_receiver

import host_logDir_watcher

class AppServerSvc (win32serviceutil.ServiceFramework):
	_svc_name_ = "Portland Log Saving"
	_svc_display_name_ = "Servizio di salvataggio dei log vmware per il progetto BigData Portland"
	has_to_stop = False;

	def __init__(self,args):
		win32serviceutil.ServiceFramework.__init__(self,args)
		self.hWaitStop = win32event.CreateEvent(None,0,0,None)

	def SvcStop(self):
		self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
		self.has_to_stop=True;
		win32event.SetEvent(self.hWaitStop)

	def SvcDoRun(self):
		servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
							  servicemanager.PYS_SERVICE_STARTED,
							  (self._svc_name_,''))
		self.main()

	def main(self):
		print "Watching %s at %s" % (masterconfig.path_to_watch, time.asctime())
		workers = []
		for vm in masterconfig.vm_name:
			dir_to_watch = os.path.join(masterconfig.path_to_watch, vm)
			p = multiprocessing.Process(target=host_logDir_watcher.dirWatcherWorker, args=(dir_to_watch, vm, masterconfig.log_filename, masterconfig.path_to_sync_log))
			p.start()
			workers.append(p)

		p=multiprocessing.Process(targer=host_log_receiver.receiverWorker args=(masterconfig.bind_addr, masterconfig.saveFilePath, masterconfig.exportPath, masterconfig.saveThresholdSecs))
		workers.append(p)
		
		while not has_to_stop:
			time.sleep(5)

		for p in workers:
			if p.is_alive():
				p.terminate()


if __name__ == '__main__':
	win32serviceutil.HandleCommandLine(AppServerSvc)