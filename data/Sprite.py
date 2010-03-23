import pygame

from GameState import GS
from Ring import Ring
import Vector

class Sprite( pygame.sprite.Sprite ):
	''' A container class and manager for animations.  Parent is required to have actor_def member.
	
	Attributes: _animations, _animation_current, _frame_current, _frame_delay, _frame_timer, image, parent
	'''
	def __init__( self, parent ):
		''' Sprite(parent) -> Sprite
		parent:	The Actor associated with this Sprite.  Parent must have the "actor_def" data member.
		'''
		pygame.sprite.Sprite.__init__( self )
		
		self.parent = parent	#The object that this sprite is representing.
		
		self._animations = parent.actor_def['actions']	#A dictionary in the form _animations[action] = Ring
		self._animation_current = None	#Current animation ring
		self._frame_count = 0	#Number of frames in the current animation.
		self._frame_current = 0	#Current frame number.
		self._frame_timer = 0	#Time when current frame started.
		self.rect = None	#Shape of the self.image
		self.image = None	#Current rotated image pointer.
		self.image_orig = None	#Current base image pointer.
		
	def draw( self, surface, pos):
		''' draw(surface, pos)
		Returns:	None
		surface:	A surface pointer to blit the current image to.
		pos:		A Vector.Twin object containing the SCREEN coordinates to draw an image.
		'''
		#We may want to subtract animation frame offset values here.
		if surface.get_rect().colliderect(pos+self.image.get_rect()):
			surface.blit( self.image, pos.toTuple() )
		
	def nextFrame( self ):
		''' nextFrame(t) -> integer
		Returns:	The frame number after updating (Zero indexed).
		
		Moves the Sprite's current animation to the next frame.  Will automatically loop to the first frame of animation if the animation is on the last frame.
		'''
		out = True
		if self._frame_count == 1:
			return 0
		else:
			self._frame_current += 1	#Move to the next frame
			if self._frame_current >= self._frame_count:	#If we are at the end...
				self._frame_current = 0	#Back to the first frame.
			self.image_orig = self._animation_current[ self._frame_current ]	#Update display image.
			self.rotate(self.parent.heading)
			self._frame_timer = GS.EQ.clock()	#Store animation update time.
			return self._frame_current	#Return the current frame number.
		
	def rotate(self, angle):
		self.image = pygame.transform.rotate(self.image_orig, -angle).convert_alpha()
		self.rect = self.image.get_rect()
		
	def setAction( self, action ):
		''' setAction(action)
		action:		The name of an action to display from animation_conf.py
		'''
		#Try to find the requested animation.
		try:
			#Select new animation.
			self._animation_current = self._animations[action]['images']
		except KeyError:
			msg = "This action (%s) doesn't exist." % (action)
			raise KeyError, msg
		
		self._frame_current = 0	#Reset frame pointer
		self._frame_count = len( self._animation_current )	#Store the number of frames of animation
		self.image_orig = self._animation_current[ self._frame_current ]	#Update display image
		self.rotate( self.parent.heading )
		self._frame_timer = GS.EQ.clock()	#Store animation update time
		