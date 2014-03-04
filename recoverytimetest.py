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
# Recovery Time Test
# -------------------
#
# This Python class measures the time Pacemaker takes to recover
# a two node OpenStack installation from outages of one OpenStack
# service.
#
# The following steps are performed during a test run:
# - Start random shutdown of OpenStack service on one
#   of the guest machines
# - Start timer on host machine
# - Repeatedly poll service status on guest machine
# - Write updated service status in shared file
# - Repeatedly poll service status in shared file 
#   until all services are up again
# - Stop timer on host machine
# - Store timer value in file
# - Stop service polling on guest machine
# - Cleanup by restarting all OpenStack services on guest
#   machine
#
#################################################################
#################################################################

import subprocess, csv, time

##################################################################
# Method to simulate outages and measure mean time to recovery
# REQUIRES: fabric file
# RETURNS: time to recover from outage
#
# fabfile: fabricfile needed to perform test on computer

def recovery_time_test(fabfile="fabfile.py"): #, fabfile2="fabfile2.py"):
    recovery_time = time.time()
    # Define shell commands that use fabric file
    start_outage = "fab -f "+ fabfile +" outage" 
    poll_processes = "fab -f "+ fabfile +" poll"
    #poll_processes = "fab -f "+ fabfile2 +" poll"
    check_crm = "fab -f "+ fabfile +" check"
    #check_crm2 = "fab -f "+ fabfile2 +" check"
    cleanup = "fab -f "+ fabfile +" cleanup"
    #cleanup2 = "fab -f "+ fabfile2 +" cleanup"

    # Start outage
    message = subprocess.Popen(start_outage, shell=True, stdout=subprocess.PIPE)
    output = message.stdout.read()
    message.stdout.close()
    message.wait()
    print output

    
    output2 = ""
    # Repeatedly poll while OpenStack is not available
    start = time.time()
    while('True' not in output2):
        # Poll execution states of processes
        message1 = subprocess.Popen(poll_processes, shell=True, stdout=subprocess.PIPE)
        output1 = message1.stdout.read()
        message1.stdout.close()
        message1.wait()
        print output1
        # check OpenStack availability
        message2 = subprocess.Popen(check_crm, shell=True, stdout=subprocess.PIPE)
        output2 = message2.stdout.read()
        message2.stdout.close()
        message2.wait()

    recovery_time = (time.time() - start)
    
    #Cleanup after test run
    message = subprocess.Popen(cleanup, shell=True, stdout=subprocess.PIPE)
    output = message.stdout.read()
    message.stdout.close()
    message.wait()
    print output
    #message2 = subprocess.Popen(cleanup2, shell=True, stdout=subprocess.PIPE)
    #output2 = message2.stdout.read()
    #message2.stdout.close()
    #message2.wait()
    #print output2

    return recovery_time

##################################################################
# Method to perform a batch of recovery time tests
# REQUIRES: number of test runs, results file, fabric file
# RETURNS: nothing
#
# testruns: number of test runs
# results_file: file to write results to
# fabfile: fabric file used in test

def batch_test(testruns=10, results_file="test.csv", fabfile="fabfile2.py"):
    with open(results_file, 'wb') as csvfile:
        resultwriter = csv.writer(csvfile, delimiter=' ',
                                 quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for index in xrange(testruns):
            recovery_time = recovery_time_test(fabfile)
            result_row = [index, str(recovery_time)]
            resultwriter.writerow(result_row)
            print "Completed test nr:\n---------------------\n"+str(index)
            print "Time expanded::::"+str(recovery_time)
    

##################################################################
# MAIN CODE:
#recovery_time = recovery_time_test("fabfile2.py")
#print "Test result is:\n-----------\n " + str(recovery_time)
batch_test(10, "/home/konstantin/lsa2_01-10.csv", "fabfile.py")
batch_test(10, "/home/konstantin/lsa2_11-20.csv", "fabfile.py")
batch_test(10, "/home/konstantin/lsa2_21-30.csv", "fabfile.py")
#batch_test(10, "/home/konstantin/ssg1_31-40.csv", "fabfile.py")
#batch_test(10, "/home/konstantin/ssg1_41-50.csv", "fabfile.py")
#batch_test(10, "/home/konstantin/ssg1_51-60.csv", "fabfile.py")
#batch_test(10, "/home/konstantin/ssg1_61-70.csv", "fabfile.py")
#batch_test(10, "/home/konstantin/ssg1_71-80.csv", "fabfile.py")
#batch_test(10, "/home/konstantin/ssg1_81-90.csv", "fabfile2.py")
#batch_test(10, "/home/konstantin/ssg1_91-100.csv", "fabfile2.py")
#batch_test(10, "/home/konstantin/ssg1_101-110.csv", "fabfile2.py")
#batch_test(10, "/home/konstantin/ssg1_111-120.csv", "fabfile2.py")
#batch_test(10, "/home/konstantin/ssg1_121-130.csv", "fabfile2.py")
#batch_test(10, "/home/konstantin/ssg1_131-140.csv", "fabfile2.py")
#batch_test(10, "/home/konstantin/ssg1_141-150.csv", "fabfile2.py")
