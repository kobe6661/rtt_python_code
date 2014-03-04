# -*- coding: utf-8 -*-

#################################################################
#################################################################
#
# Copyright (c) 2013 by
# Zürcher Hochschule der Angewandten Wissenschaften (ZHAW)
#
# Author:      Konstantin Benz
# Created:     13/08/13   
# Last update: 13/08/13
#
# Simulate Outage
# -------------------
#
# This Python class shuts down a random OpenStack service on one
# node.
#
#
#################################################################
#################################################################

import subprocess, random

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
# MAIN CODE:
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
random_shutdown(processes)

