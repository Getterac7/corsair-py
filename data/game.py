try:
	import sys
	
	from pygame.locals import *
	import pygame

	import animation_conf
	import Camera
	from GameState import GS
	from playing import PlayingGameState
	import states
	
except ImportError, err:
	print "Couldn't load a module. %s" % ( err )
	sys.exit( 2 )
	
def main():
	
	screen = pygame.display.set_mode( GS.SCREEN_SIZE.toTuple(), DOUBLEBUF )
	
	GS.camera = Camera.Camera( GS.SCREEN_SIZE )
	animation_conf.init()
	
	driver = states.StateDriver( screen )
	title = TitleScreen( driver, screen )
	driver.start( title )
	driver.run()
	
class TitleScreen( states.State ):
	
	def __init__( self, driver, screen ):
		states.State.__init__( self, driver, screen )
		self.titleFont = pygame.font.Font( None, 92 )
		self.font = GS.font_text20
		
	def draw(self,screen):
		white = ( 255, 255, 255 )
		
		w,h = screen.get_size()
		surface = self.titleFont.render( "Corsair", 0, white )
		
		centerX = w/2 - surface.get_width()/2
		centerY = h*0.25 - surface.get_height()/2
		
		screen.blit( surface, ( centerX, centerY ) )
		
		surface = self.font.render( "A Mini-LD 16 entry.", 0, ( 128, 128, 128 ) )
		centerX = w/2 - surface.get_width()/2
		centerY = h/2 - surface.get_height()/2
		
		screen.blit( surface, ( centerX, centerY ) )
		
		surface = self.font.render( "Press any key to begin", 0, white )
		centerX = w/2 - surface.get_width()/2
		centerY = h*0.75 - surface.get_height()/2
		
		screen.blit( surface, ( centerX, centerY ) )
		
	def keyEvent( self, key, unicode, pressed ):
		if( pressed ):
			playing = PlayingGameState( self._driver, self.screen )
			self._driver.start( playing )
			playing.init()
			