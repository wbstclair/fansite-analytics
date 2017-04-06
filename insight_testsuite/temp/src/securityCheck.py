import datetime
class securityCheck:
	"""
		Class for managing rankings of names based on a metric.
	"""
	def __init__(self,blockLength=300,offensesBeforeBlock=3,blockCooldown=20):
		self.blocked = dict()
		self.blockedRequests = list()
		self.loginHash = dict()
		self.blockLength = blockLength
		self.offensesBeforeBlock = offensesBeforeBlock
		self.blockCooldown=blockCooldown
	
	def assess(self,request,host,requestDateTime,command,replyCode):
		allowRequest = True
		if host in self.blocked:
			timeDifference = requestDateTime - self.blocked[host]
			if timeDifference.total_seconds() > 300:
				self.blocked.pop(host)
			else:
				self.blockedRequests.append(request)
				allowRequest = False 
		if allowRequest:
			if command == 'POST':
				if replyCode == 401:
					self.considerBlock(host,requestDateTime)
				elif replyCode == 200:
					# Remove failed login records
					if host in self.loginHash:
						self.loginHash.pop(host)
				
	
	def considerBlock(self,host,requestDateTime):
		if host in self.loginHash:
			self.removeOldEventsSC(host,requestDateTime)
			self.loginHash[host].append(requestDateTime)
			if len(self.loginHash[host]) >= self.offensesBeforeBlock:
				self.blocked[host] = requestDateTime
		else:
			self.loginHash[host] = [requestDateTime]
	
	def report(self,outputLocation=None):
		if outputLocation == None:
			for blockedRequest in self.blockRequests:
				print blockedRequest
		else:
			with open(outputLocation,'a') as outputFile:
				outputFile.seek(0)
				outputFile.truncate()
				for blockedRequest in self.blockedRequests:
					outputFile.write(blockedRequest)

	
	def removeOldEventsSC(self, host, datetimeEvent):
		for event in self.loginHash[host]:
			timeDifference = datetimeEvent - event
			if int(timeDifference.total_seconds()) > self.blockCooldown:
				self.loginHash[host].remove(event)
			else:
				break
