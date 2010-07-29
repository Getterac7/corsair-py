import random, copy, math
from sys import exit

import pygame
from pygame.constants import *

import animation_conf
from done import GameOver
from Event import Event
from GameState import GS
import gui
import Sprite
from states import *
import Vector



''' Dynamically create new functions in the format:
	def NameFactory(j, a): Name( a[0], a[1], a[2], ... )
	Where Name is a class name defined in "lst", and a is a series of arguments for constructing an object of class Name.
	This is useful for creating many Factory functions to be used later by the Event system, since the Event system cannot create objects on its own.
'''
lst = [('Explosion', 2)]
for name,argCount in lst:
	data = 'def %sFactory(j, a):	%s(' % (name, name)
	for i in xrange( argCount ):
		data += 'a[%d],' % i
	data = data[:-1]	#Kill the trailing comma.
	data += ')'
	exec(data)	#Create the new function





		
		
		
		
		
class Entity(gui.Drawable, gui.Updateable):
	def __init__(self, pos, actor_def, parent=None, action=None):
		gui.Drawable.__init__(self,pos)
		GS.driver.getCurrentState().add( self )	#Make self visible
		
		if(parent):
			self.parent = parent
			self.heading = parent.heading	#Angle in degrees
			parent.children.append(self)	#Make sure we exist as a child to our parent.
		else:
			self.parent = None
			self.heading = 0
			
		self.actor_def = actor_def	#The animation and action definition dictionary.
		self.collidable = True	#Collisions are enabled by default
		self.radius = None	#The collision radius for the current image.  This will get filled when setAction() is called
		self.sprite = Sprite.Sprite(self)	#Create a sprite
		self.directionalVelocity = Vector.Twin(0,0)	#X,Y speed vector
		if(action):
			self.setAction( action )
			
		self.children = []
	
	def delete( self ):
		if self.parent:
			self.parent.children.remove(self)	#Remove self from parent's children
		GS.driver.getCurrentState().remove( self )	#Remove self from drawables list
		self.collisionsDisable()	#Make sure nothing else can collide with this object.
		
	def draw(self,screen):
		self.sprite.draw(screen, self.pos-self.sprite.rect.center-GS.camera.pos)
		
	def collided( self ):	#This function should probably be overridden by a subclass.
		self.collisionsDisable()	#Turn off collisions
		GS.EQ.schedule(Event(GS.EQ.clock()+500, self, Entity.collisionsEnable, None))	#Make an event to enable collisions in 500ms
		
	def collisionsDisable( self ):
		self.collidable = False
		
	def collisionsEnable( self ):
		self.collidable = True
		
	def setAction(self, action):
		self.action = action	#Switch to new action.
		self.radius = self.actor_def['actions'][action]['collision']	#Change the collision radius.
		self.delay = self.actor_def['actions'][action]['delay']	#Change the frame delay
		self.sprite.setAction( self.action )	#Change our Sprite animation.
		
	def update( self ):
		pass
	
	
	
	
	
	
	
	
	
	
class Projectile(Entity):
	def __init__(self, pos, actor_def, parent):
		Entity.__init__(self, pos, actor_def, parent, 'moving')
		self.directionalVelocity = None
		
	def collided( self ):	#Overwrite Entity's collided()
		self.collidable = False	#Disable collisions
		self.directionalVelocity.set((0,0))	#Stop movement
		self.setAction('death')	#Change to death animation
	
	def update( self ):
		#Move
		self.pos += self.directionalVelocity
		
		#Check bounds
		diff = self.parent.pos - self.pos
		if diff > GS.SCREEN_SIZE or diff < -GS.SCREEN_SIZE.len():	#Compare lengths. True if Projectile is more than 1 screen away from parent.
			self.delete()	#Kill this object
		
		#Update animation
		if self.action == 'moving':
			pass
		elif self.action == 'death':
			if GS.EQ.clock() - self.sprite._frame_timer > self.delay:
				frame = self.sprite.nextFrame()
				if not frame:	#If the animation is now on the first frame (aka we looped)...
					self.delete()	#Kill this object
		else:	#Default
			msg = 'Could not process action (%s) for object (%s).' % (self.action, str(self))
			raise KeyError, msg
		
		#Entity.update( self, dt )	#Do parent class's update
		
		
		
		
		
		
		
		
		
		
		
		
