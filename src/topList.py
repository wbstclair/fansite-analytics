import datetime
class topList:
	"""
		Class for managing rankings of names based on a metric.
	"""
	def __init__(self,listLength=10,isDate=False):
		self.names = list()
		self.scores = list()
		self.listMinimum = 0
		self.memoHash = dict()
		self.listLength = listLength
		self.isDate = isDate
	
	
	def add(self,eventName,score):
		listLength = 30
		try:
			# If this trips ValueError, eventName isn't on the list
			prevIndex = self.names.index(eventName)
			# Remove from previous list, and add to the appropriate location
			self.names.remove(eventName)
			self.scores.remove(self.scores[prevIndex])
			self.add(eventName,score)
		except ValueError:
			valueAdded = False
			for currentIndex in range(0,len(self.scores)):
				if self.scores[currentIndex] < score:
					# Insert eventName
					self.names.insert(currentIndex, eventName)
					self.scores.insert(currentIndex, score)
					valueAdded = True
					break		
			if valueAdded == False:		
				self.names.append(eventName)
				self.scores.append(score)
			# Trim extra eventName, if present
			if len(self.scores) > self.listLength:
					self.names.pop()
					self.scores.pop()
			self.listMinimum = min(self.scores)
	
	def consider(self,eventName,scoreIncrement):
		if self.isDate:
			if scoreIncrement >= self.listMinimum:
				self.add(eventName,scoreIncrement)
		else: 
			if eventName in self.memoHash:
				self.memoHash[eventName] = self.memoHash[eventName] + scoreIncrement
			else:
				self.memoHash[eventName] = scoreIncrement
			if self.memoHash[eventName] >= self.listMinimum:
				self.add(eventName,self.memoHash[eventName])
	
	def report(self,outputLocation=None,includeScore=True):
		scoreReport = ''
		if outputLocation == None:
			for topNum in range(0,len(self.names)):
				if includeScore:
					scoreReport = ',' + str(self.scores[topNum])
				print nameFormat(self.names[topNum]) + scoreReport + '\n'
		else:
			with open(outputLocation,'a') as outputFile:
				outputFile.seek(0)
				outputFile.truncate()
				for topNum in range(0,len(self.names)):
					if includeScore:
						scoreReport = ',' + str(self.scores[topNum])
					outputFile.write(self.nameFormat(self.names[topNum]) + scoreReport + '\n')
	
	def nameFormat(self,name):
		if self.isDate:
			outputString = str(name)
		else:
			outputString = name
		return outputString
	
	def removeDuplicateEvents(self,recentEvent, eventScore, secondsBin):
		indicesToRemove = list()
		for eventNum in range(0,len(self.names)):
			timeDelta = recentEvent - self.names[eventNum]
			timeDelta = abs(int(timeDelta.total_seconds()))
			if timeDelta < secondsBin:
				if timeDelta > 0:
					if eventScore > self.scores[eventNum]:
						indicesToRemove.insert(0,eventNum)
		for eventNum in indicesToRemove:
			self.names.pop(eventNum)
			self.scores.pop(eventNum)
	
	def removeOldEvents(self, datetimeEvent, secondsOld):
		# remove old events
		for event in self.names:
			timeDifference = datetimeEvent - event
			if int(timeDifference.total_seconds()) > secondsOld:
				self.names.remove(event)
			else:
				break
