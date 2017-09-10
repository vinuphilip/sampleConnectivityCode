#!/usr/bin/python

import imaplib
import sys
from netaddr import *

fileNameTemp = '/Users/Bency/listIPPorts_temp'
fileName = '/Users/Bency/listIPPorts'

initialIPPortDict = {}
IPPortDictWithIPExtrapolated = {}
IPPortDictWithPortExtrapolated = {}

def checkIPAndExtrapolateIt(ip, port):

	# here the assumption is that dash "-" is present in the last quadrant 
	if "-" in ip:
		ipQudrant = ip.split('.')
		ipQ1 = ipQudrant[0]
		ipQ2 = ipQudrant[1]
		ipQ3 = ipQudrant[2]
		ipQ4WithDash = ipQudrant[3]
		ipQ4DashList = ipQ4WithDash.split('-')
		ipQ4DashRange1 = ipQ4DashList[0].strip()
		ipQ4DashRange1 = int(ipQ4DashRange1)
		ipQ4DashRange2 = ipQ4DashList[1].strip()
		ipQ4DashRange2 = int(ipQ4DashRange2) + 1
		for ipQ4 in xrange(ipQ4DashRange1, ipQ4DashRange2):
			extIp = ipQ1 + "." + ipQ2 + "." + ipQ3 + "." + str(ipQ4)
		#	print extIp  	
			IPPortDictWithIPExtrapolated[extIp] = port
	else:
		ipRange = IPNetwork(ip)
		for ip in ipRange:
		#	print ip	
			IPPortDictWithIPExtrapolated[ip] = port


def checkPortAndExtrapolateIt(ip, port):
	#print("The ip and port passed are %s and %s :" % (ip, port))
	tempList = []
	if "-" in port:
		portRangeDashList = port.split('-')
		portRange1 = portRangeDashList[0].strip()
		portRange1 = int(portRange1)
		portRange2 = portRangeDashList[1].strip()
		portRange2 = int(portRange2) + 1


		for portList in  xrange(portRange1, portRange2):
			tempList.append(portList)
		
		if ip in IPPortDictWithPortExtrapolated:
			if IPPortDictWithPortExtrapolated[ip] is None:
				IPPortDictWithPortExtrapolated[ip] = tempList
			else:
				tempList.append(IPPortDictWithPortExtrapolated[ip])
				IPPortDictWithPortExtrapolated[ip] = list(set(tempList))
		else:
			IPPortDictWithPortExtrapolated[ip] = tempList
	else:
#		print("The port is %s :" % port)
		tempList.append(port)
		IPPortDictWithPortExtrapolated[ip] = list(set(tempList))
			

		





with open(fileName,'r') as f:
	ipPortList = f.readlines()
f.close()

ipPortListStripped = [ ipPort.strip() for ipPort in ipPortList ]

for ipAndPort in ipPortListStripped:
	data = ipAndPort.split('|')
	ip= data[0].strip()
	port= data[1].strip()
	initialIPPortDict[ip] = port

for ip,ports  in initialIPPortDict.items():
	if "," in ip:
		iplist = ip.split(",")
		for ip in iplist:
			checkIPAndExtrapolateIt(ip, ports)
	else:
		checkIPAndExtrapolateIt(ip, ports)



for ip,ports in IPPortDictWithIPExtrapolated.items():
	#print ip,ports
	if "," in ports:
		portList = ports.split(",")
		for port in portList:
			checkPortAndExtrapolateIt(ip, port)
	else:
		checkPortAndExtrapolateIt(ip, ports)

print "======================"


for k,v in IPPortDictWithPortExtrapolated.items():
	print k,v
	
	
