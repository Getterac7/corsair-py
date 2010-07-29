import cPickle

import pygame
from pygame.constants import *

import gui
import states

class HighScore( gui.Drawable ):
	def __init__( self, pos ):
		gui.Drawable.__init__( self, pos )
		
		try:	#Save the new score.
			f = open( 'highscores.dat', 'r' )	#Open file.
			self.scores = cPickle.load( f )	#Unpickle high scores.
			f.close()	#Close file.
			
			#Create a bunch of TextFields
			self.drawables = []
			i=0
			for scr,nam in self.scores:
				txt = gui.TextField( self.pos + Vector.Twin( 0, (i*15) ) )
				txt.setText( nam.ljust(20) + str(scr).rjust(5) )
				self.drawables.append( txt )
				i += 1
			
		except IOError:
			print "Could not open highscores.dat for reading."
			raise IOError
		
	def checkScore( self, score ):
		''' Check if score will go on high score list
		Returns:	True if score should go on high scores list, else False.
		'''
		return (score > self.scores[-1][0])
	
	def draw( self, screen ):
		pass
	
	def insertScore( self, newName, newScore ):
		if checkScore( newScore ):
			self.scores.append( ( newScore, newName ) )	#Add the score and name to the list.
			self.scores.sort(reverse=True)	#Sort descending
			self.scores.pop()	#Drop the lowest score
			
			try:	#Save the new score.
				f = open( 'highscores.dat', 'w' )	#Open file.
				cPickle.dump( self.scores, f )	#Write Pickle'd high scores to file.
				f.close()	#Close file.
			except:
				print "Could not open highscores.dat for writing."
				raise SystemExit
	
	
	
class GameOver(states.State):
	
	def __init__(self,driver,screen,score):
		states.State.__init__(self,driver,screen)
		self.newScore = score
		self.highScoreTable = None
		
	def draw(self,screen):
		#Draw High Score table
		return
	
	def init(self):
		try:
			self.highScoreTable = HighScore( Vector.Twin( 350, 50 ) )
		except:	#High Score file didn't exist, back to main screen
			self._driver.done()
			
		if( self.checkScore(self.newScore) ):	#If new score goes on the high score table
			#Insert score with blank name
			#Allow user to type name
			pass
		else:
			#Display scores
			pass
		
	def keyEvent( self, key, unicode, pressed ):
		if( pressed ):
			playing = PlayingGameState(self._driver,self.screen)
			self._driver.replace(playing)
			
	def setMessage(self, message):
		self.message = message
		self.msgImage = self.messageFont.render(message, 0, (255,255,255))
		