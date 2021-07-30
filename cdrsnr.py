###############################
##           cdrsnr          ##
##            v1.0           ##
##         Python 2.7        ## 
##       By Matt Rienzo      ## 
##      Based heavily on     ##
## Single_Number_Reporter.py ##
##     By Redemption.Man     ##
###############################

##################################################################################################
## The Script parses a CDR file and an creates a csv file with all calls made and	        ##
## received by a single number, also includes calls that may have been forwarded		##
## on to that number.										##
##												##
## usage: Phone_Number_Reporter.py [-h] --input INPUT --phonenumber PHONENUMBER			##
## optional arguments:										##
##   -h, --help           		show this help message and exit				##
##   -i, --input INPUT         		CDR file input (must be csv)				##
##   -n, --phonenumber PHONENUMBER    	Phone number regex to report on (remember to add 9 if   ##
##                                      external number)                                        ##
##   -o, --output                       Output file                                             ##
##   -x, --exclude                      Excluded number regex pattern                           ##
##   -l, --list-forwarded               List number regex as forwarded to number                ##
##################################################################################################

import csv
import argparse
import os.path
import time
import sys

from re import search

## CLI switches
parser = argparse.ArgumentParser(prog='cdrsnr', description='Reads Cisco CDR files and creates a simplfied call record for a single number')
parser.add_argument('-i', '--input', required=True, help='CDR file input (must be csv)')
parser.add_argument('-n','--phonenumber', required=True, help='Phone number regex to report on (remember to add 9 if external number)')
parser.add_argument('-o', '--output', required=False, help='Output file')
parser.add_argument('-x', '--exclude', required=False, help='Excluded number regex pattern')
parser.add_argument('-l', '--list-forwarded', required=False, help='List number regex as forwarded to number')
args = parser.parse_args()

## END of CLI switches

## Var's that can be changed
if len(args.output) == 0:
    outputfile = "Call_Report_"+args.phonenumber+".csv"
else:
    outputfile = args.output

## Variable translations
excludedNumberStr = args.exclude
forwardedNumberStr = args.list_forwarded

## arg.input is the input file
phonenumber = args.phonenumber

#create parsed output cvs 
parsedoutput = open(outputfile, 'w+')
parsedoutput.write("Incoming/Outgoing,Start of Call,End of Call,Duration (Seconds),Caller Number,Call Answered By,Call Forwarded To\n")
## columns needed:
## starting at zero
## 2 - globalCallID_callId
## 4 - dateTimeOrigination
## 9 - callingPartyNumber
## 47 - dateTimeConnect
## 48 - dateTimeDisconnect
## 55 - Duration
## 30 - finalCalledPartyNumber
## 115 - destMobileDeviceName
#### Opens and parses cdr extracting only records with the gateway
duration = 0
calldirection = "Incoming"
totalcalls = 0

# Update this to iterate a list of DNs
with open(args.input, 'Ur') as f:
	print "Collecting all records for " + phonenumber + "\n\n"
	parserreader = csv.reader(f)
	for row in parserreader:
		callmatch = 0
                forwardMatch = 0
		# caller number
                if search(phonenumber, row[8]) and not search(excludedNumberStr, row[30]):
			calldirection = "Outgoing"
			callmatch = 1
                # Forwarded number
                if search(forwardedNumberStr, row[8]) and not search(excludedNumberStr, row[30]):
                        calldirection = "Outgoing"
                        callmatch = 1
                        forwardMatch = 1
		# called number
                if search(phonenumber, row[30]) and not search(excludedNumberStr, row[8]):
			calldirection = "Incoming"
			callmatch = 1
                # Forwarded number
                if search(forwardedNumberStr, row[30]) and not search(excludedNumberStr, row[8]):
                        calldirection = "Incoming"
                        callmatch = 1
                        forwardMatch = 1
		if callmatch == 1:
			totalcalls = totalcalls + 1
			callmatch = 0
			convertstarttime = time.localtime(float(row[4]))
			convertendtime = time.localtime(float(row[48]))
			startofcall = str(convertstarttime.tm_year)+"/"+str(convertstarttime.tm_mon)+"/"+str(convertstarttime.tm_mday)+" "+str(convertstarttime.tm_hour) +":"+ str(convertstarttime.tm_min)
			endofcall = str(convertendtime.tm_year)+"/"+str(convertendtime.tm_mon)+"/"+str(convertendtime.tm_mday)+" "+str((convertendtime.tm_hour)) +":"+ str(convertendtime.tm_min)
			
			parsedoutput.write(calldirection+","+startofcall+","+endofcall+","+row[55]+","+row[8]+","+row[115]+(","+row[30] if forwardMatch == 1 else ",no forward")+"\n")

parsedoutput.close()
f.close() 
if totalcalls == 0:
	sys.exit("***ERROR*** No calls found for phone number "+phonenumber)
else:
	print "Total calls for "+phonenumber+" : "+str(totalcalls)
