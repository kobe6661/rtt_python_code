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
# Fabric file 2
# -------------------
#
# This fabfile is required to perform recovery time test actions
# on node 2. It acts as interface to the OpenStack node.
#
# The following actions can be done:
# - Start random shutdown of OpenStack service on guest machine
# - Poll service status on guest machine
#   and write updated service status in shared file
# - Check service status in shared file 
# - Cleanup by restarting all OpenStack services on guest machine
#
#################################################################
#################################################################

from fabric.api import *

env.password  = 'vagrant'
env.hosts = ['vagrant@grizzly2']


def outage():
    output = sudo("python /vagrant/start_outage.py")
    print output

def poll():
    output = sudo("python /vagrant/poll_processes.py")
    print output

def check():
    output = sudo("python /vagrant/check_crm.py")
    print output

def cleanup():
    output = sudo("python /vagrant/cleanup.py")
    print output
