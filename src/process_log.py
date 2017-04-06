"""
 Process log data to implement:
  1. List the top 10 most active host/IP addresses that have accessed the site.
		  output: 2nd argument		example: '../log_output/hosts.txt'
  2. Identify the 10 resources that consume the most bandwidth on the site.
		  output: 4th argument 		example: '../log_output/resources.txt'
  3. List the top 10 busiest (or most frequently visited) 60-minute periods.
        output: 3rd argument		example: '../log_output/hours.txt'
  4. Detect patterns of three failed login attempts from the same IP address over 20 seconds.
        Block for 5 minutes. 
        Log possible security breaches.
        output: 5th argument 		example: '../log_output/blocked.txt'

  input: 1st argument 				example: '../log_input/log.txt'
  
  dependencies:
  	topList.py
  	securityCheck.py
"""

import datetime
import sys
import topList
import securityCheck

def removeOldEvents(eventList, datetimeEvent, secondsOld):
	# remove old events
	for event in eventList:
		timeDifference = datetimeEvent - event
		if int(timeDifference.total_seconds()) > secondsOld:
			#print str(event)
			eventList.remove(event)
		else:
			break
	return eventList

# ./src/process_log.py 
#./log_input/log.txt
#./log_output/hosts.txt
#./log_output/hours.txt
#./log_output/resources.txt
#./log_output/blocked.txt
logInput = sys.argv[1]
hostsOutput = sys.argv[2]
hoursOutput = sys.argv[3]
resourcesOutput = sys.argv[4]
blockedOutput = sys.argv[5]

activeHosts = topList.topList()
activeContent = topList.topList()
activeHours = topList.topList(isDate=True)
securityGuard = securityCheck.securityCheck()

months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', \
'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
lastHour = list()

lineNum = 1
with open(logInput,'r') as logFile:
	for request in logFile:
		# Parse the request
		requestData = request.split()
		host = requestData[0]
		reqTime = requestData[3]
		fullTime = reqTime.replace('[','')
		reqTime = fullTime.split(':')
		requestDate = reqTime[0].split('/')
		hour = reqTime[1]
		minute = reqTime[2]
		second = reqTime[3]
		day = requestDate[0]
		month = months.index(requestDate[1])
		year = requestDate[2]
		timeZone = requestData[4]
		timeZone = timeZone.replace(']','')
		requestDateTime = datetime.datetime(int(year), \
		int(month),int(day),int(hour),int(minute),int(second))

		commandParse = request.split("'")[0]
		commandParse = commandParse[1]
		commandParse = commandParse.split()
		if len(commandParse) > 1:
			content = commandParse[1]
		else:
			content = ''
		bytes = requestData[len(requestData)-1]
		if bytes == '-':
			bytes = 0
		else:
			bytes = int(bytes)
		command=commandParse[0]
		replyCode = int(requestData[len(requestData)-2])
		
		activeHosts.consider(host,1)
		
		lastHour.append(requestDateTime)				
		lastHour = removeOldEvents(lastHour,requestDateTime, 3600)
		
		activeHours.consider(requestDateTime - datetime.timedelta(hours=1),len(lastHour))
		activeContent.consider(content,bytes)
		securityGuard.assess(request,host,requestDateTime,command,replyCode)

activeHosts.report(outputLocation=hostsOutput)
activeContent.report(outputLocation=resourcesOutput)
activeHours.report(outputLocation=hoursOutput)
securityGuard.report(outputLocation=blockedOutput)