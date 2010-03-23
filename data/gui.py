from pygame.constants import *

from common import SubclassShouldImplement
from GameState import GS
import Vector

class Drawable:
	'''loc is a tuple of the upper-left location to draw this drawable at.
	Subclasses (such as Mouseable) depend on the first two entries being x,y'''
	def __init__( self, pos=None ):
		self.pos = pos

	def draw( self, screen ):
		raise SubclassShouldImplement
		
	def setPosition( self, pos ):
		self.pos.set( pos )

class Mouseable( Drawable ):
	'''bounds is the location and width/height of the mouseable.  If None,
	  we're everywhere!'''
	def __init__( self, bounds = None ):
		Drawable.__init__( self, bounds )
		self.buttonState = MOUSEBUTTONUP

	def mouseEvent( self, event ):
		"event is a MOUSE* event, this routine decodes it and calls one of the subs"
		x,y = event.pos
		if event.type == MOUSEBUTTONDOWN:
			self.buttonState = event.type
			self.mouseDownEvent( x, y )
		elif event.type == MOUSEBUTTONUP:
			self.buttonState = event.type
			self.mouseUpEvent( x, y )
		elif event.type == MOUSEMOTION:
			if self.buttonState == MOUSEBUTTONDOWN:
				self.mouseDragEvent( x, y )
			self.mouseMoveEvent( x, y )

	def mouseDownEvent( self, x, y ):
		pass

	def mouseUpEvent( self, x, y ):
		pass

	def mouseDragEvent( self, x, y ):
		pass

	def mouseMoveEvent( self, x, y ): 
		pass

class Keyable:
	def __init__( self, keys = None ):
		'''keys is a list of keys that this will respond to.  If None, it listens
		to everything'''
		self.keys = keys
		
		if(keys):
			self.pressed = {}
			for k in self.keys:
				self.pressed[k] = 0

	def maskEvent( self, key, unicode, pressed ):
		if self.keys:
			if not key in self.keys:
				return
		self.keyEvent( key, unicode, pressed )

	def keyEvent( self, key, unicode, pressed ):
		raise SubclassShouldImplement

class Updateable:

	def update( self ):
		raise SubclassShouldImplement
	
class TextField(Drawable):
	def __init__( self, pos = ( 0, 0 ), color = ( 255, 255, 255 ) ):
		pos = Vector.Twin( pos )
		Drawable.__init__( self, pos )
		self.color = color
		
		self.textImage = None
		self.textFont = GS.font_digital
		self.setText( "" )
		
	def draw( self, screen ):
		if( self.textImage and self.pos ):
			screen.blit( self.textImage, self.pos.toTuple() )
			
	def getText( self ):
		return self.text
	
	def setFont( self, font ):
		self.textFont = font
	
	def setText( self, text ):
		self.text = text
		self.textImage = self.textFont.render( text, 0, self.color )