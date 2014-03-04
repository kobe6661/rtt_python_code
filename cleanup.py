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
# Cleanup after test
# -------------------
#
# This Python class cleans up tasks performed by a recovery time
# test run. It restarts all OpenStack services on one node.
#
#
#################################################################
#################################################################

import subprocess, random
        
##################################################################
# Method to restart a process
# REQUIRES: process name
# RETURNS: nothing
#
# process: process name

def restart(process):
    checkstatus = "sudo service " + process + " status"
    restartcommand = "sudo service " + process + " restart" 
    message = subprocess.Popen(checkstatus, shell=True, stdout=subprocess.PIPE)
    output = message.stdout.read()
    message.stdout.close()
    message.wait()
    print output
    if('NOT running' in output)|('stop/waiting' in output)|('not' in output):
        subprocess.Popen(restartcommand, shell=True, stdout=subprocess.PIPE)
        print "Restart action"
    
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
restart_all(processes)
