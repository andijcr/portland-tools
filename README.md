portland-tools
==============
Tools for Portland - second project for BigData [http://www.dia.uniroma3.it/~torlone/bigdata/]

setup for the Windows Server 2008 hosts 
---------------------------------------
python 2.7, pywin32, pyzmq

```
python host_main_service.py install
```

installs a windows service that uses host_log_receiver.py and host_logDir_watcher.py to receive log data from the virtual machines, and to save a copy of vmware log file 

configuration is contained in a file named `masterconfig.py` that has to be added in the folder using this codeblock as template:

```python
""" parameters to pass to host_logDir_watcher """
vm_name = ["v58a", "v58b"]  #change this
#name of the machines, same as the dir where vmware stores them
path_to_watch = "C:\\Users\\Public\\Documents\\Shared Virtual Machines\\"
#root folder of the vm (vmware workstation 10)
log_filename = "vmware-0.log"
#log filename not in use by the vm (vmvorkstation 10)
path_to_sync_log = "C:\\Users\\Public\\Documents\\portland-logs\\"  #folder must exist
#central location to save the log 

""" parameters to pass to host_log_receiver """
port = "5558"
#free tcp port
bind_addr="tcp://*:" + port
#address to listen to (receive from everywhere)
saveFilePath= "C:\\Users\\Public\\Documents\\internal.log"
#filename (complete) to sink the received rows
exportPath = path_to_sync_log
#path where to save closed log
saveThresholdSecs = 3600
#how often should be the log rotated?

""" parameters for guest_log_sender """
save_addr="tcp://localhost:" + port         #change this with the ip address of the host machine
#ip address + port of host_log_receiver 
sleepSecs = 1
#how many seconds between two readings? 
```

setup for the Ubuntu Server 14.04 guests
----------------------------------------
python 2.7, pyzmq, bash, (D-ITG)[http://traffic.comics.unina.it/software/ITG/], stress, minerd

```bash
./vm_startup.sh
```
starts minerd to saturate the virtual cpu
and uses D-ITG (one ITGRecv, multiple ITGSend) to saturate the vlan connecting the guest machines

```bash
python guest_log_sender.py `hostname`
```
starts the log sender that at regural intervals pushes the name of the processes running in the machine to the host machine.
the processes are collected via `ps axhk +args o args`, and each log row has format

```
[seconds since unix epoch] | [vm_tag] | [processes as json array]
```

a masterconfig.py must be provided, with a similar structure of the windows one.
