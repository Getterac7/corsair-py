'''This module provides access to spatial hashing classes for storing and retrieval of objects in a 2d or 3d space.
Much of this code comes from: http://www.gamedev.net/reference/snippets/features/spatialHash/
Author: Brice Wallace

'''

class HashMap2D():
	''' Description: A hash table for storing and retrieval of points (x/y tuples) and/or Rect objects (x/y/width/heigh).
	Attributes: cell_size, grid
	'''
	def __init__(self, cell_size):
		''' HashMap(cell_size) -> HashMap
		cell_size:	The size (width and height) of each "bucket" for storing objects.
		Returns:	HashMap object.
		
		Description:	Efficiency of the HashMap will greatly depend on this number and will vary from project to project depending on how sparse your objects are.
		'''
		self.cell_size = cell_size
		self.grid = {}	#Start with an empty dictionary.
		
	def _hash(self, point):
		''' _hash(point) -> (x,y)
		point:	A tuple (x,y) of world coordinates.  Point must be an indexable object.
		Returns:	A tuple containing the HashMap bucket index.
		
		Description:	Convert x,y coordinates into a bucket index.
		'''
		return int(point[0]/self.cell_size), int(point[1]/self.cell_size)
	
	def insertRect(self, rect, object):
		''' insertRect(rect)
		rect:	
		object:	
		Returns:	None
		
		Description:
		'''
		if not rect:	#Make sure rect exists.
			print "Warning: object %s did not have a rect." % (object)
			return
		
		#Hash the minimum and maximum points.
		min, max = self._hash(rect.topleft), self._hash(rect.bottomright)
		
		#Iterate over the rectangular region.
		for i in xrange(min[0], max[0]+1):
			for j in xrange(min[1], max[1]+1):
				self.grid.setdefault( (i, j), [] ).append( object )	#Append to each intersecting cell.
		
	def queryRect( self, rect ):
		''' queryRect(rect)
		rect:	
		Returns:	A list of objects.
		
		Description:	
		'''
		s = set()	#Create a set to store objects (so we don't have duplicates).
		
		#Hash the minimum and maximum points.
		min, max = self._hash(rect.topleft), self._hash(rect.bottomright)
		
		#Iterate over the rectangular region.
		for i in xrange(min[0], max[0]+1):
			for j in xrange(min[1], max[1]+1):
				try:
					s.update( self.grid[(i,j)] )	#Add items to the set.
				except KeyError:	#(i,j) didn't exist in the dictionary.
					pass
		
		#Convert the set to a list and return it.
		return list( s )
		
	def removeRect( self, rect, object ):
		''' removeRect(rect, object)
		rect:	
		object:	
		Returns:	None
		
		Description:	
		'''
		if not rect:	#Make sure rect exists.
			print "Warning: A Rect was not passed with object (%r)." % (object)
			return
		
		#Hash the minimum and maximum points.
		min, max = self._hash(rect.topleft), self._hash(rect.bottomright)
		
		#Iterate over the rectangular region.
		for i in xrange(min[0], max[0]+1):
			for j in xrange(min[1], max[1]+1):
				try:
					self.grid[(i,j)].remove( object )	#Delete object from each bucket.
				except KeyError:	#Bucket didn't exist.
					continue
				except ValueError:	#Object didn't exist in the bucket.  This shouldn't happen unless the player moved and wasn't added to HashMap.
					print "Warning: Couldn't find object (%r) with Rect (%r) in HashMap." % (object, rect)

if __name__ == '__main__':
	import random
	import time
	
	from pygame import Rect
	
	NUM_POINTS = 10000
	GRID_SIZE = 50
	
	print "Creating %d rects for insertion." % (NUM_POINTS)
	points = []
	for i in xrange(NUM_POINTS):
		points.append( Rect(random.random()*1000, random.random()*1000, 32, 32) )
	
	print "Creating HashMap with grid size of %d." % (GRID_SIZE)
	hashmap = HashMap2D(GRID_SIZE)
	
	total = time.time()
	T = time.time()	#Start timer
	
	for pt in points:
		hashmap.insertRect( pt, pt.top )
	
	try:
		print "%d rect inserts per second." % (NUM_POINTS/(time.time()-T))
	except:
		print "Infinite rect inserts per second."
	
	T = time.time()	#Start timer
	
	for pt in points:
		hashmap.queryRect( pt )
		
	try:
		print "%d rect queries per second." % (NUM_POINTS/(time.time()-T))
	except:
		print "Infinite rect queries per second."
	
	T = time.time()	#Start timer
	
	for pt in points:
		hashmap.removeRect( pt, pt.top )
		
	try:
		print "%d rect removes per second." % (NUM_POINTS/(time.time()-T))
	except:
		print "Infinite rect removes per second."
	
	
	
	print "TOTAL TIME: %f seconds" % (time.time()-total)