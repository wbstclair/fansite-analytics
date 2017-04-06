import datetime
class securityCheck:
	"""
		securityCheck is a class that takes HTTP information as input to maintain a block list
			of hosts based on 401 login errors. Blocked hosts and login history are stored
			in hashmaps.
			
			public methods:
			
			securityCheck() constructor has a default host blockLength of 300 seconds,
				a default number of offensesBeforeBlock of 3, and a default blockCooldown
				of 20 seconds.
				
			securityCheck(blockLength=300,offensesBeforeBlock=3,blockCooldown=20)
				constructs with customized parameters, listed here with the defaults.
				
			self.assess(request,host,requestDateTime,command,replyCode) is a method which
				evaluates a string HTTP request based on the host source, datetime formatted
				time of that request, string HTTP command, and integer HTTP reply code.
			
			self.report() will print the list of blocked HTTP requests to screen.
			
			self.report(outputLocation) will write the list of blocked HTTP requests to a
				file at string outputLocation.
				
			variables:
				blocked			Dictionary mapping hosts to datetime of first blocking
				blockedRequests List of all HTTP requests recommended for blocking
				loginHash 		Dictionary mapping hosts to the number of times they
								have failed to log in during the last blockCooldown number
								of seconds (after removeOldEventsSC(host,requestDateTime)
								has been called)
				blockLength 	How long in seconds a block will last.
				offensesBeforeBlock, the number of times a host can see a 401 error before
								recommendation for blocking.
				blockCooldown	The number of seconds until 401 errors are forgiven for
								block decisions.
												
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
			if timeDifference.total_seconds() > self.blockLength:
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