class EnemyLaser(Projectile):
	def __init__(self, pos, parent):
		Projectile.__init__(self, pos, animation_conf.masterAnimationDict['EnemyLaser'], parent)
		self.directionalVelocity = Vector.Twin(3,0).CWRotationDeg(self.heading)	#Set up our movement
		
		
		
		
		
		
		
		
		
		
class PlayerLaser(Projectile):
	def __init__(self, pos, parent):
		Projectile.__init__(self, pos, animation_conf.masterAnimationDict['PlayerLaser'], parent)
		self.directionalVelocity = Vector.Twin(10,0).CWRotationDeg(self.heading)	#Set up our movement
		
		
		
		
		
		
		
		
		
		
		
class Ship(Entity):
	dampening = Vector.Twin(.99, .99)
	
	def __init__(self, pos, actor_def, action):
		Entity.__init__(self, pos, actor_def, None, action)
		
		self.health = 1	#Current health.
		self.angularVelocity = 0.0	#Current turning speed.
		self.angularAcceleration = 0.1	#Maximum change in velocity per frame.
		self.lastShotTime = 0	#Clock time that the last shot was fired.
		
	def turn(self, angle):
		'''A clockwise turn in degrees.'''
		self.heading += angle
		self.heading = self.heading % 360	#Make sure angle is between -359 and +359
		#oldCenter = Vector.Twin(self.sprite.rect.center)
		self.sprite.rotate(self.heading)
		#newCenter = Vector.Twin(self.sprite.rect.center)
		#print newCenter
		#self.pos += oldCenter-newCenter
		
	def update( self ):
		self.lastShotTime += 1	#Move forward one frame
		self.angularVelocity *= 0.99
		self.directionalVelocity *= Ship.dampening
		
		if(self.angularVelocity):
			self.turn(self.angularVelocity)
			
		if(self.directionalVelocity):
			self.pos += self.directionalVelocity
			
			
			
			
			
			
			
			
			
			
			
class Player(gui.Keyable, Ship):
	vec = Vector.Twin(0.05,0)	#Movement vector
	
	def __init__(self,pos):
		gui.Keyable.__init__(self, [ K_1, K_2, K_3, K_4, K_7, K_8, K_9, K_0 ])
		Ship.__init__(self, pos, animation_conf.masterAnimationDict['Player'], 'off')
		self.health = 5	#Start with 5 health
		#self.lives = 3	#Lives count
		self.score = 0	#Keep track of score
		
		GS.player = self	#Make this object the player
		
	def collided( self ):	#Overwrite Entity's collided()
		Ship.collided(self)	#Default collided action
		self.health -= 1
		GS.shield.sprite.nextFrame()	#Change shield display
		self.setAction('hit')	#Change to hit animation
		
		#Create some events to flash the player's ship
		a = ['on', 'hit']
		j=0
		time = GS.EQ.clock()
		for i in xrange(50,500,50):	#Start at 50ms, go to 500ms, increment by 50ms
			GS.EQ.schedule(Event(time+i, self, Player.setAction, a[j]))
			j = (j+1)%2	#Switch between 0 and 1
			
		if self.health <= 0:
			w,h = GS.SCREEN_SIZE
			
			#Show "Game Over"
			txt = gui.TextField()
			txt.setFont(GS.font_digital_large)
			txt.setText( "Game Over" )
			centerX = w/2 - txt.textImage.get_rect().width/2
			centerY = 50
			txt.setPosition( ( centerX, centerY ) )
			GS.driver.getCurrentState().add( txt )
			
			#Show "Press 0 to continue."
			txt = gui.TextField()
			txt.setFont(GS.font_digital)
			txt.setText( "Press 0 to continue." )
			centerX = w/2 - txt.textImage.get_rect().width/2
			centerY = 100
			txt.setPosition( ( centerX, centerY ) )
			GS.driver.getCurrentState().add( txt )
			
			
			#Redefine the update function so player can't control ship.
			self.update = lambda: (Ship.update( self ), GS.camera.center(self.pos))
				
			for i in xrange(3):	#Create 3 Explosions
				b = self.pos + Vector.Twin(random.randint(-13,13), random.randint(-13,13))
				#GS.EQ.schedule(Event(time+i, None, Explosion, (b, None)))
				GS.EQ.schedule(Event(time+(i*73), None, ExplosionFactory, (b, self)))
		
	def keyEvent(self,key,unicode, pressed):
		self.pressed[key] = bool(pressed)
			
	def update( self ):
		enginesOn = False
		time = GS.EQ.clock()
		
		if(self.pressed[K_1]):	#
			pass
		if(self.pressed[K_2]):	#Left
			self.angularVelocity -= self.angularAcceleration
		if(self.pressed[K_3]):	#Forward
			rot = Player.vec.CWRotationDeg(self.heading)
			self.directionalVelocity += rot
			enginesOn = True
		if(self.pressed[K_4]):	#Right
			self.angularVelocity += self.angularAcceleration
		if(self.pressed[K_7] and self.lastShotTime > 17):	#Attack
			self.lastShotTime = 0
			a = Vector.Twin( 8, 0 ).CWRotationDeg(self.heading-90)
			b = Vector.Twin( 8, 0 ).CWRotationDeg(self.heading+90)
			PlayerLaser( self.pos+a, self )
			PlayerLaser( self.pos+b, self )
		if(self.pressed[K_8]):	#
			pass
		if(self.pressed[K_9]):	#
			pass
		if(self.pressed[K_0]):	#
			pass
		
		if(enginesOn and self.action == 'off'):	#Turn engines on
			self.setAction('on')
		if(not enginesOn) and self.action == 'on':	#Turn engines off
			self.setAction('off')
			
		Ship.update( self )	#Default update.
		GS.camera.center(self.pos)
	
	
	
	
	
	
	
	
	
	
