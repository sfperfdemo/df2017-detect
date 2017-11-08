#!/bin/bash
#######################################################
# Script:
#    sendAlerts.sh
# Usage:
#    ./sendAlerts.sh <INPUTFILE>
#      INPUTFILE - full path to the file with alerts
# Description:
#    Send chatter alerts
# Authors:
#    Jasmin Nakic,    jnakic@salesforce.com
#    Samir Pilipovic, spilipovic@salesforce.com
#######################################################

INPUTFILE=$1

# Send chatter alert for each line in the input message file
cat $INPUTFILE|while read msg; do
  python alrt.py \"$msg\"
done
