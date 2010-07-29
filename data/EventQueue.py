import heapq

class EventQueue:
	'''A priority queue for Events.
	Returns: EventQueue object
	Functions: 
	Operators: 
	Attributes: events, t
	'''
	def __init__(self, time):
		self.events = []
		self.t = time
		
	def cancel_event( self, obj=None, func=None ):
		if obj and func:
			for k, e in enumerate(self.events):
				if e.obj == obj and e.func == func:
					del self.events[k]
		elif obj:
			for k, e in enumerate(self.events):
				if e.obj == obj:
					del self.events[k]
		elif func:
			for k, e in enumerate(self.events):
				if e.func == func:
					del self.events[k]
		else:
			print "Not enough parameters passed to EventQueue.cancel_event."
	
	def schedule(self, e):
		heapq.heappush( self.events, e)
		
	def has_event(self):
		if self.size() > 0:
			return True
		else:
			return False
		
	def process_event(self):
		'''Returns True if an Event is processed, else false'''
		if not self.has_event(): return False
		if self.events[0].time > self.t:
			return False
		else:
			heapq.heappop(self.events).process()
			return True
		
	def set_clock(self, t):
		self.t = t
		
	def move_clock(self, dt):
		self.t += dt
		
	def clock(self):
		return self.t
		
	def size(self):
		return len(self.events)