class Enemy(Ship):
	moveVec = Vector.Twin(0.03, 0)	#Movement vector
	
	def __init__(self,pos):
		Ship.__init__(self, pos, animation_conf.masterAnimationDict['Enemy'], 'on')
		GS.enemies.append(self)
		self.angularAcceleration = 1
		#TODO: Pick random enemy graphic
		
	def collided( self ):
		self.collisionsDisable()	#Disable collisions
		death = EnemyDeath( self.pos )	#Create EnemyDeath object with same velocity and heading as self
		death.directionalVelocity = self.directionalVelocity
		death.heading = self.heading
		GS.EQ.schedule(Event(GS.EQ.clock()+250, self, Enemy.delete, None))	#Create event to destroy self in 250ms
		
	def delete(self):
		''' Clean up this object and create two Enemies.
		Since we don't want to waste resources, this object will be recommissioned as one of the new Enemies.
		'''
		p = GS.player.pos
		a = p + Vector.Twin( GS.SCREEN_SIZE[0], 0 ).CWRotationDeg(random.randint(0,359))
		b = p + Vector.Twin( GS.SCREEN_SIZE[0], 0 ).CWRotationDeg(random.randint(0,359))
		Enemy( a )	#Create a new enemy.
		
		#Fix up this Enemy
		for c in self.children:	#Clean list of children.
			c.delete()
		self.lastShotTime = 0	#Reset some variables.
		self.pos.set(b)	#New position.
		self.collisionsEnable()	#Reenable collisions.
		
	def update( self ):
		#Turn toward the player
		pointingVec = self.pos - GS.player.pos 	#Vector pointing at player
		angle = pointingVec.toDegrees() - self.heading	#Differences in angles. Bugs out if angles are equal.
		
		while (angle <= -180): angle += 360 
		while (angle > 180): angle -= 360
		
		#print "%4.0f" % (angle)
		
		if angle > 5:	#Left
			self.angularVelocity = -self.angularAcceleration
		elif angle < -5:	#Right
			self.angularVelocity = self.angularAcceleration
			
		if math.fabs(angle-180) < 20:	#On target (or close enough)
			#Fire something!
			if(pointingVec < GS.HALF_SCREEN_SIZE.len() and self.lastShotTime > 60):	#If player is half a screen away and we haven't attack in the last 17 frames...
				self.lastShotTime = 0
				a = Vector.Twin( 13, 0 ).CWRotationDeg(self.heading)
				EnemyLaser( self.pos+a, self )
						
		#Move
		rot = Enemy.moveVec.CWRotationDeg(self.heading)
		self.directionalVelocity += rot
		
		Ship.update( self )	#Default update
		
		
		
		
		
		
		
		
		
		
		
