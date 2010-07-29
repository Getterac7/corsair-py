import Vector

class Camera:
	def __init__( self, screenVec, posVec=Vector.Twin(0,0) ):
		self.pos = posVec
		self.screenSize = screenVec
		self.halfScreenSize = screenVec/2
		
	def center( self, pos ):
		self.pos = pos-self.halfScreenSize
		
	def move( self, dx, dy ):
		self.x += dx
		self.y += dy

