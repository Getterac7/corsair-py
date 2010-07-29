import Vector
from math import cos, sin, radians, pi

class Matrix:
	def __init__( self, rows, cols=None ):
		if( cols ):	#Given the dimentions of a zero matrix
			self.data = [[0 for x in range(cols)] for y in range(rows)]
		else:	#Given only 'rows'
			if rows.__class__ == list:
				self.data = rows
			else:
				msg = "The data (%s) of type (%s) passed to Matrix.Matrix() can not be used to create a new Matrix." % ( str(rows), rows.__class__ )
				raise TypeError, msg
		
	def __getitem__( self, key ):
		return self.data[key]
		
	def __mul__(self, val):
		matrix2 = None
		if val.__class__ == Vector.Twin:	#Turn the vector into a Matrix
			matrix2 = val.getMatrix()
		elif val.__class__ == Matrix:
			matrix2 = val
		else:	#Not a Vector or a Matrix... abort!
			print "Can't multiply class", val.__class__, "with class", Matrix
			return None
		
		
		# Matrix multiplication
		if len(self.data[0]) != len(matrix2.data):
			# Check matrix dimensions
			print 'Matrices must be m*n and n*p to multiply!'
		else:
			# Multiply if correct dimensions
			new_matrix = Matrix(len(self.data), len(matrix2.data[0]))
			for i in range(len(self.data)):
				for j in range(len(matrix2.data[0])):
					for k in range(len(matrix2.data)):
						new_matrix[i][j] += self.data[i][k]*matrix2.data[k][j]
			return new_matrix
		
	def __repr__( self ):
		#Return matrix data for recreating the matrix.
		return "Matrix.Matrix(%s)" % (str(self.data))
		
	def __str__( self ):
		#Return a human readable string representation of the matrix.
		out = ''
		for row in self.data:
			out += str(row) + '\n'
		return out[0:-1]	#Cut off the last new line character.

	def CCWRotationDeg( self, t ):
		return self.CCWRotationRad( radians( t ) )
	
	def CCWRotationRad( self, t ):
		if (t % (pi/2)) == 0:	#We are rotating by a 90 degree increment (aka whole numbers!).
			rot = Matrix( [ [int(cos(t)), int(sin(t))], [int(-sin(t)), int(cos(t))] ] )
		else:	#Use floating point math.
			rot = Matrix( [ [cos(t), sin(t)], [-sin(t), cos(t)] ] )
		return rot*self
	
	def CWRotationDeg( self, t ):
		return self.CWRotationRad( radians( t ) )
	
	def CWRotationRad( self, t ):
		if (t % (pi/2)) == 0:	#We are rotating by a 90 degree increment (aka whole numbers!).
			rot = Matrix( [ [int(cos(t)), int(-sin(t))], [int(sin(t)), int(cos(t))] ] )
		else:	#Use floating point math.
			rot = Matrix( [ [cos(t), -sin(t)], [sin(t), cos(t)] ] )
		return rot*self
	
	def toVector( self ):
		if len(self.data) == 2:
			return Vector.Twin( self[0][0], self[1][0] )
		else:
			return None
		
	def zero( self ):
		#Zero the matrix data.
		for i in xrange(len(self.data)):
			for j in xrange(len(self.data[0])):
				self.data[i][j] = 0

if __name__ == '__main__':
	print 'Running tests...'
	
	print 'Creating a 2x1 matrix with data (position data):'
	south = Matrix( [[-8], [5]] )
	print 'south='
	print south
	print ''
	
	print 'east = south.CCWRotationDeg(90):'
	east = south.CCWRotationDeg(90)
	print 'east='
	print east
	print ''
	
	print 'west = south.CWRotationDeg(90):'
	west = south.CWRotationDeg(90)
	print 'west='
	print west
	print ''
	
	print 'south.CCWRotationDeg(45):'
	print south.CCWRotationDeg(45)