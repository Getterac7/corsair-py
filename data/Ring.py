class Ring:
	'''
	Attributes: _data
	'''
	def __init__( self, l ):
		if not len( l ):
			raise "ring must have at least one element"
		self._data = l

	#For printing itself (prints all items)
	def __repr__( self ):
		return repr( self._data )

	#Gets the length of _data
	def __len__( self ):
		return len( self._data )

	#Retuns an object at an arbitrary position
	def __getitem__( self, i ):
		return self._data[ i % len( self ) ]
		
	#Returns the first object in _data
	def first( self ):
		return self._data[0]

	#Returns the last object in _data
	def last( self ):
		return self._data[-1]
	
	#Returns the data in list form
	def toList( self ):
		return self._data

	#Rotates the data forward one.  first() becomes first()+1.  last() becomes first()
	def turn( self ):
		last = self._data.pop( -1 )
		self._data.insert( 0, last )
