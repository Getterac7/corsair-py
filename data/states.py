import sys

from pygame.locals import *
import pygame

from  common import SubclassShouldImplement
import gui #So we can have a common interface between gui stuff and state stuff.
from GameState import GS

class StateDriver:
	def __init__( self, screen ):
		self._states = []
		self._screen = screen
		GS.driver = self
		
	def done( self ):
		self._states.pop()
		self.getCurrentState().reactivate()
		
	def getCurrentState( self ):
		try:
			return self._states[ -1 ]
		except IndexError:
			raise SystemExit  #We're done if there are no states left.
		
	def getScreenSize( self ):
		return self._screen.get_size()
	
	def quit( self ):
		#Was 'raise SystemExit', but pychecker assumes any function that unconditionally raises an exception is abstract.
		sys.exit( 0 )
		
	def replace( self, state ):
		self._states.pop()
		self.start( state )
		
	def run( self ):
		#Init clock
		clock = pygame.time.Clock()
		
		#Set up some function pointers to speed things up.
		tick = clock.tick
		
		currentState = self.getCurrentState()
		while( currentState ):
			dt = tick(60)
			GS.EQ.move_clock(dt)
			
			# poll queue
			event = pygame.event.poll()
			while( event.type != NOEVENT ):
				if event.type == QUIT:
					currentState = None
					break
				elif event.type == KEYUP or event.type == KEYDOWN:
					if event.key == K_ESCAPE:
						currentState = None
						break
					if event.type == KEYUP:
						currentState.maskEvent( event.key, None, 0 )
					if event.type == KEYDOWN:
						currentState.maskEvent( event.key, event.unicode, 1 )
				elif (event.type == MOUSEMOTION):
					currentState.mouseEvent( event )
				elif ( event.type == MOUSEBUTTONDOWN or
					event.type == MOUSEBUTTONUP ):
						currentState.mouseEvent( event )
						
				event = pygame.event.poll()
				
			#Process events in event queue
			while GS.EQ.process_event(): pass
			
			self._screen.fill( ( 0, 0, 0 ) )
			if currentState:
				currentState.draw( self._screen )
				
				currentState.update()
				currentState = self.getCurrentState()
				
				pygame.display.flip()
				
	def start( self, state ):
		self._states.append( state )
		self.getCurrentState().activate()
		
class State( gui.Keyable, gui.Mouseable ):
	def __init__( self, driver, screen ):
		gui.Keyable.__init__( self ) # States listen to everything
		gui.Mouseable.__init__( self )
		self._driver = driver
		self.screen = screen
		
	def activate( self ):
		pass
	
	# maskEvent is handled by Keyable
	
	def keyEvent( self, key, unicode, pressed ):
		pass
	
	def draw( self, screen ):
		raise SubclassShouldImplement
	
	def reactivate( self ):
		pass
	
	def update( self ):
		pass
	
class GuiState( State ):
	def __init__( self, driver, screen ):
		State.__init__( self, driver, screen )
		self.drawables = []
		self.mouseables = []
		self.keyables = []
		self.updateables = []
		
	def add( self, item ):
		# Add to the appropriate list(s) based on type
		if(isinstance( item, gui.Drawable ) ):
			self.drawables.append( item )
		if(isinstance( item, gui.Mouseable ) ):
			self.mouseables.append( item )
		if(isinstance( item, gui.Keyable ) ):
			self.keyables.append( item )
		if(isinstance( item, gui.Updateable ) ):
			self.updateables.append( item )
			
	def draw( self, screen ):
		for drawable in self.drawables:
			drawable.draw( screen )
			
	def keyEvent( self, key, unicode, pressed ):
		for keyable in self.keyables:
			keyable.keyEvent( key, unicode, pressed )
			
	def mouseEvent( self, event ):
		x,y = event.pos
		for mouseable in self.mouseables:
			x1,y1 = mouseable.loc[0:2]
			try:
				w,h = mouseable.loc[2:4]
			except IndexError:
				w,h = self.screen.get_width(), self.screen.get_height()
			if ( x >= x1   and y >= y1 and
				 x <  x1+w and y <  y1+h ):
				mouseable.mouseEvent( event )
	def remove( self, item ):
		# Remove from the appropriate list(s) based on type
		if(isinstance( item, gui.Drawable ) ):
			self.drawables.remove( item )
		if(isinstance( item, gui.Mouseable ) ):
			self.mouseables.remove( item )
		if(isinstance( item, gui.Keyable ) ):
			self.keyables.remove( item )
		if(isinstance( item, gui.Updateable ) ):
			self.updateables.remove( item )
		
	def update( self ):
		for updateable in self.updateables:
			updateable.update()
			