class Explosion( Entity ):
	def __init__( self, pos, parent ):
		Entity.__init__(self, pos, animation_conf.masterAnimationDict['Explosion'], None, 'death')
		self.parent = parent	#We do this manually so we don't become paren't children
		self.collisionsDisable()	#Don't want collisions with anything
		
	def delete( self ):	#Overwrite parent class's delete function.
		#Recommission this object
		a = self.parent.pos + Vector.Twin(random.randint(-13,13), random.randint(-13,13))
		self.pos.set(a)	#New position.
		
		
	
	def update( self ):
		#Update animation
		if GS.EQ.clock() - self.sprite._frame_timer > self.delay:
			frame = self.sprite.nextFrame()
			if not frame:	#If the animation is now on the first frame (aka we looped)...
				self.delete()	#Kill this object
		
		#Entity.update( self, dt )	#Do parent class's update
		
		
		
		
		
	
	
	
		
class EnemyDeath( Ship ):
	def __init__(self,pos):
		Ship.__init__(self, pos, animation_conf.masterAnimationDict['EnemyDeath'], 'death')
	
	def update( self ):
		#Update animation
		if self.action == 'death':
			if GS.EQ.clock() - self.sprite._frame_timer > self.delay:
				frame = self.sprite.nextFrame()
				if not frame:	#If the animation is now on the first frame (aka we looped)...
					Ship.delete( self )	#Kill this object
		else:	#Default
			msg = 'Could not process action (%s) for object (%s).' % (self.action, str(self))
			raise KeyError, msg
		
		Ship.update( self )
		
		
		
		
		
		
class HUD():
	def __init__( self ):
		self.pos = Vector.Twin( 0, 284 )
		self.heading = 0
		self.actor_def = animation_conf.masterAnimationDict['HUD']
		self.action = 'on'
		self.sprite = Sprite.Sprite( self )
		self.sprite.setAction( self.action )	#Change our Sprite animation.
		
	def draw(self,screen):
		self.sprite.draw(screen, self.pos)
		
		
		
		
		
		
		
class Shield():
	'''User interface to display current shield status
	'''
	def __init__( self ):
		GS.shield = self
		self.pos = Vector.Twin( 19, 304 )
		self.heading = 0
		self.actor_def = animation_conf.masterAnimationDict['Shield']
		self.action = 'on'
		self.sprite = Sprite.Sprite( self )
		self.sprite.setAction( self.action )	#Change our Sprite animation.
		
	def draw(self,screen):
		self.sprite.draw(screen, self.pos)
		
		
		
		
		
	
