# -*- coding: utf-8 -*-

#################################################################
#################################################################
#
# Copyright (c) 2013 by
# Zürcher Hochschule der Angewandten Wissenschaften (ZHAW)
#
# Author:      Konstantin Benz
# Created:     13/08/13   
# Last update: 14/08/13
#
# Poll Process Execution
# ----------------------
#
# This Python class polls execution state of all OpenStack
# services on one node and writes the results in a shared file.
#
#
#################################################################
#################################################################

import subprocess, random, csv

##################################################################
# Method to test if process is executing
# REQUIRES: process name or pid, method
# RETURNS: boolean, execution state of process
#
# process: name or pid of process
# method: search method (0: by name, 1: by pid)

def is_process_running(process, method = 0):
    ps = subprocess.Popen("ps -A x", shell=True, stdout=subprocess.PIPE)
    ps_pid = ps.pid
    output = ps.stdout.read()
    ps.stdout.close()
    ps.wait()
    for line in output.split("\n"):
        if line != "" and line != None:
            fields = line.split()
            pid = fields[0]
            pname = fields[4]
            if((pname == "/usr/bin/python")|(pname == "python")):
                pname = fields[5]

            if(method == 0):
                #print pname
                if(process in pname):
                    return True
            else:
                if(pid == process):
                    return True
    return False


#################################################################
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

#################################################################
# Method to write execution state of processes into a CSV-file
# REQUIRES: list of execution states, processes, csv file
# RETURNS: nothing
#
# exec_states: list of execution states
# processes: list of processes
# process_file: csv file where execution states are written to

def write_states(exec_states, processes, process_file="/vagrant/processes.csv"):
    #init_file(processes)
    #new_states = list()
    with open(process_file, 'wb') as csvfile:
        #statereader= csv.reader(csvfile, delimiter=' ',
        #                         quotechar='|', quoting=csv.QUOTE_MINIMAL)
        statewriter = csv.writer(csvfile, delimiter=' ',
                                 quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for index in xrange(len(exec_states)):
            process, state = exec_states[index]
            #old_row = statereader.next()
            #old_state = False
            #if(old_row[1] != None):
            #    old_state = old_row[1]
            new_state = [process, state]
            #print old_state
            #if(old_state == False)|(old_state == 'False'):
            #    new_state = [process, state]
            #print new_state
            #new_states.append(new_state)
    #with open(process_file, 'wb') as csvfile:
        
        #for new_state in new_states:
            statewriter.writerow(new_state)

#################################################################
# Method to init csv file
# REQUIRES: list of processes, csv file
# RETURNS: nothing
#
# processes: list of processes
# process_file: csv file to initialize

def init_file(processes, process_file="/vagrant/processes.csv"):
    with open(process_file, 'wb') as csvfile:
        initwriter = csv.writer(csvfile, delimiter=' ',
                                 quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for process in processes:
            init_row = [process, False]
            initwriter.writerow(init_row)
        
        

##################################################################
# MAIN CODE:
processes = ("keystone-all",
             "glance-api","glance-registry",
             "quantum-server","quantum-linuxbridge-agent",
             "quantum-dhcp-agent","quantum-l3-agent",
             "quantum-metadata-agent",
             "libvirtd",
             "nova-api","nova-cert","nova-compute",
             "nova-conductor","nova-consoleauth",
             "nova-novncproxy","nova-scheduler",
             "iscsi_eh","iscsid",
             "cinder-api","cinder-schedule","cinder-volume",
             "apache2","memcached")
exec_states = poll_process_state(processes)
print exec_states
write_states(exec_states, processes)
