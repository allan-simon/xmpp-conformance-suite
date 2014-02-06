#!/bin/bash

#quick and dirty script to run the test
#the timeout command is herde to stop the script execution after 5 second
#to avoid errors that would make a script to not disconnect (and finish)
for TEST in *.py ; do timeout 5 python $TEST ; done
