import datetime
import topList
class binnedTopList:
	"""
		binnedTopList is a class for managing topList rankings of datetimes based on a metric.
		
		Once constructed with binnedTopList(), new values can be considered for the list
		with self.consider(eventName), with a new list being created for each binSize.
		
		self.report(outputLocation=outputLocation,includeScore=True) will write the
		contents of all topLists to a file at string location outputLocation. Must
		finalize before reporting if recent intervals are to be included.
		
		self.report(outputLocation=None) will print the lists to the screen. Must
		finalize before reporting if recent intervals are to be included.
		
		variables:
			hourLists	        list, each element is a topList
			binTimes	        list, contains the datetime start of each topList
			currentHourStart	datetime start of the current time interval
			currentHour         list, contains each datetime in the current time interval
			binSize             integer # of seconds each topList will be responsible for
			listLength			number of top rankings to maintain
			intervalLength		integer # of seconds to score activity during
	"""
	def __init__(self,listLength=10,binSize=86400,intervalLength=3600):
		self.hourLists = list()
		self.binTimes = list()
		self.currentHourStart = None
		self.currentHour = list()
		self.binSize = binSize
		self.intervalLength = intervalLength
		self.listLength = listLength
		
	def consider(self,eventDateTime):
		# Consider adding the event to the relevant list
		if self.currentHourStart == None:
			self.binTimes.append(eventDateTime)
			self.currentHourStart = eventDateTime
			newHourList = topList.topList(listLength=self.listLength,isDate=True)
			self.currentHour.append(eventDateTime)
			newHourList.consider(eventDateTime,len(self.currentHour))
			self.hourLists.append(newHourList)
		else:
			timeDelta = eventDateTime - self.currentHourStart
			timeDelta = abs(int(timeDelta.total_seconds()))
			if timeDelta < self.binSize:
				# Add to hour list and consider hour for top list
				self.currentHour.append(eventDateTime)
				self.removeOldEventsBTL(eventDateTime)
				self.hourLists[len(self.hourLists)-1].consider(eventDateTime,len(self.currentHour))
			else:
				self.finalize()
				# Create a new bin and add to the list
				self.binTimes.append(eventDateTime)
				self.currentHourStart = eventDateTime
				newHourList = topList.topList(listLength=self.listLength,isDate=True)
				self.currentHour = list()
				self.currentHour.append(eventDateTime)
				newHourList.consider(eventDateTime,len(self.currentHour))
				self.hourLists.append(newHourList)
	
	def report(self,outputLocation=None,includeScore=True):
		scoreReport = ''
		if outputLocation == None:
			print('Maximums saved for ' + str(len(self.binTimes)) \
				+ ' bins.\n Bin Start Times:')
			for binTime in self.binTimes:
				print binTime
			for topListNum in range(0,len(self.hourLists)):
				self.hourLists[topListNum].report(includeScore=includeScore)
		else:
			with open(outputLocation,'a') as outputFile:
				outputFile.seek(0)
				outputFile.truncate()
				outputFile.write('Maximums saved for ' + str(len(self.binTimes)) \
				+ ' bins.\n Bin Start Times:')
				for binTime in self.binTimes:
					outputFile.write(binTime)
			for topListNum in range(0, len(self.hourLists)):
				self.hourLists[topListNum].report(outputLocation=outputLocation,\
				includeScore=includeScore, truncateFile=False)
				
	def finalize(self):
		# Empty remaining events in lastHour for consideration
		remainingHours = len(self.currentHour)
		for remainingHour in range(0,remainingHours):
			requestDateTime = self.currentHour.pop(0)
			self.hourLists[len(self.hourLists)-1].consider(requestDateTime,len(self.currentHour)+1)
	
	def removeOldEventsBTL(self, datetimeEvent):
		# remove old events
		for event in self.currentHour:
			timeDifference = datetimeEvent - event
			timeDifference = abs(int(timeDifference.total_seconds()))
			if timeDifference > self.intervalLength:
				self.currentHour.remove(event)
			else:
				break
