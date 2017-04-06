import datetime
class topList:
	"""
		topList is a class for managing rankings of names based on a metric. The top
		listLength number of rankings will be maintained, with all other names and scores
		summed in a hashmap self.memoHash. 
		
		Once constructed with topList(), new values can be considered for the list with
		self.consider(eventName, scoreIncrement). If using datetimes as names, and the
		constructor was called with isDate=True, only the scoreIncrement is used for the
		ranking (it is not added to a hashmapped sum).
		
		self.report(outputLocation=outputLocation,includeScore=True) will write the
		contents of names and scores to a file at string location outputLocation.
		
		self.report(outputLocation=None) will print the lists to the screen.
		
		variables:
			names		list, ordered from first to last by score
			scores		list, sorted largest to smallest
			listMinimum	smallest score on the list
			memoHash	dictionary mapping names to scores
			listLength	number of top rankings to maintain
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
			if self.scores[prevIndex] < score:
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
			if scoreIncrement >= self.listMinimum or len(self.scores) < self.listLength:
				self.add(eventName,scoreIncrement)
		else: 
			if eventName in self.memoHash:
				self.memoHash[eventName] = self.memoHash[eventName] + scoreIncrement
			else:
				self.memoHash[eventName] = scoreIncrement
			if self.memoHash[eventName] >= self.listMinimum \
			or len(self.scores) < self.listLength:
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
			outputString = name# + datetime.timedelta(hours=1)
			outputString = outputString.strftime("%d/%b/%Y:%H:%M:%S -0400")
			#outputString = str(name)
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
