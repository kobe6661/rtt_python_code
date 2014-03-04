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
# Check Execution File
# --------------------
#
# This Python class checks if all OpenStack services are available
# in the cluster by checking the shared process_file
#
#
#################################################################
#################################################################

import csv

##################################################################
# Method to check availability of all OpenStack processes
# REQUIRES: process file
# RETURNS: boolean, if OpenStack is available or not
#
# process_file: shared file where execution states of OpenStack
# services are stored

def is_available(process_file="/vagrant/processes.csv"):
    with open(process_file, 'rb') as csvfile:
        statereader = csv.reader(csvfile, delimiter=' ',
                                 quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for row in statereader:
            available = row[1]
            #print available
            if(available=='False'):
                return False
    return True

##################################################################
# MAIN CODE:
output = is_available()
print output