class PlayingGameState( GuiState ):
	def __init__( self, driver, screen ):
		GuiState.__init__( self, driver, screen )
		
	def draw( self, screen ):
		#Draw star field
		p = GS.player
		l = int( p.pos[0] ) - GS.SCREEN_SIZE[0]
		r = int( p.pos[0] ) + GS.SCREEN_SIZE[0]
		t = int( p.pos[1] ) - GS.SCREEN_SIZE[1]
		b = int( p.pos[1] ) + GS.SCREEN_SIZE[1]
		for j in xrange( 3 ):
			fn = self.starmap[j]
			c = self.starmapC[j]
			for i in xrange(self.starCount):
				d = p.directionalVelocity * c
				fo = fn[i] - d
				pygame.draw.line( screen, ( 255, 255, 255 ), ( fo - GS.camera.pos ).toTuple(), ( fn[i]-GS.camera.pos ).toTuple() )
				if( fn[i][0] > r ):	#Right
					fn[i] = Vector.Twin( l, random.randint( t, b ) )
				elif( fn[i][1] > b ): #Bottom
					fn[i] = Vector.Twin( random.randint( l, r ), t )
				elif( fn[i][0] < l ):	#Left
					fn[i] = Vector.Twin( r, random.randint( t, b ) )
				elif( fn[i][1] < t ): #Top
					fn[i] = Vector.Twin( random.randint( l, r ), b )
			
		GuiState.draw( self, screen )	#Standard draw
		
		
		#Draw green line for the player's velocity
		h = GS.HALF_SCREEN_SIZE
		pygame.draw.line( screen, 0x00ff00, h.toTuple(), ( p.directionalVelocity*10+h ).toTuple() )
		
		self.HUD.draw( screen )
		self.shield.draw( screen )
		self.text2.draw( screen )
		
	def init(self):
		#Object count
		#TODO: Remove this before public release
		self.text1 = gui.TextField( ( 5, 5 ) )
		self.add( self.text1 )	#Auto-draw
		
		#Player score
		self.text2 = gui.TextField( ( 160, 402 ) )
		
		self.HUD = HUD()
		self.shield = Shield()
		
		Player( Vector.Twin(0,0))	#Set up the player
		p = GS.player.pos
		self.text2.setText( str( GS.player.score ).zfill(3) )	#Update the score display
		
 		#Set up an enemy
	 	a = p + Vector.Twin( GS.SCREEN_SIZE[0], 0 ).CWRotationDeg(random.randint(0,359))
		Enemy( a )
		#Enemy( Vector.Twin( -100, 0 ) )
		
		#Some star fields
		self.starCount = 50
		l = int( p[0] ) - GS.SCREEN_SIZE[0]+1
		r = int( p[0] ) + GS.SCREEN_SIZE[0]-1
		t = int( p[1] ) - GS.SCREEN_SIZE[1]+1
		b = int( p[1] ) + GS.SCREEN_SIZE[1]-1
		
		self.nearStars = [ Vector.Twin( random.randint( l, r ), random.randint( t, b ) ) for i in xrange( self.starCount ) ]	#make some random points.
		self.midStars = [ Vector.Twin( random.randint( l, r ), random.randint( t, b ) ) for i in xrange( self.starCount ) ]
		self.farStars = [ Vector.Twin( random.randint( l, r ), random.randint( t, b ) ) for i in xrange( self.starCount ) ]
		self.starmap = [self.farStars, self.midStars, self.nearStars]	#Easy iteration later
		self.starmapC = [0, 1, 3]	#Length modifiers for "tail" of stars
	
	def keyEvent( self, key, unicode, pressed ):
		GuiState.keyEvent( self, key, unicode, pressed )
		if(GS.player.health == 0 and key == K_0):
			end = GameOver( self._driver, self.screen, GS.player.score )
			self._driver.replace(end)
			end.init()
	
	def update( self ):
		GuiState.update( self )
		p = GS.player
		
		if( p.health <= 0 ):
			#player is dead... do some explosions
			
			pass
		else:
			#Collision detection.
			for enemy in GS.enemies:
				for laser in enemy.children:
					#Player <-> EnemyLaser
					collide( p, laser )
				
				for laser in p.children:
					#Enemy <-> PlayerLaser
					if collide( enemy, laser ):
						#print 'enemy hit!'
						p.score += 1
						self.text2.setText( str( GS.player.score ).zfill(3) )
		
		#Move stars
		a = GS.player.directionalVelocity
		for i in xrange( self.starCount ):
			self.farStars[i] -= ( a * (-0.9) )
			self.midStars[i] -= ( a * (-0.4) )
			self.nearStars[i] -= ( a * (0.1) )
		
		#Update projectile text.
		self.text1.setText( "Objects: " + str( len( self.drawables ) ) )
		
		
		
		
		
		
		
		
		
		
''' Helper Functions '''
def collide( a, b ):
	if not (a.collidable and b.collidable and a.radius and b.radius):	#Make sure both a and b are collidable.
		return False	#Collision not possible.
	
	dist = (a.pos - b.pos).len()	#Find distance from a to b
	dist = math.fabs(dist)	#Make dist positive
	distance = dist - a.radius - b.radius
	if distance <= 0:	#Collision!
		a.collided()	#Call collided() on the objects
		b.collided()
		return True
	else:	#No collision
		return False

def quadratic( a, b, c):
	delta = (b**2) - (4 * a * c)
	#check if delta is below 0 (or neg)
	if (delta < 0):
		msg = "Error: No real solution to quadratic(%d, %d, %d)" % (a, b, c)
		raise msg
	else:	#else when delta is positive
		x1 = ((-b) + math.sqrt(delta)) / (2 * a)
		x2 = ((-b) - math.sqrt(delta)) / (2 * a)
		return (x1, x2)