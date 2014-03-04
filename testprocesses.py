import subprocess, random

##################################################################
# Method to test if process is executing
# REQUIRES: process name or pid, method
# RETURNS: boolean, execution state of process
#
# process: name or pid of process
# method: search method (0: by name, 1: by pid)

def is_process_running(process, method = 0):
    ps = subprocess.Popen("ps -A", shell=True, stdout=subprocess.PIPE)
    ps_pid = ps.pid
    output = ps.stdout.read()
    ps.stdout.close()
    ps.wait()
    for line in output.split("\n"):
        if line != "" and line != None:
            fields = line.split()
            pid = fields[0]
            pname = fields[3]

            if(method == 0):
                if((pname == process)|(pname == process+"d")):
                    return True
            else:
                if(pid == process):
                    return True
    return False


##################################################################
# Method to poll execution state of processes
# REQUIRES: list of process names
# RETURNS: list of process names and execution states
#
# processes: list of process names

def poll_process_state(processes):
    exec_states = list()
    for process in processes:
        row = list()
        exec_state = is_process_running(process)
        row.append(process)
        row.append(exec_state)
        exec_states.append(row)
    return exec_states


##################################################################
# Method to shutdown a process
# REQUIRES: process name
# RETURNS: nothing
#
# process: process name

def shutdown(process):
    command = "sudo service " + process + " stop" 
    message = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    output = message.stdout.read()
    message.stdout.close()
    message.wait()
    print output
    

##################################################################
# Method to shutdown a random process in a list
# REQUIRES: list of process names
# RETURNS: nothing
#
# processes: list of process names

def random_shutdown(processes):
    num_processes = len(processes)
    print num_processes
    select = random.randint(0, num_processes-1)
    print select
    for index in xrange(len(processes)):
        process = processes[index]
        #check if random select higher than probability
        if index == select:
            print "Shutdown of "+ process
            shutdown(process)
            break
        else:
            print "No shutdown."
            continue
        
##################################################################
# Method to restart a process
# REQUIRES: process name
# RETURNS: nothing
#
# process: process name

def restart(process):
    command = "sudo service " + process + " restart" 
    message = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    output = message.stdout.read()
    message.stdout.close()
    message.wait()
    print output
    
##################################################################
# Method to restart all processes
# REQUIRES: list of process names
# RETURNS: nothing
#
# processes: list of process names

def restart_all(processes):
    for index in xrange(len(processes)):
        process = processes[index]
        print "Restart of "+ process
        restart(process)


processes = ("keystone",
             "glance-api","glance-registry",
             "quantum-server","quantum-plugin-linuxbridge-agent",
             "quantum-dhcp-agent","quantum-l3-agent",
             "quantum-metadata-agent",
             "libvirt-bin",
             "nova-api","nova-cert","nova-compute",
             "nova-conductor","nova-consoleauth",
             "nova-novncproxy","nova-scheduler",
             "iscsitarget","open-iscsi",
             "cinder-api","cinder-scheduler","cinder-volume",
             "apache2","memcached")
exec_states = poll_process_state(processes)
print exec_states
