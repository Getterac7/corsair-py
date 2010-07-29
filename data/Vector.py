from math import atan2,degrees
from itertools import imap
from operator import mul

from pygame import Rect

import Matrix

class Twin():
	'''
	Attributes: _x, _y
	'''
	def __init__( self, x, y = None ):
		if y == None:
			y = x[1]
			x = x[0]
		self._x = x
		self._y = y
	
	def __add__( self, val ):
		if val.__class__ == Rect:	#Rect
			return Rect( self._x + val.left, self._y + val.top, val.w, val.h )
		elif val.__class__ == int or val.__class__ == float or val.__class__ == long:	#Number
			return Twin( self._x + val, self._y + val )
		elif val.__class__ == Twin:	#Twin
			return Twin( self._x + val._x, self._y + val._y )
		elif val.__class__ == tuple:	#Tuple
			return Twin( self._x + val[0], self._y + val[1] )
		elif val.__class__ == list:	#List
			return Twin( self._x + val[0], self._y + val[1] )
		else:	#Something else
			msg = "unsupported operand type(s) for +: '%s' and '%s'" % (self.__class__.__name__, val.__class__.__name__)
			raise TypeError, msg
	
	def __div__( self, val ):
		if val.__class__ == int or val.__class__ == float or val.__class__ == long:	#Number
			return Twin( self._x / val, self._y / val )
		elif val.__class__ == Twin:	#Twin
			return Twin( self._x / val._x, self._y / val._y )
		elif val.__class__ == tuple:	#Tuple
			return Twin( self._x / val[0], self._y / val[1] )
		elif val.__class__ == list:	#List
			return Twin( self._x / val[0], self._y / val[1] )
		else:	#Something else
			msg = "unsupported operand type(s) for /: '%s' and '%s'" % (self.__class__.__name__, val.__class__.__name__)
			raise TypeError, msg
		
	def __eq__( self, val ):
		if val.__class__ == Twin:
			return self._x == val._x and self._y == val._y
		else:
			return False
		
	def __ge__( self, other ):
		if other.__class__ == int or other.__class__ == float or other.__class__ == long:
			return self.len() >= other
		if self.len() >= other.len():
			return True
		else:
			return False
		
	def __getitem__( self, key ):
		l = [self._x, self._y]
		return l[key]
		
	def __gt__( self, other ):
		if other.__class__ == int or other.__class__ == float or other.__class__ == long:
			return self.len() > other
		if self.len() > other.len():
			return True
		else:
			return False
		
	def __hash__( self ):
		return hash(str(self._x).zfill(10) + str(self._y).zfill(10))
		
	def __le__( self, other ):
		if other.__class__ == int or other.__class__ == float or other.__class__ == long:
			return self.len() <= other
		if self.len() <= other.len():
			return True
		else:
			return False
		
	def __lt__( self, other ):
		if other.__class__ == int or other.__class__ == float or other.__class__ == long:
			return self.len() < other
		if self.len() < other.len():
			return True
		else:
			return False
	
	def __mul__( self, val ):
		if val.__class__ == int or val.__class__ == float or val.__class__ == long:	#Number
			return Twin( self._x * val, self._y * val )
		elif val.__class__ == Twin:	#Twin
			return Twin( self._x * val._x, self._y * val._y )
		elif val.__class__ == tuple:	#Tuple
			return Twin( self._x * val[0], self._y * val[1] )
		elif val.__class__ == list:	#List
			return Twin( self._x * val[0], self._y * val[1] )
		else:	#Something else
			msg = "unsupported operand type(s) for *: '%s' and '%s'" % (self.__class__.__name__, val.__class__.__name__)
			raise TypeError, msg
		
	def __ne__( self, val ):
		if self._x != val._x or self._y != val._y:
			return True
		else:
			return False
		
	def __nonzero__( self ):
		if self._x or self._y:
			return True
		else:
			return False
		
	def __repr__( self ):
		return "Vector.Twin(%s, %s)" % (self._x, self._y)
	
	def __setitem__( self, key, val ):
		if key == 0:
			self._x = val
		elif key == 1:
			self._y = val
		else:
			msg = "list index out of range"
			raise IndexError, msg
			
	
	def __str__( self ):
		return "<%s, %s>" % ( self._x, self._y )
	
	def __sub__( self, val ):
		if val.__class__ == int or val.__class__ == float or val.__class__ == long:	#Number
			return Twin( self._x - val, self._y - val )
		elif val.__class__ == Twin:	#Twin
			return Twin( self._x - val._x, self._y - val._y )
		elif val.__class__ == tuple:	#Tuple
			return Twin( self._x - val[0], self._y - val[1] )
		elif val.__class__ == list:	#List
			return Twin( self._x - val[0], self._y - val[1] )
		else:	#Something else
			msg = "unsupported operand type(s) for -: '%s' and '%s'" % (self.__class__.__name__, val.__class__.__name__)
			raise TypeError, msg
		
	def __trunc__( self ):
		return Twin( int(self._x), int(self._y) )

	def CCWRotationDeg( self, t ):
		return self.toMatrix().CCWRotationDeg( t ).toVector()
	
	def CCWRotationRad( self, t ):
		return self.toMatrix().CCWRotationRad( t ).toVector()
	
	def CWRotationDeg( self, t ):
		return self.toMatrix().CWRotationDeg( t ).toVector()
	
	def CWRotationRad( self, t ):
		return self.toMatrix().CWRotationRad( t ).toVector()
	
	def dot( self, other ):
		return sum( imap( mul, self, other ) )
	
	def len( self ):
		return ( self._x ** 2 + self._y ** 2 ) ** 0.5
	
	def normalize( self ):
		vlen = self.len()
		if vlen == 0:
			return
		self._x = self._x / vlen
		self._y = self._y / vlen
	
	def set( self, val ):
		if val.__class__ == tuple:	#Tuple
			self._x = val[0]
			self._y = val[1]
		elif val.__class__ == list:	#List
			self._x = val[0]
			self._y = val[1]
		elif val.__class__ == Twin:	#Twin
			self._x = val[0]
			self._y = val[1]
		else:	#Something else
			msg = "unsupported operand type for set(): '%s'" % (val.__class__.__name__)
			raise TypeError, msg
		
	def toDegrees( self ):
		return degrees(atan2(self._y, self._x))
		
	def toRadians( self ):
		return atan2(self._y, self._x)
		
	def toMatrix( self ):
		return Matrix.Matrix( [ [self._x], [self._y] ] )
	
	def toTuple( self ):
		return ( self._x, self._y )

if __name__ == '__main__':
	print 'Running tests...'
	err = False
	
	#Twin + Twin
	x = Twin(2,3)
	y = Twin(6,7)
	if x+y != Twin(8,10):
		print 'Error calculating Vector.Twin + Vector.Twin'
		err = True
	
	#Twin + Rect
	x = Twin(1,2)
	y = Rect(13,18,34,55)
	if x+y != Rect(14,20,34,55):
		print 'Error calculating Vector.Twin + pygame.Rect'
		err = True
	
	#Twin + tuple
	x = Twin(5,6)
	y = (10, 15)
	if x+y != (15,21):
		print 'Error calculating Vector.Twin + tuple'
		err = True
		
	x = Twin(5,6)
	y = Matrix.Matrix(2,2)
	x+y
	
	print 'Done'
	if not err:
		print 'No errors!'
	