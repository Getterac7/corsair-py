class Event:
	'''An Event object for calling functions now or in the future.
	Returns: Event object
	Functions: process
	Operators: <, <=, ==, !=, >=, >
	Attributes: obj, func, time
	'''
	def __init__(self, time, obj, func, args):
		'''
		time	-Time event should be called (milliseconds).
		obj		-Object to do the action on.
		func	-Function to call on object.
		args	-Arguments passed to function call.
		'''
		self.obj = obj
		self.func = func
		self.time = time
		self.args = args
		
	def __lt__(self, other):
		'''Implementation of < operator'''
		if self.time < other.time:
			return True
		else:
			return False
		
	def __le__(self, other):
		'''Implementation of <= operator'''
		if self.time <= other.time:
			return True
		else:
			return False
		
	def __eq__(self, other):
		'''Implementation of == operator'''
		if self.time == other.time:
			return True
		else:
			return False
		
	def __ne__(self, other):
		'''Implementation of != operator'''
		if self.time != other.time:
			return True
		else:
			return False
		
	def __gt__(self, other):
		'''Implementation of >= operator'''
		if self.time >= other.time:
			return True
		else:
			return False
		
	def __ge__(self, other):
		'''Implementation of > operator'''
		if self.time > other.time:
			return True
		else:
			return False
		
	def process(self):
		if self.func:
			if self.args:
				self.func( self.obj, self.args )
			else:
				self.func( self.obj )
	
		
